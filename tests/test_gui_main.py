# -*- coding: utf-8 -*-

# Test gui/main.py
import logging
from pathlib import Path

import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QSignalSpy, QTest
from PyQt5.QtWidgets import QMainWindow, QProgressDialog, QPushButton

from dgp.core.oid import OID
from dgp.core.models.project import AirborneProject
from dgp.core.controllers.project_treemodel import ProjectTreeModel
from dgp.core.controllers.flight_controller import FlightController
from dgp.core.controllers.project_controllers import AirborneProjectController
from dgp.gui.main import MainWindow
from dgp.gui.dialogs.create_project_dialog import CreateProjectDialog
from dgp.gui.utils import ProgressEvent


@pytest.fixture
def window(project) -> MainWindow:
    window = MainWindow()
    window.add_project(project)
    yield window
    window.close()


def test_MainWindow_load(window, project):
    assert isinstance(window, QMainWindow)
    assert not window.isVisible()

    window.load(project)
    assert window.isVisible()
    assert not window.isWindowModified()

    window.close()
    assert not window.isVisible()


def test_MainWindow_tab_open_requested(project, window):
    assert isinstance(window.model, ProjectTreeModel)

    tab_open_spy = QSignalSpy(window.model.tabOpenRequested)
    assert 0 == len(tab_open_spy)
    assert 0 == window.workspace.count()

    flt_ctrl = window.model.active_project.get_child(project.flights[0].uid)

    assert isinstance(flt_ctrl, FlightController)
    assert window.workspace.get_tab(flt_ctrl.uid) is None

    window.model.item_activated(flt_ctrl.index())
    assert 1 == len(tab_open_spy)
    assert 1 == window.workspace.count()

    window.model.item_activated(flt_ctrl.index())
    assert 2 == len(tab_open_spy)
    assert 1 == window.workspace.count()


def test_MainWindow_project_mutated(window: MainWindow):
    assert not window.isWindowModified()
    window.model.projectMutated.emit()
    assert window.isWindowModified()
    window.save_projects()
    assert not window.isWindowModified()


def test_MainWindow_set_logging_level(window: MainWindow):
    # Test UI combo-box widget to change/set logging level
    assert logging.DEBUG == window.log.level

    index_level_map = {0: logging.DEBUG,
                       1: logging.INFO,
                       2: logging.WARNING,
                       3: logging.ERROR,
                       4: logging.CRITICAL}

    for index, level in index_level_map.items():
        window.combo_console_verbosity.setCurrentIndex(index)
        assert level == window.log.level


def test_MainWindow_new_project_dialog(window: MainWindow, tmpdir):
    assert 1 == window.model.rowCount()
    dest = Path(tmpdir)
    dest_str = str(dest.absolute().resolve())

    dlg: CreateProjectDialog = window.new_project_dialog()
    projectCreated_spy = QSignalSpy(dlg.sigProjectCreated)
    dlg.prj_name.setText("TestNewProject")
    dlg.prj_dir.setText(dest_str)
    dlg.accept()

    assert 1 == len(projectCreated_spy)
    assert 2 == window.model.rowCount()

    prj_dir = dest.joinpath(dlg.project.name)
    assert prj_dir.exists()


def test_MainWindow_open_project_dialog(window: MainWindow, project_factory, tmpdir):
    prj2: AirborneProject = project_factory("Proj2", tmpdir, dataset=False)
    prj2_ctrl = AirborneProjectController(prj2)
    prj2_ctrl.save()
    prj2_ctrl.hdfpath.touch(exist_ok=True)

    assert window.model.active_project.path != prj2_ctrl.path
    assert 1 == window.model.rowCount()

    window.open_project(path=prj2.path, prompt=False)
    assert 2 == window.model.rowCount()

    # Try to open an already open project
    window.open_project(path=prj2.path, prompt=False)
    assert 2 == window.model.rowCount()

    with pytest.raises(FileNotFoundError):
        window.open_project(path=Path(tmpdir), prompt=False)
    assert 2 == window.model.rowCount()


def test_MainWindow_progress_event_handler(project, window):
    model: ProjectTreeModel = window.model
    progressEventRequested_spy = QSignalSpy(model.progressNotificationRequested)

    flt_ctrl = window.model.active_project.get_child(project.flights[0].uid)

    prog_event = ProgressEvent(flt_ctrl.uid, label="Loading Data Set")
    assert flt_ctrl.uid == prog_event.uid
    assert not prog_event.completed
    assert 0 == prog_event.value

    model.progressNotificationRequested.emit(prog_event)
    assert 1 == len(progressEventRequested_spy)
    assert 1 == len(window._progress_events)
    assert flt_ctrl.uid in window._progress_events
    dlg = window._progress_events[flt_ctrl.uid]
    assert isinstance(dlg, QProgressDialog)
    assert dlg.isVisible()
    assert prog_event.label == dlg.labelText()
    assert 1 == dlg.value()

    prog_event2 = ProgressEvent(flt_ctrl.uid, label="Loading Data Set 2",
                                start=0, stop=100)
    prog_event2.value = 35
    model.progressNotificationRequested.emit(prog_event2)
    assert 2 == len(progressEventRequested_spy)

    assert dlg == window._progress_events[flt_ctrl.uid]
    assert prog_event2.label == dlg.labelText()
    assert prog_event2.value == dlg.value()

    prog_event2.value = 100
    assert prog_event2.completed
    model.progressNotificationRequested.emit(prog_event2)
    assert not dlg.isVisible()

    assert 0 == len(window._progress_events)

    model.progressNotificationRequested.emit(prog_event)
    assert 1 == len(window._progress_events)

    # Test progress bar with cancellation callback slot
    received = False

    def _receiver():
        nonlocal received
        received = True

    _uid = OID()
    prog_event_callback = ProgressEvent(_uid, "Testing Callback", receiver=_receiver)
    model.progressNotificationRequested.emit(prog_event_callback)

    dlg: QProgressDialog = window._progress_events[_uid]
    cancel = QPushButton("Cancel")
    dlg.setCancelButton(cancel)
    assert dlg.isVisible()
    QTest.mouseClick(cancel, Qt.LeftButton)

    assert received

