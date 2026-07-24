from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from studio.main_window import LAST_PROJECT_PATH_SETTINGS_KEY, MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project.project_io import save_project_to_file
from studio.services import StudioServices


def _make_window() -> MainWindow:
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_starts_with_the_demo_project_when_nothing_was_ever_saved():
    window = _make_window()

    project = window.services.projects.current_project
    assert project.project_id == "PRJ-DEMO-001"


def test_opens_the_last_saved_project_instead_of_the_demo(tmp_path):
    saved_project = StudioProject(
        project_id="proj-real",
        name="Caja real",
        boards=[StudioBoard("TAB-001", 900, 490)],
    )
    path = tmp_path / "caja.bcstudio.json"
    save_project_to_file(saved_project, path)
    QSettings().setValue(LAST_PROJECT_PATH_SETTINGS_KEY, str(path))

    window = _make_window()

    project = window.services.projects.current_project
    assert project.project_id == "proj-real"
    assert project.name == "Caja real"
    assert window.services.projects.filename == str(path)


def test_falls_back_to_the_demo_when_the_last_project_no_longer_exists(tmp_path):
    QSettings().setValue(
        LAST_PROJECT_PATH_SETTINGS_KEY, str(tmp_path / "does-not-exist.bcstudio.json")
    )

    window = _make_window()

    project = window.services.projects.current_project
    assert project.project_id == "PRJ-DEMO-001"


def test_falls_back_to_the_demo_when_the_last_project_is_corrupted(tmp_path):
    path = tmp_path / "corrupted.bcstudio.json"
    path.write_text("not valid json", encoding="utf-8")
    QSettings().setValue(LAST_PROJECT_PATH_SETTINGS_KEY, str(path))

    window = _make_window()

    project = window.services.projects.current_project
    assert project.project_id == "PRJ-DEMO-001"


def test_saving_a_new_project_remembers_its_path_for_next_launch(tmp_path, monkeypatch):
    window = _make_window()
    path = tmp_path / "guardado.bcstudio.json"
    monkeypatch.setattr(
        "studio.main_window.QFileDialog.getSaveFileName",
        lambda *a, **k: (str(path), ""),
    )

    window._save_project()

    assert QSettings().value(LAST_PROJECT_PATH_SETTINGS_KEY) == str(path)


def test_opening_a_project_remembers_its_path(tmp_path, monkeypatch):
    other_project = StudioProject(
        project_id="proj-other",
        name="Otro",
        pieces=[StudioPiece("p1", 100, 100)],
        placements=[StudioPlacement("p1", 0, 0, board_id="TAB-001")],
    )
    path = tmp_path / "otro.bcstudio.json"
    save_project_to_file(other_project, path)
    monkeypatch.setattr(
        "studio.main_window.QFileDialog.getOpenFileName",
        lambda *a, **k: (str(path), ""),
    )

    window = _make_window()
    window._open_project()

    assert QSettings().value(LAST_PROJECT_PATH_SETTINGS_KEY) == str(path)
