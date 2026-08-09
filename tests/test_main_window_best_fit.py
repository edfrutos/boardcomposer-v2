import pytest
from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_best_fit_distribution_places_pieces_and_updates_ui(window):
    window.services.projects.new_project(
        StudioProject(
            project_id="proj-1",
            name="Demo",
            boards=[
                StudioBoard("grande", 2000, 2000),
                StudioBoard("retal", 600, 300),
            ],
            pieces=[StudioPiece("p1", 500, 300)],
        )
    )

    window._apply_best_fit_distribution()

    project = window.services.projects.current_project
    assert project.placement_by_piece_id("p1").board_id == "retal"


def test_best_fit_distribution_without_a_project_shows_a_message(window, monkeypatch):
    window.services.projects.close_project()
    messages = []
    monkeypatch.setattr(
        window.statusBar(), "showMessage", lambda text, *a: messages.append(text)
    )

    window._apply_best_fit_distribution()

    assert len(messages) == 1


def test_best_fit_distribution_with_nothing_to_place_shows_a_message(
    window, monkeypatch
):
    window.services.projects.new_project(
        StudioProject(
            project_id="proj-2",
            name="Demo",
            boards=[StudioBoard("A", 2000, 300, thickness_mm=19.0)],
            pieces=[StudioPiece("p1", 500, 300, thickness_mm=25.0)],
        )
    )
    messages = []
    monkeypatch.setattr(
        window.statusBar(), "showMessage", lambda text, *a: messages.append(text)
    )

    window._apply_best_fit_distribution()

    assert len(messages) == 1
    project = window.services.projects.current_project
    assert project.placement_by_piece_id("p1") is None


def test_best_fit_distribution_with_no_matching_material_shows_a_message(
    window, monkeypatch
):
    window.services.projects.new_project(
        StudioProject(
            project_id="proj-2b",
            name="Demo",
            boards=[StudioBoard("A", 2000, 300, material="Roble")],
            pieces=[StudioPiece("p1", 500, 300, material="Pino")],
        )
    )
    messages = []
    monkeypatch.setattr(
        window.statusBar(), "showMessage", lambda text, *a: messages.append(text)
    )

    window._apply_best_fit_distribution()

    assert len(messages) == 1
    project = window.services.projects.current_project
    assert project.placement_by_piece_id("p1") is None


def test_best_fit_distribution_keeps_existing_placements_on_other_boards(window):
    window.services.projects.new_project(
        StudioProject(
            project_id="proj-3",
            name="Demo",
            boards=[
                StudioBoard("A", 1000, 300),
                StudioBoard("B", 1000, 300),
            ],
            pieces=[
                StudioPiece("hand-placed", 400, 300),
                StudioPiece("nueva", 400, 300),
            ],
        )
    )
    project = window.services.projects.current_project
    project.placements.append(StudioPlacement("hand-placed", 0, 0, board_id="B"))

    window._apply_best_fit_distribution()

    assert project.placement_by_piece_id("hand-placed").board_id == "B"
    assert project.placement_by_piece_id("nueva") is not None
