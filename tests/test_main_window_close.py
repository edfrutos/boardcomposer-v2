import pytest
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_close_without_changes_accepts_immediately(window, monkeypatch):
    # A freshly-loaded demo project is always "modified" (new_project() has
    # no associated file yet) — mark it saved first to get a clean slate.
    window.services.projects.open_project(
        window.services.projects.current_project, filename="/tmp/demo.bcstudio.json"
    )
    called = []
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: called.append(1) or None
    )

    event = QCloseEvent()
    window.closeEvent(event)

    assert event.isAccepted()
    assert called == []


def test_close_with_changes_cancel_ignores_close(window, monkeypatch):
    window.services.projects.mark_modified()
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Cancel
    )

    event = QCloseEvent()
    window.closeEvent(event)

    assert not event.isAccepted()


def test_close_with_changes_discard_accepts_without_saving(window, monkeypatch):
    window.services.projects.mark_modified()
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Discard
    )

    event = QCloseEvent()
    window.closeEvent(event)

    assert event.isAccepted()
    assert window.services.projects.is_modified is True


def test_close_with_changes_save_writes_file_and_accepts(window, monkeypatch, tmp_path):
    path = str(tmp_path / "demo.bcstudio.json")
    window.services.projects.open_project(
        window.services.projects.current_project, filename=path
    )
    window.services.projects.mark_modified()
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Save
    )

    event = QCloseEvent()
    window.closeEvent(event)

    assert event.isAccepted()
    assert window.services.projects.is_modified is False
    assert (tmp_path / "demo.bcstudio.json").exists()


def test_close_with_changes_save_cancelled_dialog_ignores_close(
    window, monkeypatch, tmp_path
):
    window.services.projects.mark_modified()
    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Save
    )
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *a, **k: ("", ""))

    event = QCloseEvent()
    window.closeEvent(event)

    assert not event.isAccepted()
    assert window.services.projects.is_modified is True
