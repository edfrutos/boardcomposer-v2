from PySide6.QtWidgets import QApplication

from studio.activity_log import ACTIVITY_EVENT
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices
from studio.workspace.board_workspace import BoardWorkspace


def _services_with_two_boards() -> StudioServices:
    services = StudioServices()
    project = StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[
            StudioBoard("B1", 2000, 300),
            StudioBoard("B2", 1500, 400),
        ],
        pieces=[
            StudioPiece("p1", 500, 200),
            StudioPiece("p2", 400, 150),
        ],
        placements=[
            StudioPlacement("p1", 0, 0, board_id="B1"),
            StudioPlacement("p2", 0, 0, board_id="B2"),
        ],
    )
    services.projects.new_project(project)
    return services


def _workspace() -> BoardWorkspace:
    QApplication.instance() or QApplication([])
    return BoardWorkspace(_services_with_two_boards())


def test_reload_project_defaults_the_active_board_to_the_first_one():
    workspace = _workspace()

    workspace.reload_project()

    assert workspace.active_board_id == "B1"


def test_finish_piece_drag_publishes_to_the_activity_event_bus():
    # BoardWorkspace has no MainWindow reference — before this fix, a
    # freehand drag-move (the single most common piece-manipulation
    # gesture) called CommandManager.execute() directly and never reached
    # the Actividad log, unlike every dialog-driven mutation.
    workspace = _workspace()
    workspace.reload_project()

    messages = []
    workspace.services.events.subscribe(
        ACTIVITY_EVENT, lambda name, payload: messages.append(payload["message"])
    )

    item = workspace.piece_item_by_id("p1")
    workspace._drag.begin("p1", 0, 0)
    placement = workspace.services.projects.current_project.placement_by_piece_id("p1")
    placement.x_mm = 300
    placement.y_mm = 50
    item.setPos(300, 50)

    workspace._finish_piece_drag()

    assert messages == ["Pieza movida: p1"]


def test_reload_project_only_renders_pieces_placed_on_the_active_board():
    workspace = _workspace()

    workspace.reload_project()

    assert [item.piece_id for item in workspace._piece_items] == ["p1"]


def test_set_active_board_switches_to_the_other_board_and_its_pieces():
    workspace = _workspace()
    workspace.reload_project()

    workspace.set_active_board("B2")

    assert workspace.active_board_id == "B2"
    assert [item.piece_id for item in workspace._piece_items] == ["p2"]


def test_reload_project_falls_back_to_the_first_board_if_the_active_one_is_gone():
    workspace = _workspace()
    workspace.set_active_board("B2")
    project = workspace.services.projects.current_project
    project.boards = [board for board in project.boards if board.board_id != "B2"]

    workspace.reload_project()

    assert workspace.active_board_id == "B1"
