import pytest
from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _open_project(window, project):
    window.services.projects.new_project(project)
    window.workspace.reload_project()
    window.workspace.set_active_board(project.boards[0].board_id)


def test_rotate_selected_piece_rotates_in_place_when_there_is_room(window):
    project = StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("B1", 600, 600)],
        pieces=[StudioPiece("p1", 200, 100)],
        placements=[StudioPlacement("p1", 0, 0, board_id="B1")],
    )
    _open_project(window, project)
    window.workspace.selection.select_many(["p1"])

    window._rotate_selected_piece()

    placement = window.services.projects.current_project.placement_by_piece_id("p1")
    assert placement.rotation == 90
    assert (placement.x_mm, placement.y_mm) == (0, 0)


def test_rotate_selected_piece_repositions_when_in_place_would_collide(window):
    # p1 (200x100) sits right above p2 (300x300) — rotating p1 in place grows
    # its height from 100 to 200, reaching straight into p2. B1 is large
    # enough to have free space elsewhere for the rotated piece.
    project = StudioProject(
        project_id="proj-2",
        name="Demo",
        boards=[StudioBoard("B1", 600, 600)],
        pieces=[StudioPiece("p1", 200, 100), StudioPiece("p2", 300, 300)],
        placements=[
            StudioPlacement("p1", 0, 0, board_id="B1"),
            StudioPlacement("p2", 0, 100, board_id="B1"),
        ],
    )
    _open_project(window, project)
    window.workspace.selection.select_many(["p1"])

    window._rotate_selected_piece()

    placement = window.services.projects.current_project.placement_by_piece_id("p1")
    assert placement.rotation == 90
    assert (placement.x_mm, placement.y_mm) != (0, 0)


def test_rotate_selected_piece_rejects_when_no_free_space_exists(window):
    # p1 fills the entire board exactly — rotated (100x200) doesn't fit a
    # 200x100 board in any position, in place or otherwise.
    project = StudioProject(
        project_id="proj-3",
        name="Demo",
        boards=[StudioBoard("B1", 200, 100)],
        pieces=[StudioPiece("p1", 200, 100)],
        placements=[StudioPlacement("p1", 0, 0, board_id="B1")],
    )
    _open_project(window, project)
    window.workspace.selection.select_many(["p1"])

    window._rotate_selected_piece()

    placement = window.services.projects.current_project.placement_by_piece_id("p1")
    assert placement.rotation == 0
    assert "hueco libre" in window.statusBar().currentMessage()
