import pytest
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox

from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _write_csv(tmp_path, content: str):
    path = tmp_path / "tableros.csv"
    path.write_text(content, encoding="utf-8")
    return str(path)


def _patch_open_dialog(monkeypatch, path: str):
    monkeypatch.setattr(
        "studio.main_window.QFileDialog.getOpenFileName",
        staticmethod(lambda *a, **k: (path, "CSV (*.csv)")),
    )


def _patch_preview_dialog(monkeypatch, *, accept: bool = True):
    code = QDialog.DialogCode.Accepted if accept else QDialog.DialogCode.Rejected
    monkeypatch.setattr(
        "studio.main_window.BoardCsvImportPreviewDialog.exec", lambda self: code
    )


def test_import_boards_csv_adds_boards_to_the_project(window, monkeypatch, tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nT-101,1200,600,19\nT-102,800,400,16\n",
    )
    _patch_open_dialog(monkeypatch, path)
    _patch_preview_dialog(monkeypatch)
    project = window.services.projects.current_project
    boards_before = len(project.boards)

    window._import_boards_csv()

    assert len(project.boards) == boards_before + 2
    imported = {board.board_id for board in project.boards}
    assert {"T-101", "T-102"} <= imported


def test_import_boards_csv_is_undoable_board_by_board(window, monkeypatch, tmp_path):
    path = _write_csv(
        tmp_path, "id,length_mm,width_mm,thickness_mm\nT-101,1200,600,19\n"
    )
    _patch_open_dialog(monkeypatch, path)
    _patch_preview_dialog(monkeypatch)
    project = window.services.projects.current_project
    boards_before = len(project.boards)

    window._import_boards_csv()
    window._undo()

    assert len(project.boards) == boards_before


def test_import_boards_csv_with_a_bad_file_leaves_the_project_untouched(
    window, monkeypatch, tmp_path
):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nT-101,1200,600,19\nT-101,800,400,19\n",
    )
    _patch_open_dialog(monkeypatch, path)
    warnings = []
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *a, **k: warnings.append(a) or None
    )
    project = window.services.projects.current_project
    boards_before = len(project.boards)

    window._import_boards_csv()

    assert len(project.boards) == boards_before
    assert len(warnings) == 1


def test_import_boards_csv_rejects_ids_already_in_the_project(
    window, monkeypatch, tmp_path
):
    project = window.services.projects.current_project
    existing_id = project.boards[0].board_id
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm\n{existing_id},1200,600,19\n",
    )
    _patch_open_dialog(monkeypatch, path)
    monkeypatch.setattr(QMessageBox, "warning", lambda *a, **k: None)
    boards_before = len(project.boards)

    window._import_boards_csv()

    assert len(project.boards) == boards_before


def test_import_boards_csv_cancelled_dialog_does_nothing(window, monkeypatch):
    _patch_open_dialog(monkeypatch, "")
    project = window.services.projects.current_project
    boards_before = len(project.boards)

    window._import_boards_csv()

    assert len(project.boards) == boards_before


def test_import_boards_csv_rejected_preview_does_not_commit_anything(
    window, monkeypatch, tmp_path
):
    path = _write_csv(
        tmp_path, "id,length_mm,width_mm,thickness_mm\nT-101,1200,600,19\n"
    )
    _patch_open_dialog(monkeypatch, path)
    _patch_preview_dialog(monkeypatch, accept=False)
    project = window.services.projects.current_project
    boards_before = len(project.boards)

    window._import_boards_csv()

    assert len(project.boards) == boards_before
    assert "T-101" not in {board.board_id for board in project.boards}


def test_import_boards_csv_without_a_project_warns_and_never_opens_the_dialog(
    window, monkeypatch
):
    window.services.projects.close_project()
    warnings = []
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *a, **k: warnings.append(a) or None
    )
    dialog_calls = []
    monkeypatch.setattr(
        "studio.main_window.QFileDialog.getOpenFileName",
        staticmethod(lambda *a, **k: dialog_calls.append(1) or ("", "")),
    )

    window._import_boards_csv()

    assert len(warnings) == 1
    assert dialog_calls == []
