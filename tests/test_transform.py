# coding: utf-8

import os
import unittest
import numpy as np
import pandas as pd
from copy import deepcopy
from scipy import signal

from .context import  dgp
from dgp.lib.transform import TransformChain, DataWrapper, Filter

from copy import deepcopy


class TestTransform(unittest.TestCase):
    def test_basic_transform_chain_ops(self):
        df = pd.DataFrame({'A': range(11), 'B': range(11)})

        tc = TransformChain()

        def transform1(df):
            df['A'] = df['A'] + 3.
            return df

        def transform2(df):
            df['A'] = df['A'] + df['B']
            return df

        def transform3(df):
            df = (df + df.shift(1)).dropna()
            return df

        tc.addtransform(transform1)
        tc.addtransform(transform2)
        tc.addtransform(transform3)

        self.assertTrue(len(tc) == 3)

        new_df_A = tc.apply(df)

        df_A = deepcopy(df)
        df_A['A'] = df_A['A'] + 3.
        df_A['A'] = df_A['A'] + df_A['B']
        df_A = (df_A + df_A.shift(1)).dropna()

        self.assertTrue(new_df_A.equals(df_A))

        # test reordering
        reordering = {tc[2]: 0, tc[0]: 2}
        reordered_uids = [tc.ordering[-1], tc.ordering[1], tc.ordering[0]]
        tc.reorder(reordering)

        self.assertTrue(tc.ordering == reordered_uids)

        xforms = [transform3, transform2, transform1]
        reordered_xforms = [t for t in tc]
        self.assertTrue(xforms == reordered_xforms)

    def test_basic_data_wrapper(self):

        def transform1a(df):
            df['A'] = df['A'] + 3.
            return df

        def transform2a(df):
            df['A'] = df['A'] + df['B']
            return df

        def transform1b(df):
            df['A'] = df['A'] * 3
            return df

        def transform2b(df):
            df['C'] = df['A'] + df['B'] * 2
            return df

        tc_a = TransformChain()
        tc_a.addtransform(transform1a)
        tc_a.addtransform(transform2a)

        tc_b = TransformChain()
        tc_b.addtransform(transform1b)
        tc_b.addtransform(transform2b)

        df = pd.DataFrame({'A': range(11), 'B': range(11)})
        wrapper = DataWrapper(df)
        df_a = wrapper.applychain(tc_a)
        df_b = wrapper.applychain(tc_b)

        df_a_true = deepcopy(df)
        df_a_true['A'] = df_a_true['A'] + 3.
        df_a_true['A'] = df_a_true['A'] + df_a_true['B']

        df_b_true = deepcopy(df)
        df_b_true['A'] = df_b_true['A'] * 3
        df_b_true['C'] = df_b_true['A'] + df_b_true['B'] * 2

        self.assertTrue(df_a.equals(df_a_true))
        self.assertTrue(df_b.equals(df_b_true))

        self.assertTrue(len(wrapper) == 2)

        self.assertTrue(df_a.equals(wrapper.modified[tc_a.uid]))
        self.assertTrue(df_b.equals(wrapper.modified[tc_b.uid]))

    def test_simple_filter_class(self):

        def lp_filter(data, fc, fs, window):
            return data

        lp = Filter(func=lp_filter, fc=10, fs=100, typ='low pass')

        self.assertTrue(lp.fc == 10)
        self.assertTrue(lp.fs == 100)
        self.assertTrue(lp.nyq == lp.fs * 0.5)
        self.assertTrue(lp.wn == lp.fc / lp.nyq)
        self.assertTrue(lp.filtertype == 'low pass')
        self.assertTrue(lp.transformtype == 'filter')

        data = np.ones(5)
        res = lp(data)
        np.testing.assert_array_equal(res, data)

    def _find_comp(self, sig, fs):
        w = np.fft.fft(sig)
        freqs = np.fft.fftfreq(len(w))
        n = np.argpartition(np.abs(w), -10)[-10:]
        ind = n[np.abs(w)[n] > 100]
        freq = np.unique(np.abs(freqs[ind])) * fs
        return list(freq)

    def test_lp_filter_class(self):

        def lp_filter(data, fc, fs, window):
            filter_len = 1 / fc
            nyq = fs / 2.0
            wn = fc / nyq
            N = int(2.0 * filter_len * fs)
            taps = signal.firwin(N, wn, window=window, nyq=nyq)
            filtered_data = signal.filtfilt(taps, 1.0, data, padtype='even', padlen=80)
            return filtered_data

        # generate a signal
        fs = 100 # Hz
        frequencies = [1.2, 3, 5, 7] # Hz
        start = 0
        stop = 10 # s
        t = np.linspace(start, stop, fs * (stop - start))
        sig = np.zeros(len(t))
        for f in frequencies:
            sig += np.sin(2 * np.pi * f * t )

        freq_before = self._find_comp(sig, fs)
        lp = Filter(func=lp_filter, fc=5, fs=fs, typ='low pass')

        self.assertTrue(lp.window == 'blackman')

        filtered_sig = lp(sig)
        freq_after = self._find_comp(filtered_sig, fs)
        self.assertTrue(freq_after == [1.2, 3])
