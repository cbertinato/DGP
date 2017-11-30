# coding: utf-8

"""
Provide definitions of the models used by the Qt Application in our
model/view widgets.
"""

import logging
from typing import Union, List

import PyQt5.QtCore as QtCore
from PyQt5 import Qt
from PyQt5.Qt import QWidget
from PyQt5.QtCore import (QModelIndex, QVariant, QAbstractItemModel,
                          QMimeData, pyqtSignal, pyqtBoundSignal)
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtWidgets import QComboBox

from dgp.gui.qtenum import QtDataRoles, QtItemFlags
from dgp.lib.types import AbstractTreeItem, TreeItem, TreeLabelItem, DataChannel


class TableModel(QtCore.QAbstractTableModel):
    """Simple table model of key: value pairs."""

    def __init__(self, columns, editable=None, editheader=False, parent=None):
        super().__init__(parent=parent)
        # TODO: Allow specification of which columns are editable
        # List of column headers
        self._cols = columns
        self._rows = []
        self._editable = editable
        self._editheader = editheader
        self._updates = {}

    def set_object(self, obj):
        """
        Populates the model with key, value pairs from the passed objects'
        __dict__
        """
        for key, value in obj.__dict__.items():
            self.append(key, value)

    def append(self, *args):
        """
        Add a new row of data to the table, trimming input array to length of
        columns.
        """
        if not isinstance(args, list):
            args = list(args)
        while len(args) < len(self._cols):
            # Pad the end
            args.append(None)

        self._rows.append(args[:len(self._cols)])
        return True

    def get_row(self, row: int):
        try:
            return self._rows[row]
        except IndexError:
            print("Invalid row index")
            return None

    @property
    def updates(self):
        return self._updates

    @property
    def data(self):
        # TODO: Work on some sort of mapping to map column headers to row values
        return self._rows

    # Required implementations of super class (for a basic, non-editable table)

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self._rows)

    def columnCount(self, parent=None, *args, **kwargs):
        return len(self._cols)

    def data(self, index: QModelIndex, role=None):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            try:
                return self._rows[index.row()][index.column()]
            except IndexError:
                return None
        return QtCore.QVariant()

    def flags(self, index: QModelIndex):
        flags = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        if index.row() == 0 and self._editheader:
            flags = flags | QtCore.Qt.ItemIsEditable
        # Allow the values column to be edited
        elif self._editable is not None and index.column() in self._editable:
            flags = flags | QtCore.Qt.ItemIsEditable
        return flags

    def headerData(self, section, orientation, role=None):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self._cols[section]

    # Required implementations of super class for editable table

    def setData(self, index: QtCore.QModelIndex, value: QtCore.QVariant, role=None):
        """
        Basic implementation of editable model. This doesn't propagate the
        changes to the underlying object upon which the model was based
        though (yet)
        """
        if index.isValid() and role == QtCore.Qt.ItemIsEditable:
            self._rows[index.row()][index.column()] = value
            self.dataChanged.emit(index, index)
            return True
        else:
            return False


class BaseTreeModel(QAbstractItemModel):
    """
    Define common methods required for a Tree Model based on
    QAbstractItemModel.
    Subclasses must provide implementations for update() and data()
    """
    def __init__(self, root_item: AbstractTreeItem, parent=None):
        super().__init__(parent=parent)
        self._root = root_item

    @property
    def root(self):
        """
        @property

        Returns
        -------
        AbstractTreeItem:
            Top-level or root item in the model.
        """
        return self._root

    def parent(self, index: QModelIndex=QModelIndex()) -> QModelIndex:
        """
        Returns the parent QModelIndex of the given index. If the object
        referenced by index does not have a parent (i.e. the root node) an
        invalid QModelIndex() is constructed and returned.
        """
        if not index.isValid():
            return QModelIndex()

        child_item = index.internalPointer()  # type: AbstractTreeItem
        parent_item = child_item.parent  # type: AbstractTreeItem
        if parent_item == self._root or parent_item is None:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def update(self, *args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs

        Returns
        -------

        """
        raise NotImplementedError("Update must be implemented by subclass.")

    def data(self, index: QModelIndex, role: QtDataRoles=None):
        """

        Parameters
        ----------
        index
        role

        Returns
        -------

        """
        raise NotImplementedError("data() must be implemented by subclass.")

    def flags(self, index: QModelIndex) -> QtItemFlags:
        """Return the flags of an item at the specified ModelIndex"""
        if not index.isValid():
            return QtItemFlags.NoItemFlags
        return index.internalPointer().flags()

    @staticmethod
    def itemFromIndex(index: QModelIndex) -> AbstractTreeItem:
        """Returns the object referenced by index"""
        return index.internalPointer()

    @staticmethod
    def columnCount(parent: QModelIndex=QModelIndex(), *args, **kwargs):
        """Basic static implementation - returns 1"""
        return 1

    def headerData(self, section: int, orientation, role:
                   QtDataRoles=QtDataRoles.DisplayRole):
        """
        Returns display data for the Model header.
        If root has data of DisplayRole, it is returned here, otherwise an 
        empty QVariant() is returned.

        Returns
        -------
        QVariant:
            Data to display for header
        """
        if (orientation == QtCore.Qt.Horizontal and
                role == QtDataRoles.DisplayRole):
            return self._root.data(role)
        return QVariant()

    def index(self, row: int, col: int, parent: QModelIndex=QModelIndex(),
              *args, **kwargs) -> QModelIndex:
        """Return a QModelIndex for the item at the given row and column,
        with the specified parent."""
        if not self.hasIndex(row, col, parent):
            return QModelIndex()
        if not parent.isValid():
            parent_item = self._root
        else:
            parent_item = parent.internalPointer()  # type: AbstractTreeItem

        child_item = parent_item.child(row)
        # VITAL to compare is not None vs if child_item:
        if child_item is not None:
            return self.createIndex(row, col, child_item)
        else:
            return QModelIndex()

    def rowCount(self, parent: QModelIndex=QModelIndex(), *a, **kw) -> int:
        """

        Parameters
        ----------
        parent: QModelIndex
            Parent index to query row count

        Returns
        -------
        int:
            Count of children belonging to item at parent QModelIndex
        """
        # *args and **kwargs are necessary to suppress Qt Warnings
        if parent.isValid():
            return parent.internalPointer().child_count()
        return self._root.child_count()


class ProjectModel(BaseTreeModel):
    """Heirarchial (Tree) Project Model with a single root node."""
    def __init__(self, project: AbstractTreeItem, parent=None):
        self.log = logging.getLogger(__name__)
        super().__init__(TreeItem("root"), parent=parent)
        # assert isinstance(project, GravityProject)
        project.model = self
        self.root.append_child(project)
        self.layoutChanged.emit()
        self.log.info("Project Tree Model initialized.")

    def update(self, action=None, obj=None, **kwargs):
        """
        This simply emits layout change events to update the view.
        By calling layoutAboutToBeChanged and layoutChanged, we force an
        update of the entire layout that uses this model.
        This may not be as efficient as utilizing the beginInsertRows and
        endInsertRows signals to specify an exact range to update, but with
        the amount of data this model expects to handle, this is far less
        error prone and unnoticable.
        """
        self.layoutAboutToBeChanged.emit()
        self.log.info("ProjectModel Layout Changed")
        self.layoutChanged.emit()
        return

    def data(self, index: QModelIndex, role: QtDataRoles=None):
        """
        Returns data for the requested index and role.
        We do some processing here to encapsulate data within Qt Types where
        necesarry, as TreeItems in general do not import Qt Modules due to
        the possibilty of pickling them.

        Parameters
        ----------
        index: QModelIndex
            Model Index of item to retrieve data from
        role: QtDataRoles
            Role from the enumerated Qt roles in dgp/gui/qtenum.py

        Returns
        -------
        QVariant:
            Returns QVariant data depending on specified role.
            If role is UserRole, the underlying AbstractTreeItem object is
            returned
        """
        if not index.isValid():
            return QVariant()
        item = index.internalPointer()  # type: AbstractTreeItem
        data = item.data(role)

        # To guard against cases where role is not implemented
        if data is None:
            return QVariant()

        # Role encapsulation
        if role == QtDataRoles.UserRole:
            return item
        if role == QtDataRoles.DecorationRole:
            # Construct Decoration object from data
            return QIcon(data)
        if role in [QtDataRoles.BackgroundRole, QtDataRoles.ForegroundRole]:
            return QBrush(QColor(data))

        return QVariant(data)

    @staticmethod
    def flags(index: QModelIndex) -> QtItemFlags:
        """Return the flags of an item at the specified ModelIndex"""
        if not index.isValid():
            return QtItemFlags.NoItemFlags
        # return index.internalPointer().flags()
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled


# QStyledItemDelegate
class SelectionDelegate(Qt.QStyledItemDelegate):
    """Used by the Advanced Import Dialog to enable column selection/setting."""
    def __init__(self, choices, parent=None):
        super().__init__(parent=parent)
        self._choices = choices

    def createEditor(self, parent: QWidget, option: Qt.QStyleOptionViewItem,
                     index: QModelIndex) -> QWidget:
        """Creates the editor widget to display in the view"""
        editor = QComboBox(parent)
        editor.setFrame(False)
        for choice in sorted(self._choices):
            editor.addItem(choice)
        return editor

    def setEditorData(self, editor: QWidget, index: QModelIndex) -> None:
        """Set the value displayed in the editor widget based on the model data
        at the index"""
        combobox = editor  # type: QComboBox
        value = str(index.model().data(index, QtDataRoles.EditRole))
        index = combobox.findText(value)  # returns -1 if value not found
        if index != -1:
            combobox.setCurrentIndex(index)
        else:
            combobox.addItem(value)
            combobox.setCurrentIndex(combobox.count() - 1)

    def setModelData(self, editor: QWidget, model: QAbstractItemModel,
                     index: QModelIndex) -> None:
        combobox = editor  # type: QComboBox
        value = str(combobox.currentText())
        row = index.row()
        for c in range(model.columnCount()):
            mindex = model.index(row, c)
            data = str(model.data(mindex, QtCore.Qt.DisplayRole))
            if data == value:
                model.setData(mindex, '<Unassigned>', QtCore.Qt.EditRole)
        model.setData(index, value, QtCore.Qt.EditRole)

    def updateEditorGeometry(self, editor: QWidget, option: Qt.QStyleOptionViewItem,
                             index: QModelIndex) -> None:
        editor.setGeometry(option.rect)


class ChannelListModel(BaseTreeModel):
    """
    Creates a model with n+1 top-level headers where n = plots.

    Each plot has a header that channels can then be dragged to from the
    available channel list.
    The available channels list (displayed below the plot headers is
    constructed from the list of channels supplied.
    The plot headers limit the number of items that can be children to 2,
    this is so that the MatplotLib plotting canvas can display a left and
    right Y axis scale for each plot.

    Parameters
    ----------
    channels : List[DataChannel]
        List of DataChannels to add to the model upon instantiation
    plots: int
        Number of plot headings to generate
    parent:
        Optional Qt GUI Parent
    """

    plotOverflow = pyqtSignal(str)  # type: pyqtBoundSignal
    """
    SIGNAL pyqtSignal(str):
    
    Emits UID of item, when dropping item would exceed child limit on a 
    plot header.
    """
    channelChanged = pyqtSignal(int, int, DataChannel)  # type: pyqtBoundSignal
    """
    SIGNAL pyqtSignal(int, int, DataChannel)
    
    Emits (new_index: int, old_index: int, channel: DataChannel) upon 
    sucessful drag-drop action of a data channel.
    """

    def __init__(self, channels: List[DataChannel], plots: int, parent=None):
        super().__init__(TreeLabelItem('Channel Selection'), parent=parent)
        self._plots = {}
        self._child_limit = 2
        for i in range(plots):
            plt_label = TreeLabelItem('Plot {}'.format(i), True, 2)
            self._plots[i] = plt_label
            self.root.append_child(plt_label)
        self._available = TreeLabelItem('Available Channels')
        self._channels = {}
        self._build_model(channels)
        self.root.append_child(self._available)

    def _build_model(self, channels: List[DataChannel]):
        """Build the model representation"""
        for channel in channels:  # type: DataChannel
            self._channels[channel.uid] = channel
            if channel.plotted != -1:
                self._plots[channel.plotted].append_child(channel)
            else:
                self._available.append_child(channel)

    def append_channel(self, channel: DataChannel) -> None:
        """
        Append a DataChannel to the model

        New channels are placed under the 'Available Channels' header.

        Parameters
        ----------
        channel: DataChannel
            Channel to add
        """
        self._available.append_child(channel)
        self._channels[channel.uid] = channel

    def remove_channel(self, uid: str) -> bool:
        """
        Remove a DataChannel from the model by UID

        Parameters
        ----------
        uid: str
            DataChannel UID to locate and remove

        Returns
        -------
        bool:
            True on sucess, False if uid not located in model
        """
        if uid not in self._channels:
            return False
        cn = self._channels[uid]  # type: DataChannel
        cn_parent = cn.parent
        cn_parent.remove_child(cn)
        del self._channels[uid]
        return True

    def update(self) -> None:
        """
        Request an update of the model view by emitting layoutAboutToBeChanged
        and layoutChanged signals.
        """
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def data(self, index: QModelIndex, role: QtDataRoles=None) -> QVariant:
        item_data = index.internalPointer().data(role)
        if item_data is None:
            return QVariant()
        return item_data

    def flags(self, index: QModelIndex):
        item = index.internalPointer()
        if item == self.root:
            return QtCore.Qt.NoItemFlags
        if isinstance(item, DataChannel):
            return (QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsSelectable |
                    QtCore.Qt.ItemIsEnabled)
        return (QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled |
                QtCore.Qt.ItemIsDropEnabled)

    def supportedDropActions(self):
        return QtCore.Qt.MoveAction

    def supportedDragActions(self):
        return QtCore.Qt.MoveAction

    def dropMimeData(self, data: QMimeData, action, row, col,
                     parent: QModelIndex) -> bool:
        """
        Respond to MimeData being dropped on the model/view.
        Check is performed here to see if dropping a channel would exceed the
        child limit of a plot parent, as we want to enable the plotting of
        only 2 channels per plot in order to enable the use of a twin-y axis
        scale.

        Parameters
        ----------
        data: QMimeData
            QMimeData of the dropped object. Must contain Text referencing a
            channel UID.
        action: Qt::DropAction
            Drag and drop action. Must be MoveAction in this model.
        row: int
            Row index relative to new parent where drop occured
        col: int
            Column is ignored, assumed to be 1
        parent: QModelIndex
            New parent index of dropped object

        Returns
        -------
        bool:
            True on sucess
            False on failure/invalid drop
        """
        if action != QtCore.Qt.MoveAction:
            return False
        if not data.hasText():
            return False

        drop_object = self._channels.get(data.text(), None)  # type: DataChannel
        if drop_object is None:
            return False

        if not parent.isValid():
            if row == -1:
                p_item = self._available
                drop_object.plotted = False
                drop_object.axes = -1
            else:
                p_item = self.root.child(row-1)
        else:
            p_item = parent.internalPointer()  # type: TreeLabelItem
        if p_item.child_count() >= self._child_limit:
            if p_item != self._available:
                self.plotOverflow.emit(p_item.uid)
                return False

        # Remove the object to be dropped from its previous parent
        drop_parent = drop_object.parent
        drop_parent.remove_child(drop_object)
        self.beginInsertRows(parent, row, row)
        # For simplicity, simply append as the sub-order doesn't matter
        drop_object.axes = p_item.row()
        p_item.append_child(drop_object)
        self.endInsertRows()
        if drop_parent is self._available:
            old_row = -1
        else:
            old_row = drop_parent.row()
        if p_item is self._available:
            row = -1
        else:
            row = p_item.row()
        self.channelChanged.emit(row, old_row, drop_object)
        self.update()
        return True

    def canDropMimeData(self, data: QMimeData, action, row, col, parent:
                        QModelIndex) -> bool:
        """
        Queried when Mime data is dragged over/into the model. Returns 
        True if the data can be dropped. Does not guarantee that it will be 
        accepted.
        """
        if data.hasText():
            return True
        return False

    def mimeData(self, indexes):
        """
        Encodes a QMimeData reference of the object at index[0] of the
        specified indexes using the objects UID.

        Parameters
        ----------
        indexes: List[QModelIndex]
            List of QModelIndexes - should always be of length 1 as this is a
            single selection model/view.

        Returns
        -------
        QMimeData:
            Mime object containing the UID of the item at indexes[0] as a
            mime/text field.
        """
        index = indexes[0]
        item_uid = index.internalPointer().uid
        data = QMimeData()
        data.setText(item_uid)
        return data
