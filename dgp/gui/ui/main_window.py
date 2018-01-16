# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dgp/gui/ui\main_window.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1490, 1135)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/geoid"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tab_workspace = TabWorkspace(self.centralwidget)
        self.tab_workspace.setObjectName("tab_workspace")
        self.horizontalLayout.addWidget(self.tab_workspace)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1490, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(True)
        self.statusbar.setAutoFillBackground(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.project_dock = QtWidgets.QDockWidget(MainWindow)
        self.project_dock.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.project_dock.sizePolicy().hasHeightForWidth())
        self.project_dock.setSizePolicy(sizePolicy)
        self.project_dock.setMinimumSize(QtCore.QSize(359, 262))
        self.project_dock.setMaximumSize(QtCore.QSize(524287, 524287))
        self.project_dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea|QtCore.Qt.RightDockWidgetArea)
        self.project_dock.setObjectName("project_dock")
        self.project_dock_contents = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.project_dock_contents.sizePolicy().hasHeightForWidth())
        self.project_dock_contents.setSizePolicy(sizePolicy)
        self.project_dock_contents.setObjectName("project_dock_contents")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.project_dock_contents)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.project_dock_grid = QtWidgets.QGridLayout()
        self.project_dock_grid.setContentsMargins(5, -1, -1, -1)
        self.project_dock_grid.setSpacing(3)
        self.project_dock_grid.setObjectName("project_dock_grid")
        self.label_prj_info = QtWidgets.QLabel(self.project_dock_contents)
        self.label_prj_info.setObjectName("label_prj_info")
        self.project_dock_grid.addWidget(self.label_prj_info, 0, 0, 1, 1)
        self.prj_add_flight = QtWidgets.QPushButton(self.project_dock_contents)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/airborne"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prj_add_flight.setIcon(icon1)
        self.prj_add_flight.setObjectName("prj_add_flight")
        self.project_dock_grid.addWidget(self.prj_add_flight, 2, 0, 1, 1)
        self.prj_add_meter = QtWidgets.QPushButton(self.project_dock_contents)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/meter_config.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prj_add_meter.setIcon(icon2)
        self.prj_add_meter.setObjectName("prj_add_meter")
        self.project_dock_grid.addWidget(self.prj_add_meter, 2, 1, 1, 1)
        self.prj_import_gps = QtWidgets.QPushButton(self.project_dock_contents)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/gps"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prj_import_gps.setIcon(icon3)
        self.prj_import_gps.setObjectName("prj_import_gps")
        self.project_dock_grid.addWidget(self.prj_import_gps, 4, 0, 1, 1)
        self.prj_import_grav = QtWidgets.QPushButton(self.project_dock_contents)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/gravity"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.prj_import_grav.setIcon(icon4)
        self.prj_import_grav.setIconSize(QtCore.QSize(16, 16))
        self.prj_import_grav.setObjectName("prj_import_grav")
        self.project_dock_grid.addWidget(self.prj_import_grav, 4, 1, 1, 1)
        self.contextual_tree = QtWidgets.QTreeView(self.project_dock_contents)
        self.contextual_tree.setDragEnabled(False)
        self.contextual_tree.setDragDropOverwriteMode(False)
        self.contextual_tree.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.contextual_tree.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.contextual_tree.setUniformRowHeights(True)
        self.contextual_tree.setObjectName("contextual_tree")
        self.contextual_tree.header().setVisible(False)
        self.project_dock_grid.addWidget(self.contextual_tree, 1, 0, 1, 2)
        self.verticalLayout_4.addLayout(self.project_dock_grid)
        self.project_dock.setWidget(self.project_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.project_dock)
        self.toolbar = QtWidgets.QToolBar(MainWindow)
        self.toolbar.setFloatable(False)
        self.toolbar.setObjectName("toolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.info_dock = QtWidgets.QDockWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_dock.sizePolicy().hasHeightForWidth())
        self.info_dock.setSizePolicy(sizePolicy)
        self.info_dock.setMinimumSize(QtCore.QSize(644, 246))
        self.info_dock.setMaximumSize(QtCore.QSize(524287, 246))
        self.info_dock.setSizeIncrement(QtCore.QSize(0, 0))
        self.info_dock.setFeatures(QtWidgets.QDockWidget.AllDockWidgetFeatures)
        self.info_dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea|QtCore.Qt.TopDockWidgetArea)
        self.info_dock.setObjectName("info_dock")
        self.console_dock_contents = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_dock_contents.sizePolicy().hasHeightForWidth())
        self.console_dock_contents.setSizePolicy(sizePolicy)
        self.console_dock_contents.setObjectName("console_dock_contents")
        self.gridLayout = QtWidgets.QGridLayout(self.console_dock_contents)
        self.gridLayout.setContentsMargins(5, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.console_frame = QtWidgets.QFrame(self.console_dock_contents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_frame.sizePolicy().hasHeightForWidth())
        self.console_frame.setSizePolicy(sizePolicy)
        self.console_frame.setSizeIncrement(QtCore.QSize(2, 0))
        self.console_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.console_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.console_frame.setObjectName("console_frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.console_frame)
        self.verticalLayout_2.setContentsMargins(6, 0, 0, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text_console = QtWidgets.QTextEdit(self.console_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_console.sizePolicy().hasHeightForWidth())
        self.text_console.setSizePolicy(sizePolicy)
        self.text_console.setMinimumSize(QtCore.QSize(0, 100))
        self.text_console.setMaximumSize(QtCore.QSize(16777215, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.text_console.setPalette(palette)
        self.text_console.setAutoFillBackground(True)
        self.text_console.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.text_console.setReadOnly(True)
        self.text_console.setObjectName("text_console")
        self.verticalLayout_2.addWidget(self.text_console)
        self.console_btns_layout = QtWidgets.QGridLayout()
        self.console_btns_layout.setObjectName("console_btns_layout")
        self.combo_console_verbosity = QtWidgets.QComboBox(self.console_frame)
        self.combo_console_verbosity.setObjectName("combo_console_verbosity")
        self.combo_console_verbosity.addItem("")
        self.combo_console_verbosity.addItem("")
        self.combo_console_verbosity.addItem("")
        self.combo_console_verbosity.addItem("")
        self.combo_console_verbosity.addItem("")
        self.console_btns_layout.addWidget(self.combo_console_verbosity, 0, 2, 1, 1)
        self.btn_clear_console = QtWidgets.QPushButton(self.console_frame)
        self.btn_clear_console.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btn_clear_console.setObjectName("btn_clear_console")
        self.console_btns_layout.addWidget(self.btn_clear_console, 0, 0, 1, 1)
        self.label_logging_level = QtWidgets.QLabel(self.console_frame)
        self.label_logging_level.setObjectName("label_logging_level")
        self.console_btns_layout.addWidget(self.label_logging_level, 0, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.console_btns_layout)
        self.gridLayout.addWidget(self.console_frame, 0, 1, 1, 1)
        self.text_info = QtWidgets.QPlainTextEdit(self.console_dock_contents)
        self.text_info.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_info.sizePolicy().hasHeightForWidth())
        self.text_info.setSizePolicy(sizePolicy)
        self.text_info.setMinimumSize(QtCore.QSize(0, 100))
        self.text_info.setSizeIncrement(QtCore.QSize(1, 0))
        self.text_info.setReadOnly(True)
        self.text_info.setPlainText("")
        self.text_info.setObjectName("text_info")
        self.gridLayout.addWidget(self.text_info, 0, 0, 1, 1)
        self.info_dock.setWidget(self.console_dock_contents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(8), self.info_dock)
        self.actionDocumentation = QtWidgets.QAction(MainWindow)
        self.actionDocumentation.setObjectName("actionDocumentation")
        self.action_exit = QtWidgets.QAction(MainWindow)
        self.action_exit.setObjectName("action_exit")
        self.action_project_dock = QtWidgets.QAction(MainWindow)
        self.action_project_dock.setCheckable(True)
        self.action_project_dock.setChecked(True)
        self.action_project_dock.setObjectName("action_project_dock")
        self.action_tool_dock = QtWidgets.QAction(MainWindow)
        self.action_tool_dock.setCheckable(True)
        self.action_tool_dock.setChecked(False)
        self.action_tool_dock.setObjectName("action_tool_dock")
        self.action_file_new = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/new_file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_file_new.setIcon(icon5)
        self.action_file_new.setObjectName("action_file_new")
        self.action_file_open = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/folder_open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_file_open.setIcon(icon6)
        self.action_file_open.setObjectName("action_file_open")
        self.action_file_save = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/save_project.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_file_save.setIcon(icon7)
        self.action_file_save.setObjectName("action_file_save")
        self.action_add_flight = QtWidgets.QAction(MainWindow)
        self.action_add_flight.setIcon(icon1)
        self.action_add_flight.setObjectName("action_add_flight")
        self.action_add_meter = QtWidgets.QAction(MainWindow)
        self.action_add_meter.setIcon(icon2)
        self.action_add_meter.setObjectName("action_add_meter")
        self.action_project_info = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/icons/dgs"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_project_info.setIcon(icon8)
        self.action_project_info.setObjectName("action_project_info")
        self.action_info_dock = QtWidgets.QAction(MainWindow)
        self.action_info_dock.setCheckable(True)
        self.action_info_dock.setChecked(True)
        self.action_info_dock.setObjectName("action_info_dock")
        self.action_import_gps = QtWidgets.QAction(MainWindow)
        self.action_import_gps.setIcon(icon3)
        self.action_import_gps.setObjectName("action_import_gps")
        self.action_import_grav = QtWidgets.QAction(MainWindow)
        self.action_import_grav.setIcon(icon4)
        self.action_import_grav.setObjectName("action_import_grav")
        self.menuFile.addAction(self.action_file_new)
        self.menuFile.addAction(self.action_file_open)
        self.menuFile.addAction(self.action_file_save)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_exit)
        self.menuHelp.addAction(self.actionDocumentation)
        self.menuView.addAction(self.action_project_dock)
        self.menuView.addAction(self.action_tool_dock)
        self.menuView.addAction(self.action_info_dock)
        self.menuProject.addAction(self.action_import_grav)
        self.menuProject.addAction(self.action_import_gps)
        self.menuProject.addAction(self.action_add_flight)
        self.menuProject.addAction(self.action_add_meter)
        self.menuProject.addAction(self.action_project_info)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolbar.addAction(self.action_file_new)
        self.toolbar.addAction(self.action_file_open)
        self.toolbar.addAction(self.action_file_save)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.action_add_flight)
        self.toolbar.addAction(self.action_add_meter)
        self.toolbar.addAction(self.action_import_gps)
        self.toolbar.addAction(self.action_import_grav)
        self.toolbar.addSeparator()

        self.retranslateUi(MainWindow)
        self.action_project_dock.toggled['bool'].connect(self.project_dock.setVisible)
        self.project_dock.visibilityChanged['bool'].connect(self.action_project_dock.setChecked)
        self.action_info_dock.toggled['bool'].connect(self.info_dock.setVisible)
        self.info_dock.visibilityChanged['bool'].connect(self.action_info_dock.setChecked)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dynamic Gravity Processor"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuView.setTitle(_translate("MainWindow", "Panels"))
        self.menuProject.setTitle(_translate("MainWindow", "Project"))
        self.project_dock.setWindowTitle(_translate("MainWindow", "Project"))
        self.label_prj_info.setText(_translate("MainWindow", "Project Tree:"))
        self.prj_add_flight.setText(_translate("MainWindow", "Add Flight"))
        self.prj_add_meter.setText(_translate("MainWindow", "Add Meter"))
        self.prj_import_gps.setText(_translate("MainWindow", "Import GPS"))
        self.prj_import_grav.setText(_translate("MainWindow", "Import Gravity"))
        self.toolbar.setWindowTitle(_translate("MainWindow", "Toolbar"))
        self.info_dock.setWindowTitle(_translate("MainWindow", "Info/Console"))
        self.combo_console_verbosity.setItemText(0, _translate("MainWindow", "Debug"))
        self.combo_console_verbosity.setItemText(1, _translate("MainWindow", "Info"))
        self.combo_console_verbosity.setItemText(2, _translate("MainWindow", "Warning"))
        self.combo_console_verbosity.setItemText(3, _translate("MainWindow", "Error"))
        self.combo_console_verbosity.setItemText(4, _translate("MainWindow", "Critical"))
        self.btn_clear_console.setText(_translate("MainWindow", "Clear"))
        self.label_logging_level.setText(_translate("MainWindow", "<html><head/><body><p align=\"right\">Logging Level:</p></body></html>"))
        self.text_info.setPlaceholderText(_translate("MainWindow", "Selection Info"))
        self.actionDocumentation.setText(_translate("MainWindow", "Documentation"))
        self.actionDocumentation.setShortcut(_translate("MainWindow", "F1"))
        self.action_exit.setText(_translate("MainWindow", "Exit"))
        self.action_exit.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.action_project_dock.setText(_translate("MainWindow", "Project"))
        self.action_project_dock.setShortcut(_translate("MainWindow", "Alt+1"))
        self.action_tool_dock.setText(_translate("MainWindow", "Tools"))
        self.action_tool_dock.setShortcut(_translate("MainWindow", "Alt+2"))
        self.action_file_new.setText(_translate("MainWindow", "New Project..."))
        self.action_file_new.setShortcut(_translate("MainWindow", "Ctrl+Shift+N"))
        self.action_file_open.setText(_translate("MainWindow", "Open Project"))
        self.action_file_open.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))
        self.action_file_save.setText(_translate("MainWindow", "Save Project"))
        self.action_file_save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_add_flight.setText(_translate("MainWindow", "Add Flight"))
        self.action_add_flight.setShortcut(_translate("MainWindow", "Ctrl+Shift+F"))
        self.action_add_meter.setText(_translate("MainWindow", "Add Meter"))
        self.action_add_meter.setShortcut(_translate("MainWindow", "Ctrl+Shift+M"))
        self.action_project_info.setText(_translate("MainWindow", "Project Info..."))
        self.action_project_info.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.action_info_dock.setText(_translate("MainWindow", "Console"))
        self.action_info_dock.setShortcut(_translate("MainWindow", "Alt+3"))
        self.action_import_gps.setText(_translate("MainWindow", "Import GPS"))
        self.action_import_grav.setText(_translate("MainWindow", "Import Gravity"))

from dgp.gui.widgets import TabWorkspace
from dgp import resources_rc
