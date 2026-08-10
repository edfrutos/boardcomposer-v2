import pytest
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QApplication, QDialog, QMenu

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _non_blocking_menu(monkeypatch, trigger_label: str | None = None):
    """QMenu.exec() opens a real (nested-event-loop) menu and blocks until
    something dismisses it — fine for interactive use, but there's no user
    to click it in a test, so it would hang forever. Monkeypatching
    QMenu.exec directly on the class doesn't intercept PySide6's dispatch
    (verified: it silently no-ops and the real exec() still runs) —
    subclassing and patching the *name* MainWindow's module resolves to
    does."""

    class _NonBlockingMenu(QMenu):
        def exec(self, pos=None):
            if trigger_label is not None:
                action = next(a for a in self.actions() if a.text() == trigger_label)
                action.trigger()
            return None

    monkeypatch.setattr("studio.main_window.QMenu", _NonBlockingMenu)


class _FakeEditDialog:
    def __init__(self, values):
        self._values = values

    def exec(self):
        return QDialog.DialogCode.Accepted

    def values(self):
        return self._values


def test_piece_context_menu_selects_the_clicked_piece(window, monkeypatch):
    _non_blocking_menu(monkeypatch)

    # The demo project's active piece selection starts empty; a menu on
    # P-002 (not previously selected) must still act on P-002.
    window._show_piece_context_menu("P-002", QPoint(10, 10))

    assert window.workspace.selection.current() == "P-002"


def test_piece_context_menu_edit_action_edits_the_clicked_piece(window, monkeypatch):
    _non_blocking_menu(monkeypatch, "Editar pieza…")
    # P-002 (520x360 in the demo project) sits at x=900 with P-003 starting
    # at x=1500 — up to 550 still clears that gap without overlapping it.
    monkeypatch.setattr(
        "studio.main_window.PieceDialog",
        lambda *a, **k: _FakeEditDialog(("P-002", 550, 360, "Demo", 19.0)),
    )

    window._show_piece_context_menu("P-002", QPoint(10, 10))

    project = window.services.projects.current_project
    piece = next(p for p in project.pieces if p.piece_id == "P-002")
    assert piece.length_mm == 550


def test_piece_context_menu_delete_action_removes_it_from_the_project(
    window, monkeypatch
):
    _non_blocking_menu(monkeypatch, "Eliminar del proyecto…")

    window._show_piece_context_menu("P-002", QPoint(10, 10))

    project = window.services.projects.current_project
    assert all(piece.piece_id != "P-002" for piece in project.pieces)


def test_board_context_menu_edit_action_edits_the_active_board(window, monkeypatch):
    board_id = window.workspace.active_board_id
    _non_blocking_menu(monkeypatch, "Editar tablero…")
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeEditDialog((board_id, 5000, 900, "Demo", 19.0)),
    )

    window._show_board_context_menu(QPoint(10, 10))

    project = window.services.projects.current_project
    board = next(b for b in project.boards if b.board_id == board_id)
    assert board.length_mm == 5000


def test_board_context_menu_delete_action_removes_the_active_board(window, monkeypatch):
    board_id = window.workspace.active_board_id
    _non_blocking_menu(monkeypatch, "Eliminar tablero…")

    window._show_board_context_menu(QPoint(10, 10))

    project = window.services.projects.current_project
    assert all(board.board_id != board_id for board in project.boards)


def test_delete_active_board_removes_it_and_unplaces_its_pieces(window):
    project = window.services.projects.current_project
    board_id = window.workspace.active_board_id
    piece_ids_on_board = [
        p.piece_id for p in project.placements if p.board_id == board_id
    ]
    assert piece_ids_on_board  # sanity: the demo board has placed pieces

    window._delete_active_board()

    project = window.services.projects.current_project
    assert all(board.board_id != board_id for board in project.boards)
    assert all(placement.board_id != board_id for placement in project.placements)
    remaining_piece_ids = {piece.piece_id for piece in project.pieces}
    assert set(piece_ids_on_board).issubset(remaining_piece_ids)


def test_delete_active_board_is_undoable(window):
    project = window.services.projects.current_project
    boards_before = [b.board_id for b in project.boards]
    placements_before = len(project.placements)

    window._delete_active_board()
    window.services.commands.undo()

    project = window.services.projects.current_project
    assert [b.board_id for b in project.boards] == boards_before
    assert len(project.placements) == placements_before
