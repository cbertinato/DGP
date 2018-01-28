# coding: utf-8

from itertools import cycle
from typing import Dict

import PyQt5.QtGui as QtGui
from pandas import Series, DataFrame, to_numeric
from matplotlib.axes import Axes
from pyqtgraph.flowchart import Node, Terminal
from pyqtgraph.flowchart.library.Display import PlotWidgetNode

"""Containing display Nodes to translate between pyqtgraph Flowchart and an
MPL plot"""

__displayed__ = False


class MPLPlotNode(Node):
    nodeName = 'MPLPlotNode'

    def __init__(self, name):
        terminals = {'In': dict(io='in', multi=True)}
        super().__init__(name=name, terminals=terminals)
        self.plot = None
        self.canvas = None

    def set_plot(self, plot: Axes, canvas=None):
        self.plot = plot
        self.canvas = canvas

    def disconnected(self, localTerm, remoteTerm):
        """Called when connection is removed"""
        print("local/remote term type:")
        print(type(localTerm))
        print(type(remoteTerm))
        if localTerm is self['In']:
            pass

    def process(self, In: Dict, display=True) -> None:
        if display and self.plot is not None:
            # term is the Terminal from which the data originates
            for term, series in In.items():  # type: Terminal, Series
                if series is None:
                    continue

                if not isinstance(series, Series):
                    print("Incompatible data input")
                    continue

                self.plot.plot(series.index, series.values)
                if self.canvas is not None:
                    self.canvas.draw()


class PGPlotNode(Node):
    nodeName = 'PGPlotNode'

    def __init__(self, name):
        super().__init__(name, terminals={'In': dict(io='in', multi=True)})
        self.color_cycle = cycle([dict(color=(255, 193, 9)),
                                  dict(color=(232, 102, 12)),
                                  dict(color=(183, 12, 232))])
        self.plot = None
        self.items = {}  # SourceTerm: PlotItem

    def setPlot(self, plot):
        self.plot = plot

    def disconnected(self, localTerm, remoteTerm):
        if localTerm is self['In'] and remoteTerm in self.items:
            self.plot.removeItem(self.items[remoteTerm])
            del self.items[remoteTerm]

    def process(self, In, display=True):
        if display and self.plot is not None:
            items = set()
            # Add all new input items to selected plot
            for name, series in In.items():
                if series is None:
                    continue

                # TODO: Add UI Combobox to select channel if input is a DF?
                # But what about multiple inputs?
                assert isinstance(series, Series)

                uid = id(series)
                if uid in self.items and self.items[uid].scene() is self.plot.scene():
                    # Item is already added to the correct scene
                    items.add(uid)
                else:
                    # Add the item to the plot, or generate a new item if needed
                    # Need to convert series index/values to numeric type
                    # Otherwise numpy.isnan complains
                    xvals = to_numeric(series.index, errors='coerce')
                    yvals = to_numeric(series.values, errors='coerce')

                    item = self.plot.plot(x=xvals, y=yvals,
                                          name=series.name,
                                          pen=next(self.color_cycle))
                    self.items[uid] = item
                    items.add(uid)

            # Any left-over items that did not appear in the input must be removed
            for uid in list(self.items.keys()):
                if uid not in items:
                    # PlotWidget getattr wrapper fails when trying to
                    # retrieve 'legend' attr from the plotItem
                    # So we must access it directly
                    # This is because the PlotWidget getattr method only
                    # returns callable attributes from the underlying PlotItem
                    self.plot.plotItem.legend.removeItem(
                        self.items[uid].name())
                    self.plot.removeItem(self.items[uid])
                    del self.items[uid]

    def ctrlWidget(self):
        return None

    def updateUi(self):
        pass

