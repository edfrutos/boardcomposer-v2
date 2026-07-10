"""Pytest-wide setup.

Some tests instantiate real Qt objects (QPainter, QPdfWriter) that abort
if no QGuiApplication exists yet. Force the offscreen platform plugin
before PySide6 is imported anywhere, so these tests run headlessly both
locally and in CI (GitHub Actions runners have no display server).
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
