# -*- coding: utf-8 -*-
from typing import Optional, Tuple, Any, List

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, QModelIndex, pyqtSlot, pyqtBoundSignal
from PyQt5.QtGui import QContextMenuEvent, QStandardItem
from PyQt5.QtWidgets import QTreeView, QMenu

from dgp.core.controllers.controller_interfaces import IFlightController, IAirborneController
from dgp.core.controllers.project_treemodel import ProjectTreeModel


class ProjectTreeView(QTreeView):
    """ProjectTreeView is a customized QTreeView use to display and interact
    with the hierarchy of a Gravity project(s) in the User Interface.

    This class is instantiated as a Promoted Widget within a Qt .ui form
    created wit Qt Designer.
    Because of this, the constructor does not accept a model instance, and the
    model should be instead set with the :func:`setModel` method.

    """
    def __init__(self, parent: Optional[QObject]=None):
        super().__init__(parent=parent)
        self.setMinimumSize(QtCore.QSize(0, 300))
        self.setAlternatingRowColors(False)
        self.setAutoExpandDelay(1)
        self.setExpandsOnDoubleClick(False)
        self.setRootIsDecorated(False)
        self.setUniformRowHeights(True)
        self.setHeaderHidden(True)
        self.setObjectName('project_tree_view')
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        # Set Stylesheet for Tree View, see:
        # http://doc.qt.io/qt-5/stylesheet-examples.html#customizing-qtreeview
        self.setStyleSheet("""
            QTreeView::item {
            }
            QTreeView::branch {
                /*background: palette(base);*/
            }
            QTreeView::branch:closed:has-children {
                background: none;
                image: url(:/icons/chevron-right);
            }
            QTreeView::branch:open:has-children {
                background: none;
                image: url(:/icons/chevron-down);
            }
        """)

        self._action_refs = []

    @staticmethod
    def _clear_signal(signal: pyqtBoundSignal):
        """Utility method to clear all connections from a bound signal"""
        while True:
            try:
                signal.disconnect()
            except TypeError:
                break

    def model(self) -> ProjectTreeModel:
        return super().model()

    def setModel(self, model: ProjectTreeModel):
        """Set the View Model and connect signals to its slots"""
        self._clear_signal(self.clicked)
        self._clear_signal(self.doubleClicked)
        super().setModel(model)

        self.clicked.connect(self._on_click)
        self.doubleClicked.connect(self._on_double_click)

    @pyqtSlot(QModelIndex, name='_on_click')
    def _on_click(self, index: QModelIndex):
        self.model().item_selected(index)

    @pyqtSlot(QModelIndex, name='_on_double_click')
    def _on_double_click(self, index: QModelIndex):
        """Selectively expand/collapse an item depending on its active state"""
        item = self.model().itemFromIndex(index)
        if isinstance(item, IFlightController):
            if item.is_active():
                self.setExpanded(index, not self.isExpanded(index))
            else:
                self.setExpanded(index, True)
        else:
            self.setExpanded(index, not self.isExpanded(index))
        self.model().item_activated(index)

    def _build_menu(self, menu: QMenu, bindings: List[Tuple[str, Tuple[Any]]]):
        self._action_refs.clear()
        for attr, params in bindings:
            if hasattr(QMenu, attr):
                res = getattr(menu, attr)(*params)
                self._action_refs.append(res)

    def contextMenuEvent(self, event: QContextMenuEvent, *args, **kwargs):
        index = self.indexAt(event.pos())
        item = self.model().itemFromIndex(index)  # type: QStandardItem
        expanded = self.isExpanded(index)

        menu = QMenu(self)
        bindings = getattr(item, 'menu_bindings', [])[:]  # type: List

        # Experimental Menu Inheritance/Extend functionality
        # if hasattr(event_item, 'inherit_context') and event_item.inherit_context:
        #     print("Inheriting parent menu(s)")
        #     ancestors = []
        #     parent = event_item.parent()
        #     while parent is not None:
        #         ancestors.append(parent)
        #         if not hasattr(parent, 'inherit_context'):
        #             break
        #         parent = parent.parent()
        #     print(ancestors)
        #
        #     ancestor_bindings = []
        #     for item in reversed(ancestors):
        #         if hasattr(item, 'menu_bindings'):
        #             ancestor_bindings.extend(item.menu_bindings)
        #     pprint(ancestor_bindings)
        #     bindings.extend(ancestor_bindings)

        if isinstance(item, IAirborneController):
            bindings.insert(0, ('addAction', ("Expand All", self.expandAll)))

        bindings.append(('addAction', ("Expand" if not expanded else "Collapse",
                                       lambda: self.setExpanded(index, not expanded))))
        # bindings.append(('addAction', ("Properties", self._get_item_attr(item, 'properties'))))

        self._build_menu(menu, bindings)
        menu.exec_(event.globalPos())
        event.accept()

    @staticmethod
    def _get_item_attr(item, attr):
        return getattr(item, attr, lambda *x, **y: None)
