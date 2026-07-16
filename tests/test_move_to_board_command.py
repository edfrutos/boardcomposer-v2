from studio.commands import MoveToBoardCommand
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


def _services_with_piece_on_board_a() -> StudioServices:
    services = StudioServices()
    project = StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300), StudioBoard("B", 1000, 300)],
        pieces=[StudioPiece("p1", 500, 200)],
        placements=[StudioPlacement("p1", 0, 0, board_id="A")],
    )
    services.projects.new_project(project)
    return services


def test_move_to_board_command_reassigns_the_placement():
    services = _services_with_piece_on_board_a()
    command = MoveToBoardCommand(services, "p1", "A", "B")

    command.redo()

    placement = services.projects.current_project.placement_by_piece_id("p1")
    assert placement.board_id == "B"


def test_move_to_board_command_undo_restores_the_old_board():
    services = _services_with_piece_on_board_a()
    command = MoveToBoardCommand(services, "p1", "A", "B")
    command.redo()

    command.undo()

    placement = services.projects.current_project.placement_by_piece_id("p1")
    assert placement.board_id == "A"
