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


def test_add_board_appends_a_new_board_and_makes_it_active(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0)),
    )

    window._add_board()

    project = window.services.projects.current_project
    assert any(board.board_id == "B2" for board in project.boards)
    assert window.workspace.active_board_id == "B2"


def test_add_board_is_undoable(window, monkeypatch):
    boards_before = len(window.services.projects.current_project.boards)
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0)),
    )
    window._add_board()

    window.services.commands.undo()

    assert len(window.services.projects.current_project.boards) == boards_before


def test_add_board_rejects_a_duplicate_id(window, monkeypatch):
    existing_id = window.services.projects.current_project.boards[0].board_id
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog((existing_id, 1000, 1000, "Demo", 19.0)),
    )

    window._add_board()

    assert len(window.services.projects.current_project.boards) == 1


def test_add_board_does_nothing_when_the_dialog_is_cancelled(window, monkeypatch):
    boards_before = len(window.services.projects.current_project.boards)
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0), accepted=False),
    )

    window._add_board()

    assert len(window.services.projects.current_project.boards) == boards_before


def test_add_board_with_a_quantity_creates_several_boards(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog(("B2", 1500, 400, "Demo", 19.0), quantity=3),
    )

    window._add_board()

    project = window.services.projects.current_project
    ids = {board.board_id for board in project.boards}
    assert {"B2", "B2-2", "B2-3"} <= ids


def test_edit_board_replaces_the_active_boards_dimensions(window, monkeypatch):
    board_id = window.workspace.active_board_id
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeDialog((board_id, 5000, 900, "Demo", 19.0)),
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
        lambda *a, **k: _FakeDialog(("p-new", 300, 150, "Demo", 19.0)),
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
        lambda *a, **k: _FakeDialog((existing_id, 300, 150, "Demo", 19.0)),
    )

    window._add_piece()

    assert len(window.services.projects.current_project.pieces) == pieces_before


def test_add_piece_with_a_quantity_creates_several_pieces_all_placed(
    window, monkeypatch
):
    active_board_id = window.workspace.active_board_id
    monkeypatch.setattr(
        "studio.main_window.PieceDialog",
        lambda *a, **k: _FakeDialog(("p-new", 300, 150, "Demo", 19.0), quantity=3),
    )

    window._add_piece()

    project = window.services.projects.current_project
    ids = {piece.piece_id for piece in project.pieces}
    assert {"p-new", "p-new-2", "p-new-3"} <= ids
    for piece_id in ("p-new", "p-new-2", "p-new-3"):
        placement = project.placement_by_piece_id(piece_id)
        assert placement is not None
        assert placement.board_id == active_board_id


def test_edit_piece_requires_a_selection(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.PieceDialog",
        lambda *a, **k: _FakeDialog(("P-001", 999, 999, "Demo", 19.0)),
    )

    window._edit_piece()

    project = window.services.projects.current_project
    piece = next(p for p in project.pieces if p.piece_id == "P-001")
    assert piece.length_mm != 999


def test_edit_piece_replaces_the_selected_pieces_dimensions(window, monkeypatch):
    window.workspace.selection.select_many(["P-001"])
    monkeypatch.setattr(
        "studio.main_window.PieceDialog",
        lambda *a, **k: _FakeDialog(("P-001", 800, 400, "Demo", 19.0)),
    )

    window._edit_piece()

    project = window.services.projects.current_project
    piece = next(p for p in project.pieces if p.piece_id == "P-001")
    assert piece.length_mm == 800
    assert piece.width_mm == 400


def _explorer_piece_texts(window) -> list[str]:
    root = window.explorer.topLevelItem(0)
    pieces_root = next(
        root.child(i)
        for i in range(root.childCount())
        if root.child(i).text(0) == "Piezas"
    )
    return [pieces_root.child(i).text(0) for i in range(pieces_root.childCount())]


def test_delete_selected_piece_removes_it_from_the_explorer(window):
    window.workspace.selection.select_many(["P-001"])

    window._delete_selected_piece()

    assert not any(text.startswith("P-001") for text in _explorer_piece_texts(window))


class _FakeMoveDialog:
    def __init__(self, board_id, accepted=True):
        self._board_id = board_id
        self._accepted = accepted

    def exec(self):
        return (
            QDialog.DialogCode.Accepted
            if self._accepted
            else QDialog.DialogCode.Rejected
        )

    def selected_board_id(self):
        return self._board_id


def test_move_piece_to_board_reassigns_the_placement(window, monkeypatch):
    project = window.services.projects.current_project
    from studio.models import StudioBoard

    project.boards.append(StudioBoard("TAB-002", 1000, 500))
    window.workspace.selection.select_many(["P-001"])
    monkeypatch.setattr(
        "studio.main_window.MoveToBoardDialog",
        lambda *a, **k: _FakeMoveDialog("TAB-002"),
    )

    window._move_piece_to_board()

    placement = project.placement_by_piece_id("P-001")
    assert placement.board_id == "TAB-002"


def test_move_piece_to_board_requires_a_selection(window, monkeypatch):
    project = window.services.projects.current_project
    from studio.models import StudioBoard

    project.boards.append(StudioBoard("TAB-002", 1000, 500))
    monkeypatch.setattr(
        "studio.main_window.MoveToBoardDialog",
        lambda *a, **k: _FakeMoveDialog("TAB-002"),
    )

    window._move_piece_to_board()

    placement = project.placement_by_piece_id("P-001")
    assert placement.board_id == "TAB-001"


def test_move_piece_to_board_with_a_single_board_shows_a_message(window, monkeypatch):
    window.workspace.selection.select_many(["P-001"])

    window._move_piece_to_board()

    placement = window.services.projects.current_project.placement_by_piece_id("P-001")
    assert placement.board_id == "TAB-001"
    assert "otro tablero" in window.statusBar().currentMessage()


def test_move_piece_to_board_rejects_a_different_thickness(window, monkeypatch):
    project = window.services.projects.current_project
    from studio.models import StudioBoard

    project.boards.append(StudioBoard("TAB-002", 3000, 1000, thickness_mm=25.0))
    window.workspace.selection.select_many(["P-001"])
    monkeypatch.setattr(
        "studio.main_window.MoveToBoardDialog",
        lambda *a, **k: _FakeMoveDialog("TAB-002"),
    )

    window._move_piece_to_board()

    placement = project.placement_by_piece_id("P-001")
    assert placement.board_id == "TAB-001"
    assert "grosor" in window.statusBar().currentMessage()


def test_move_piece_to_board_rejects_a_piece_that_no_longer_fits(window, monkeypatch):
    project = window.services.projects.current_project
    from studio.models import StudioBoard

    # P-001 is 700x300 at (120, 120) — doesn't fit an 500x400 board.
    project.boards.append(StudioBoard("TAB-002", 500, 400))
    window.workspace.selection.select_many(["P-001"])
    monkeypatch.setattr(
        "studio.main_window.MoveToBoardDialog",
        lambda *a, **k: _FakeMoveDialog("TAB-002"),
    )

    window._move_piece_to_board()

    placement = project.placement_by_piece_id("P-001")
    assert placement.board_id == "TAB-001"
    assert "no cabe" in window.statusBar().currentMessage()


def test_move_piece_to_board_rejects_an_overlap_with_an_existing_piece(
    window, monkeypatch
):
    project = window.services.projects.current_project
    from studio.models import StudioBoard, StudioPiece, StudioPlacement

    project.boards.append(StudioBoard("TAB-002", 3000, 1000))
    # Same position/size P-001 would keep when moved — guaranteed overlap.
    project.pieces.append(StudioPiece("P-999", 700, 300))
    project.placements.append(StudioPlacement("P-999", 120, 120, board_id="TAB-002"))
    window.workspace.selection.select_many(["P-001"])
    monkeypatch.setattr(
        "studio.main_window.MoveToBoardDialog",
        lambda *a, **k: _FakeMoveDialog("TAB-002"),
    )

    window._move_piece_to_board()

    placement = project.placement_by_piece_id("P-001")
    assert placement.board_id == "TAB-001"
    assert "no cabe" in window.statusBar().currentMessage()


class _FakeKerfDialog:
    def __init__(self, kerf_mm, accepted=True):
        self._kerf_mm = kerf_mm
        self._accepted = accepted

    def exec(self):
        return (
            QDialog.DialogCode.Accepted
            if self._accepted
            else QDialog.DialogCode.Rejected
        )

    def kerf_mm(self):
        return self._kerf_mm


def test_configure_kerf_updates_the_project(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.KerfDialog", lambda *a, **k: _FakeKerfDialog(3.5)
    )

    window._configure_kerf()

    assert window.services.projects.current_project.kerf_mm == 3.5


def test_configure_kerf_is_undoable(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.KerfDialog", lambda *a, **k: _FakeKerfDialog(3.5)
    )
    window._configure_kerf()

    window.services.commands.undo()

    assert window.services.projects.current_project.kerf_mm == 0.0


def test_configure_kerf_does_nothing_when_cancelled(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.KerfDialog",
        lambda *a, **k: _FakeKerfDialog(3.5, accepted=False),
    )

    window._configure_kerf()

    assert window.services.projects.current_project.kerf_mm == 0.0
