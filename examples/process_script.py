import os
from datetime import datetime
import yaml

from dgp.lib.gravity_ingestor import read_at1a
from dgp.lib.trajectory_ingestor import import_trajectory
from dgp.lib.etc import align_frames
from dgp.lib.transform.transform_graphs import AirbornePost
from dgp.lib.transform.filters import detrend
from dgp.lib.plots import timeseries_gravity_diagnostic, mapplot_segment, read_meterconfig

# Runtime Options
write_out = True
make_plots = True
add_map_plots = False
diagnostic = True

# Read YAML config file
proj_path = os.path.abspath(os.path.dirname(__file__))
try:
    with open(os.path.join(proj_path, 'config_runtime.yaml'), 'r') as file:
        config = yaml.safe_load(file)
        print('Read YAML configuration file for {}'.format(config['flight']))
except Exception as e:
    print('Error reading the config file')
    # TODO What to do if exception is reached? Exit, or read in test data?
campaign = config['campaign']
flight = config['flight']
begin_line = datetime.strptime(config['begin_line'], '%Y-%m-%d %H:%M')
end_line = datetime.strptime(config['end_line'], '%Y-%m-%d %H:%M')
gravity_directory = config['gravity_dir']
gravity_file = config['gravity_file']
trajectory_source = config['trajectory_src']
trajectory_directory = config['trajectory_dir']
trajectory_file = config['trajectory_file']
gps_fields = config['gps_fields']
configdir = config['config_dir']
outdir = config['out_dir']
try:
    QC_segment = config['QC1']  #
    QC_plot = True
except KeyError:
    print('No QC Segments...')
    QC_plot = False
if trajectory_source == 'Waypoint':
    trajectory_engine = 'c'
    trajectory_delim = ','
else:
    trajectory_engine = 'python'
    trajectory_delim = '\s+'

# Load Data Files
print('\nImporting gravity')
gravity = read_at1a(os.path.join(gravity_directory, gravity_file), interp=True)
print("Gravity START: {}".format(gravity.index[0]))
print("Gravity END:   {}".format(gravity.index[-1]))
print('\nImporting trajectory')
trajectory = import_trajectory(os.path.join(trajectory_directory, trajectory_file),
                               columns=gps_fields, skiprows=1,
                               timeformat='hms', engine=trajectory_engine, sep=trajectory_delim)

# Read MeterProcessing file in Data Directory
config_file = os.path.join(configdir, 'DGS_config_files', 'MeterProcessing.ini')
k_factor = read_meterconfig(config_file, 'kfactor')
tie_gravity = read_meterconfig(config_file, 'TieGravity')
print('K-factor:    {}\nGravity-tie: {}\n'.format(k_factor, tie_gravity))

# Still Readings
#  TODO: Semi-automate or create GUI to get statics
first_static = read_meterconfig(config_file, 'PreStill')
second_static = read_meterconfig(config_file, 'PostStill')

# pre-processing prep
if not begin_line < end_line:
    print('Check your times.  Using start and end of gravity file instead.')
    begin_line = gravity.index[0]
    end_line = gravity.index[-1]
trajectory_full = trajectory[['long', 'lat']]
gravity = gravity[(begin_line <= gravity.index) & (gravity.index <= end_line)]
trajectory = trajectory[(begin_line <= trajectory.index) & (trajectory.index <= end_line)]

# Save a 'meter_gravity' column for diagnostic output
gravity['meter_gravity'] = gravity['gravity']

# align gravity and trajectory frames
gravity, trajectory = align_frames(gravity, trajectory)

# adjust for crossing the prime meridian
trajectory['long'] = trajectory['long'].where(trajectory['long'] > 0, trajectory['long'] + 360)

# de-drift
if not diagnostic:
    gravity['gravity'] = detrend(gravity['gravity'], first_static, second_static)

# adjust to absolute
offset = tie_gravity - k_factor * first_static
gravity['gravity'] += offset

print('\nProcessing')
g = AirbornePost(trajectory, gravity, begin_static=first_static, end_static=second_static)
results = g.execute()

if write_out:   # TODO: split this file up into a Diagnostic and Standard output
    import numpy as np
    import pandas as pd
    print('\nWriting Output to File')
    time = pd.Series(trajectory.index.astype(np.int64) / 10 ** 9,
                     index=trajectory.index, name='unix_time')
    columns = ['unixtime', 'lat', 'long', 'ell_ht',
               'eotvos_corr', 'kin_accel_corr', 'meter_grav',
               'lat_corr', 'fa_corr', 'total_corr',
               'abs_grav', 'FAA', 'FAA_LP']
    values = np.array([time.values, trajectory['lat'].values, trajectory['long'].values, trajectory['ell_ht'].values,
                       results['eotvos'].values, results['kin_accel'].values, gravity['meter_gravity'].values,
                       results['lat_corr'].values, results['fac'].values, results['total_corr'].values,
                       results['abs_grav'].values, results['corrected_grav'].values, results['filtered_grav'].values])
    #
    df = pd.DataFrame(data=values.T, columns=columns, index=time)   #pd.DatetimeIndex(gravity.index)
    df = df.apply(pd.to_numeric, errors='ignore')
    df.index = pd.to_datetime(trajectory.index)
    outfile = os.path.join(outdir, '{}_{}_{}_DGP.csv'.format(campaign, flight, str(begin_line.strftime('%Y%m%d_%H%Mz'))))
    df.to_csv(outfile)  # , na_rep=" ")

###########
# Real plots

if make_plots:
    print('\nPlotting')
    # Time-series Plot
    variables = ['meter_gravity', 'gravity', 'cross_accel', 'beam', 'temp']
    variable_units = ['mGal', 'mGal', 'mGal', ' ', 'C']
    plot_title = '{} {}: QC'.format(campaign, flight)
    plot_file = os.path.join(outdir, '{}_{}_DGP_QCplot_meter.png'.format(campaign, flight))
    timeseries_gravity_diagnostic(gravity, variables, variable_units, begin_line, end_line,
                                  plot_title, plot_file)

    variables = ['ell_ht', 'lat', 'long']
    variable_units = ['m', 'degrees', 'degrees']
    plot_title = '{} {}: PNT'.format(campaign, flight)
    plot_file = os.path.join(outdir, '{}_{}_DGP_QCplot_trajectory.png'.format(campaign, flight))
    timeseries_gravity_diagnostic(results['trajectory'], variables, variable_units, begin_line, end_line,
                                  plot_title, plot_file)

    variables = ['eotvos', 'lat_corr', 'fac', 'kin_accel', 'total_corr']
    variable_units = ['mGal', 'mGal', 'mGal', 'mGal', 'mGal']
    plot_title = '{} {}: Corrections'.format(campaign, flight)
    plot_file = os.path.join(outdir, '{}_{}_DGP_QCplot_corrections.png'.format(campaign, flight))
    timeseries_gravity_diagnostic(results, variables, variable_units, begin_line, end_line,
                                  plot_title, plot_file)

    variables = ['abs_grav', 'corrected_grav', 'filtered_grav']
    variable_units = ['mGal', 'mGal', 'mGal']
    plot_title = '{} {}: Gravity'.format(campaign, flight)
    plot_file = os.path.join(outdir, '{}_{}_DGP_QCplot_freeair.png'.format(campaign, flight))
    timeseries_gravity_diagnostic(results, variables, variable_units, begin_line, end_line,
                                  plot_title, plot_file)

    if QC_plot:
        # QC Segment Plot
        variables = ['filtered_grav', 'corrected_grav', 'abs_grav']
        variable_units = ['mGal', 'mGal', 'mGal', 'mGal']
        plot_title = '{} {}: Gravity (segment)'.format(campaign, flight)
        plot_file = os.path.join(outdir, '{}_{}_DGP_QCplot_freeair_segment.png'.format(campaign, flight))
        timeseries_gravity_diagnostic(results, variables, variable_units,
                                      QC_segment['start'], QC_segment['end'],
                                      plot_title, plot_file)

    if add_map_plots:
        plot_title = '{} {}: Gravity'.format(campaign, flight)
        plot_file = os.path.join(outdir, '{}_{}_DGP_QCplot_freeair_map.png'.format(campaign, flight))
        mapplot_segment(results, 'filtered_grav',
                        QC_segment['start'], QC_segment['end'],
                        'mGal', plot_title, plot_file)