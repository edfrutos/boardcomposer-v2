import pytest
from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _write_csv(tmp_path, content: str):
    path = tmp_path / "piezas.csv"
    path.write_text(content, encoding="utf-8")
    return str(path)


def _patch_open_dialog(monkeypatch, path: str):
    monkeypatch.setattr(
        "studio.main_window.QFileDialog.getOpenFileName",
        staticmethod(lambda *a, **k: (path, "CSV (*.csv)")),
    )


def test_import_csv_adds_pieces_to_the_active_board(window, monkeypatch, tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nP-101,700,300,19\nP-102,520,360,16\n",
    )
    _patch_open_dialog(monkeypatch, path)
    project = window.services.projects.current_project
    active_board_id = window.workspace.active_board_id
    pieces_before = len(project.pieces)

    window._import_pieces_csv()

    assert len(project.pieces) == pieces_before + 2
    imported = {piece.piece_id for piece in project.pieces}
    assert {"P-101", "P-102"} <= imported
    placements = {
        placement.piece_id: placement.board_id for placement in project.placements
    }
    assert placements["P-101"] == active_board_id
    assert placements["P-102"] == active_board_id


def test_import_csv_is_undoable_piece_by_piece(window, monkeypatch, tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nP-101,700,300,19\n",
    )
    _patch_open_dialog(monkeypatch, path)
    project = window.services.projects.current_project
    pieces_before = len(project.pieces)

    window._import_pieces_csv()
    window._undo()

    assert len(project.pieces) == pieces_before


def test_import_csv_with_a_bad_file_leaves_the_project_untouched(
    window, monkeypatch, tmp_path
):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nP-101,700,300,19\nP-101,520,360,19\n",
    )
    _patch_open_dialog(monkeypatch, path)
    project = window.services.projects.current_project
    pieces_before = len(project.pieces)

    window._import_pieces_csv()

    assert len(project.pieces) == pieces_before


def test_import_csv_rejects_ids_already_in_the_project(window, monkeypatch, tmp_path):
    project = window.services.projects.current_project
    existing_id = project.pieces[0].piece_id
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm\n{existing_id},700,300,19\n",
    )
    _patch_open_dialog(monkeypatch, path)
    pieces_before = len(project.pieces)

    window._import_pieces_csv()

    assert len(project.pieces) == pieces_before


def test_import_csv_cancelled_dialog_does_nothing(window, monkeypatch):
    _patch_open_dialog(monkeypatch, "")
    project = window.services.projects.current_project
    pieces_before = len(project.pieces)

    window._import_pieces_csv()

    assert len(project.pieces) == pieces_before
