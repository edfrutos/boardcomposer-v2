"""Pytest-wide setup.

Some tests instantiate real Qt objects (QPainter, QPdfWriter) that abort
if no QGuiApplication exists yet. Force the offscreen platform plugin
before PySide6 is imported anywhere, so these tests run headlessly both
locally and in CI (GitHub Actions runners have no display server).
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QMessageBox


@pytest.fixture(autouse=True)
def _isolate_qsettings(tmp_path):
    """MainWindow persists the last opened/saved project path via QSettings
    (IDE-00xx). Without this, every test constructing a MainWindow would
    read/write the developer's REAL settings file — polluting every test
    that assumes the demo project loads with whatever real project was
    last open on that machine, and leaking state between test runs.
    Points QSettings at a fresh temp directory for each test instead."""
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(
        QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(tmp_path)
    )


@pytest.fixture(autouse=True)
def _no_modal_message_boxes(monkeypatch):
    """Turns the static QMessageBox helpers into no-ops for every test.

    A modal box blocks its own event loop, so a single unexpected one (an
    error path a test didn't anticipate, e.g. _open_project rejecting a
    file) hangs the whole run until the timeout instead of failing — which
    is unusable in CI. Tests that care about a specific dialog still
    monkeypatch it themselves; those patches are applied after this fixture
    and win.
    """
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *a, **k: QMessageBox.StandardButton.Ok
    )
    monkeypatch.setattr(
        QMessageBox, "critical", lambda *a, **k: QMessageBox.StandardButton.Ok
    )
    monkeypatch.setattr(
        QMessageBox, "information", lambda *a, **k: QMessageBox.StandardButton.Ok
    )
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Discard
    )
