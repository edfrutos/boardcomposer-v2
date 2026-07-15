import pytest
from PySide6.QtWidgets import QApplication, QDialog

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


class _FakeDialog:
    def __init__(self, values, accepted=True):
        self._values = values
        self._accepted = accepted

    def exec(self):
        code = (
            QDialog.DialogCode.Accepted
            if self._accepted
            else QDialog.DialogCode.Rejected
        )
        return code

    def values(self):
        return self._values


def test_add_board_appends_a_new_board_and_makes_it_active(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.BoardDialog", lambda *a, **k: _FakeDialog(("B2", 1500, 400))
    )

    window._add_board()

    project = window.services.projects.current_project
    assert any(board.board_id == "B2" for board in project.boards)
    assert window.workspace.active_board_id == "B2"


def test_add_board_is_undoable(window, monkeypatch):
    boards_before = len(window.services.projects.current_project.boards)
    monkeypatch.setattr(
        "studio.main_window.BoardDialog", lambda *a, **k: _FakeDialog(("B2", 1500, 400))
    )
    window._add_board()

    window.services.commands.undo()

    assert len(window.services.projects.current_project.boards) == boards_before


def test_add_board_rejects_a_duplicate_id(window, monkeypatch):
    existing_id = window.services.projects.current_project.boards[0].board_id
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog((existing_id, 1000, 1000)),
    )

    window._add_board()

    assert len(window.services.projects.current_project.boards) == 1


def test_add_board_does_nothing_when_the_dialog_is_cancelled(window, monkeypatch):
    boards_before = len(window.services.projects.current_project.boards)
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400), accepted=False),
    )

    window._add_board()

    assert len(window.services.projects.current_project.boards) == boards_before


def test_edit_board_replaces_the_active_boards_dimensions(window, monkeypatch):
    board_id = window.workspace.active_board_id
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog((board_id, 5000, 900)),
    )

    window._edit_board()

    project = window.services.projects.current_project
    board = next(b for b in project.boards if b.board_id == board_id)
    assert board.length_mm == 5000
    assert board.width_mm == 900


def test_add_piece_appends_a_piece_visible_on_the_active_board(window, monkeypatch):
    active_board_id = window.workspace.active_board_id
    monkeypatch.setattr(
        "studio.main_window.PieceDialog",
        lambda *a, **k: _FakeDialog(("p-new", 300, 150)),
    )

    window._add_piece()

    project = window.services.projects.current_project
    assert any(piece.piece_id == "p-new" for piece in project.pieces)
    placement = project.placement_by_piece_id("p-new")
    assert placement is not None
    assert placement.board_id == active_board_id


def test_add_piece_rejects_a_duplicate_id(window, monkeypatch):
    existing_id = window.services.projects.current_project.pieces[0].piece_id
    pieces_before = len(window.services.projects.current_project.pieces)
    monkeypatch.setattr(
        "studio.main_window.PieceDialog",
        lambda *a, **k: _FakeDialog((existing_id, 300, 150)),
    )

    window._add_piece()

    assert len(window.services.projects.current_project.pieces) == pieces_before


def test_edit_piece_requires_a_selection(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.PieceDialog",
        lambda *a, **k: _FakeDialog(("P-001", 999, 999)),
    )

    window._edit_piece()

    project = window.services.projects.current_project
    piece = next(p for p in project.pieces if p.piece_id == "P-001")
    assert piece.length_mm != 999


def test_edit_piece_replaces_the_selected_pieces_dimensions(window, monkeypatch):
    window.workspace.selection.select_many(["P-001"])
    monkeypatch.setattr(
        "studio.main_window.PieceDialog",
        lambda *a, **k: _FakeDialog(("P-001", 800, 400)),
    )

    window._edit_piece()

    project = window.services.projects.current_project
    piece = next(p for p in project.pieces if p.piece_id == "P-001")
    assert piece.length_mm == 800
    assert piece.width_mm == 400
