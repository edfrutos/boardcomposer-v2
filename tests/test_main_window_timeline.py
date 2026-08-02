import pytest
from PySide6.QtWidgets import QApplication, QDialog

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


class _FakeDialog:
    def __init__(self, values, accepted=True, quantity=1):
        self._values = values
        self._accepted = accepted
        self._quantity = quantity

    def exec(self):
        code = (
            QDialog.DialogCode.Accepted
            if self._accepted
            else QDialog.DialogCode.Rejected
        )
        return code

    def values(self):
        return self._values

    def quantity(self):
        return self._quantity


def test_timeline_overview_lists_the_demo_projects_board(window):
    assert "TAB-001" in window.timeline_overview.toPlainText()


def test_adding_a_board_refreshes_the_timeline_overview(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0)),
    )

    window._add_board()

    assert "B2" in window.timeline_overview.toPlainText()


def test_adding_a_board_logs_it_to_the_activity_tab(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0)),
    )
    assert "Sin actividad" in window.timeline_activity.toPlainText()

    window._add_board()

    activity_text = window.timeline_activity.toPlainText()
    assert "Tablero añadido" in activity_text
    assert "B2" in activity_text
    assert "B2" in window.services.activity.entries[0].message
    assert window.services.activity.entries[0].category == "tablero"


def test_activity_filter_shows_only_the_selected_category(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0)),
    )
    window._add_board()
    window._undo()

    index = window.timeline_activity_filter.findData("tablero")
    window.timeline_activity_filter.setCurrentIndex(index)

    activity_text = window.timeline_activity.toPlainText()
    assert "Tablero añadido" in activity_text
    assert "Deshecho" not in activity_text


def test_undo_logs_to_the_activity_tab(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0)),
    )
    window._add_board()

    window._undo()

    assert "Deshecho" in window.timeline_activity.toPlainText()


def test_undo_refreshes_the_explorer(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0)),
    )
    window._add_board()

    window._undo()

    root = window.explorer.topLevelItem(0)
    boards_root = next(
        root.child(i)
        for i in range(root.childCount())
        if root.child(i).text(0) == "Tableros"
    )
    board_texts = [
        boards_root.child(i).text(0) for i in range(boards_root.childCount())
    ]
    assert not any(text.startswith("B2") for text in board_texts)
