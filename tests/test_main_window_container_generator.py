import pytest
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _patch_generator_dialog(monkeypatch, *, accept: bool = True, **values):
    code = QDialog.DialogCode.Accepted if accept else QDialog.DialogCode.Rejected
    monkeypatch.setattr(
        "studio.main_window.ContainerGeneratorDialog.exec", lambda self: code
    )
    defaults = {
        "outer_length_mm": 300.0,
        "outer_width_mm": 200.0,
        "outer_height_mm": 100.0,
        "thickness_mm": 18.0,
        "material": "Demo",
        "id_prefix": "caja",
    }
    defaults.update(values)
    monkeypatch.setattr(
        "studio.main_window.ContainerGeneratorDialog.values",
        lambda self: defaults,
    )
    monkeypatch.setattr(
        "studio.main_window.ContainerGeneratorDialog.template_key",
        lambda self: "caja_simple",
    )


def _patch_preview_dialog(monkeypatch, *, accept: bool = True):
    code = QDialog.DialogCode.Accepted if accept else QDialog.DialogCode.Rejected
    monkeypatch.setattr(
        "studio.main_window.CsvImportPreviewDialog.exec", lambda self: code
    )


def test_generates_five_pieces_on_the_active_board(window, monkeypatch):
    _patch_generator_dialog(monkeypatch)
    _patch_preview_dialog(monkeypatch)
    project = window.services.projects.current_project
    active_board_id = window.workspace.active_board_id
    pieces_before = len(project.pieces)

    window._generate_container_pieces()

    assert len(project.pieces) == pieces_before + 5
    generated_ids = {
        "caja-base",
        "caja-pared-frontal",
        "caja-pared-trasera",
        "caja-lateral-izquierdo",
        "caja-lateral-derecho",
    }
    assert generated_ids <= {piece.piece_id for piece in project.pieces}
    placements = {
        placement.piece_id: placement.board_id for placement in project.placements
    }
    for piece_id in generated_ids:
        assert placements[piece_id] == active_board_id


def test_generation_is_undoable_piece_by_piece(window, monkeypatch):
    _patch_generator_dialog(monkeypatch)
    _patch_preview_dialog(monkeypatch)
    project = window.services.projects.current_project
    pieces_before = len(project.pieces)

    window._generate_container_pieces()
    window._undo()

    assert len(project.pieces) == pieces_before + 4


def test_invalid_dimensions_warn_and_add_nothing(window, monkeypatch):
    _patch_generator_dialog(monkeypatch, outer_width_mm=30.0)
    warnings = []
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *a, **k: warnings.append(a) or None
    )
    project = window.services.projects.current_project
    pieces_before = len(project.pieces)

    window._generate_container_pieces()

    assert len(project.pieces) == pieces_before
    assert len(warnings) == 1


def test_rejected_preview_does_not_commit_anything(window, monkeypatch):
    _patch_generator_dialog(monkeypatch)
    _patch_preview_dialog(monkeypatch, accept=False)
    project = window.services.projects.current_project
    pieces_before = len(project.pieces)

    window._generate_container_pieces()

    assert len(project.pieces) == pieces_before


def test_cancelled_dialog_does_nothing(window, monkeypatch):
    _patch_generator_dialog(monkeypatch, accept=False)
    project = window.services.projects.current_project
    pieces_before = len(project.pieces)

    window._generate_container_pieces()

    assert len(project.pieces) == pieces_before


def test_generates_five_pieces_for_drawer_no_rails_template(window, monkeypatch):
    code = QDialog.DialogCode.Accepted
    monkeypatch.setattr(
        "studio.main_window.ContainerGeneratorDialog.exec", lambda self: code
    )
    monkeypatch.setattr(
        "studio.main_window.ContainerGeneratorDialog.values",
        lambda self: {
            "opening_length_mm": 300.0,
            "opening_height_mm": 100.0,
            "depth_mm": 200.0,
            "clearance_mm": 1.5,
            "thickness_mm": 18.0,
            "material": "Demo",
            "id_prefix": "cajon",
        },
    )
    monkeypatch.setattr(
        "studio.main_window.ContainerGeneratorDialog.template_key",
        lambda self: "cajon_sin_rieles",
    )
    _patch_preview_dialog(monkeypatch)
    project = window.services.projects.current_project
    pieces_before = len(project.pieces)

    window._generate_container_pieces()

    assert len(project.pieces) == pieces_before + 5
    assert "cajon-base" in {piece.piece_id for piece in project.pieces}


def test_without_a_board_warns_and_never_opens_the_dialog(window, monkeypatch):
    window._new_project()
    warnings = []
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *a, **k: warnings.append(a) or None
    )
    dialog_calls = []
    monkeypatch.setattr(
        "studio.main_window.ContainerGeneratorDialog.__init__",
        lambda self, *a, **k: dialog_calls.append(1),
    )

    window._generate_container_pieces()

    assert len(warnings) == 1
    assert dialog_calls == []
