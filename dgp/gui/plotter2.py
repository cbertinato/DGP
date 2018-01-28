# coding: utf-8

# PROTOTYPE new LineGrabPlot class based on mplutils utility classes
import logging
from abc import ABCMeta, abstractmethod
from typing import Union
from itertools import cycle

import matplotlib as mpl
import pandas as pd
from PyQt5.QtWidgets import QSizePolicy, QMenu, QAction, QWidget
from PyQt5.QtCore import pyqtSignal, QMimeData
from PyQt5.QtGui import QCursor, QDropEvent, QDragEnterEvent, QDragMoveEvent
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT)
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from matplotlib.dates import DateFormatter, num2date, date2num
from matplotlib.ticker import NullFormatter, NullLocator, AutoLocator
from matplotlib.backend_bases import MouseEvent, PickEvent
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.text import Annotation
import numpy as np
import pyqtgraph as pg
from pyqtgraph.graphicsItems import AxisItem
from pyqtgraph.widgets.PlotWidget import PlotWidget, PlotItem

from dgp.lib.project import Flight

from ..lib.types import DataChannel, LineUpdate
from .mplutils import *


_log = logging.getLogger(__name__)

#######
# WIP #
#######


"""Design Requirements of FlightLinePlot:

Use Case:
FlightLinePlot (FLP) is designed for a specific use case, where the user may 
plot raw Gravity and GPS data channels on a synchronized x-axis plot in order to 
select distinct 'lines' of data (where the Ship or Aircraft has turned to 
another heading).

Requirements:
 - Able to display 2-4 plots displayed in a row with a linked x-axis scale.
 - Each plot must have dual y-axis scales and should limit the number of lines 
plotted to 1 per y-axis to allow for plotting of different channels of widely 
varying amplitudes.
- User can enable a 'line selection mode' which allows the user to 
graphically specify flight lines through the following functionality:
 - On click, a new semi-transparent rectangle 'patch' is created across all 
 visible axes. If there is no patch in the area already.
 - On drag of a patch, it should follow the mouse, allowing the user to 
 adjust its position.
 - On click and drag of the edge of any patch it should resize to the extent 
 of the movement, allowing the user to resize the patches.
 - On right-click of a patch, a context menu should be displayed allowing 
 user to label, or delete, or specify precise (spinbox) x/y limits of the patch

"""

__all__ = ['FlightLinePlot', 'TransformPlotWidget']


class BasePlottingCanvas(FigureCanvas):
    """
    BasePlottingCanvas sets up the basic Qt FigureCanvas parameters, and is
    designed to be subclassed for different plot types.
    Mouse events are connected to the canvas here, and the handlers should be
    overriden in sub-classes to provide custom actions.
    """
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        super().__init__(Figure(figsize=(width, height), dpi=dpi,
                                tight_layout=True))

        self.setParent(parent)
        super().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        super().updateGeometry()

        self.figure.canvas.mpl_connect('pick_event', self.onpick)
        self.figure.canvas.mpl_connect('button_press_event', self.onclick)
        self.figure.canvas.mpl_connect('button_release_event', self.onrelease)
        self.figure.canvas.mpl_connect('motion_notify_event', self.onmotion)

    def onclick(self, event: MouseEvent):
        pass

    def onrelease(self, event: MouseEvent):
        pass

    def onmotion(self, event: MouseEvent):
        pass

    def onpick(self, event: PickEvent):
        pass


class FlightLinePlot(BasePlottingCanvas):
    linechanged = pyqtSignal(LineUpdate)

    def __init__(self, flight, rows=3, width=8, height=4, dpi=100,
                 parent=None, **kwargs):
        _log.debug("Initializing FlightLinePlot")
        super().__init__(parent=parent, width=width, height=height, dpi=dpi)

        self._flight = flight
        # Allow dependency injection
        self.mgr = kwargs.get('axes_mgr', None) or StackedAxesManager(
            self.figure, rows=rows)
        self.pm = kwargs.get('patch_mgr', None) or PatchManager(parent=parent)

        self._home_action = QAction("Home")
        self._home_action.triggered.connect(lambda *args: print("Home Clicked"))
        self._zooming = False
        self._panning = False
        self._grab_lines = False
        self._toolbar = None

    def set_mode(self, grab=True):
        self._grab_lines = grab

    def get_toolbar(self, home_callback=None):
        """Configure and return the Matplotlib Toolbar used to interactively
        control the plot area.
        Here we replace the default MPL Home action with a custom action,
        and attach additional callbacks to the Pan and Zoom buttons.
        """
        if self._toolbar is not None:
            return self._toolbar

        def toggle(action):
            if action.lower() == 'zoom':
                print("Toggling zoom")
                self._panning = False
                self._zooming = not self._zooming
            elif action.lower() == 'pan':
                print("Toggling Pan")
                self._zooming = False
                self._panning = not self._panning
            else:
                self._zooming = False
                self._panning = False

        tb = NavigationToolbar2QT(self, parent=None)
        _home = tb.actions()[0]

        new_home = QAction(_home.icon(), "Home", parent=tb)
        home_callback = home_callback or (lambda *args: None)
        new_home.triggered.connect(home_callback)
        new_home.setToolTip("Reset View")
        tb.insertAction(_home, new_home)
        tb.removeAction(_home)

        tb.actions()[4].triggered.connect(lambda x: toggle('pan'))
        tb.actions()[5].triggered.connect(lambda x: toggle('zoom'))
        self._toolbar = tb
        return tb

    def add_series(self, channel: DataChannel, row=0, draw=True):
        self.mgr.add_series(channel.series(), row=row, uid=channel.uid)

    def onclick(self, event: MouseEvent):
        if not self._grab_lines or self._zooming or self._panning:
            print("Not in correct mode")
            return
        # If the event didn't occur within an Axes, ignore it
        if event.inaxes not in self.mgr:
            return

        # Else, process the click event
        # Get the patch group at click loc if it exists
        active = self.pm.select(event.xdata, inner=False)
        print("Active group: ", active)

        # Right Button
        if event.button == 3 and active:
            cursor = QCursor()
            self._pop_menu.popup(cursor.pos())
            return

        # Left Button
        elif event.button == 1 and not active:
            print("Creating new patch group")
            patches = []
            for ax, twin in self.mgr:
                xmin, xmax = ax.get_xlim()
                width = (xmax - xmin) * 0.05
                x0 = event.xdata - width / 2
                y0, y1 = ax.get_ylim()
                rect = Rectangle((x0, y0), width, height=1, alpha=0.1,
                                 edgecolor='black', linewidth=2, picker=True)
                patch = ax.add_patch(rect)
                patch.set_picker(True)
                ax.draw_artist(patch)
                patches.append(patch)
            pg = RectanglePatchGroup(*patches)
            self.pm.add_group(pg)
            self.draw()

            if self._flight.uid is not None:
                self.linechanged.emit(
                    LineUpdate(flight_id=self._flight.uid,
                               action='add',
                               uid=pg.uid,
                               start=pg.start(),
                               stop=pg.stop(),
                               label=None))
            return
        # Middle Button/Misc Button
        else:
            return

    def onmotion(self, event: MouseEvent) -> None:
        """
        Event Handler: Pass any motion events to the AxesGroup to handle,
        as long as the user is not Panning or Zooming.

        Parameters
        ----------
        event : MouseEvent
            Matplotlib MouseEvent object with event parameters

        Returns
        -------
        None

        """
        if self._zooming or self._panning:
            return
        self.pm.onmotion(event)

    def onrelease(self, event: MouseEvent) -> None:
        """
        Event Handler: Process event and emit any changes made to the active
        Patch group (if any) upon mouse release.

        Parameters
        ----------
        event : MouseEvent
            Matplotlib MouseEvent object with event parameters

        Returns
        -------
        None

        """
        if self._zooming or self._panning:
            self.pm.rescale_patches()
            self.draw()
            return

        active = self.pm.active
        if active is not None:
            if active.modified:
                self.linechanged.emit(
                    LineUpdate(flight_id=self._flight.uid,
                               action='modify',
                               uid=active.uid,
                               start=active.start(),
                               stop=active.stop(),
                               label=active.label))
            self.pm.deselect()
            self.figure.canvas.draw()


class DateAxis(pg.AxisItem):
    def tickStrings(self, values, scale, spacing):
        if not values:
            rng = 0
        else:
            rng = max(values)-min(values)
        # print("Range: ", rng, " scale: ", scale, " spacing: ", spacing)
        strns = []

        if rng < 1e12:
            strfmt = '%H:%M:%S'
        else:
            strfmt = '%Y-%m-%d %H:%M'

        for x in values:
            try:
                strns.append(pd.to_datetime(x).strftime(strfmt))
                # strns.append(time.strftime(string, time.localtime(x)))
            except ValueError:  ## Windows can't handle dates before 1970
                strns.append('')
            except OSError:
                print("OS Error in Date Formatter")
        return strns

    def tickSpacing(self, minVal, maxVal, size):
        # print("Get tickSpacing: minVal {}  maxVal {}  size {}".format(minVal,
        #                                                               maxVal,
        #                                                               size))
        # print("Min/max diff: ", maxVal - minVal)
        return super().tickSpacing(minVal, maxVal, size)


class TransformPlotWidget(QWidget):
    """
    Plot(s) based on pyqtgraph API used for fast data visualization for
    Transformation/filtering operations.

    Requirements:
    Multiple plots should be able to share an X-axis
    Support Date formatter for x-axis
    Date formatter should be optional, however? What if we need to plot vs
    scalar latitude/longitude.


    """
    def __init__(self, rows=2, sharex=True, parent=None):
        super().__init__(parent=parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                           QtWidgets.QSizePolicy.Expanding)
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.plots = []

        for i in range(rows):
            nplot = PlotWidget(parent=self,
                               axisItems={'bottom': DateAxis(
                                   orientation='bottom')},
                               background='w')
            if i > 0 and sharex:
                nplot.setXLink(self.plots[0])
            nplot.addLegend(offset=(-15, 15))
            self.plots.append(nplot)
            self.layout.addWidget(nplot)

    def get_plot(self, row=0):
        return self.plots[row]


class SeriesPlotter(metaclass=ABCMeta):
    colors = ['r', 'g', 'b', 'g']
    colorcycle = cycle([{'color': v} for v in colors])

    def __getattr__(self, item):
        """Passes attribute calls to underlying plotter object if no override
        in SeriesPlotter implementation."""
        if hasattr(self.plotter, item):
            attr = getattr(self.plotter, item)
            return attr
        raise AttributeError(item)

    @property
    @abstractmethod
    def plotter(self) -> Union[Axes, PlotItem]:
        """This property should return the underlying plot object, either a
        Matplotlib Axes or a PyQtgraph PlotItem"""
        pass

    @property
    @abstractmethod
    def items(self):
        """This property should return a list or a generator which yields the
        items plotted on the plot."""
        pass

    @abstractmethod
    def add_series(self, series, *args, **kwargs):
        pass

    @abstractmethod
    def remove_series(self, series):
        pass

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        """This method should clear all items from the Plotter"""
        pass


# Maybe use a Metaclass to dynamically generate methods based on the type of
# plot?
class PlotItemWrapper(SeriesPlotter):
    def __init__(self, plot):
        assert isinstance(plot, PlotItem)

        self._plot = plot
        self._lines = {}  # id(Series): line

    @property
    def plotter(self) -> PlotItem:
        return self._plot

    @property
    def items(self):
        for item in self._lines.values():
            yield item

    def add_series(self, series: pd.Series, *args, **kwargs):
        """Take in a pandas Series, add it to the plot and retain a
        reference."""
        sid = id(series)
        if sid in self.lines:
            print("Series already plotted")
            return
        xvals = pd.to_numeric(series.index, errors='coerce')
        yvals = pd.to_numeric(series.values, errors='coerce')

        line = self.plot.plot(x=xvals, y=yvals,
                              name=series.name,
                              pen=next(self.colorcycle))
        self._lines[sid] = line

    def remove_series(self, series):
        sid = id(series)
        if sid not in self._lines:
            return
        try:
            self._plot.legend.removeItem(self._lines[sid].name())
        except:
            pass
        self._plot.removeItem(self._lines[sid])
        del self._lines[sid]

    def draw(self):
        """Draw is uncecesarry for Pyqtgraph plots"""
        pass

    def clear(self):
        pass


class MPLAxesWrapper(SeriesPlotter):
    def __init__(self, plot, canvas=None):
        assert isinstance(plot, Axes)
        self._plot = plot
        self._lines = {}  # id(Series): Line2D
        self._canvas = canvas
        pass

    @property
    def plotter(self) -> Axes:
        return self._plot

    @property
    def items(self):
        pass

    def add_series(self, series, *args, **kwargs):
        line = self.plot.plot(series.index, series.values,
                              color=next(self.colorcycle)['color'],
                              label=series.name)
        self.draw()

    def remove_series(self, series):
        sid = id(series)
        line = self._lines[sid]  # type: Line2D
        line.remove()
        del self._lines[sid]

    def draw(self) -> None:
        pass

    def clear(self) -> None:
        pass