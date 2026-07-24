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
