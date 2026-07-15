from studio.commands import (
    AddBoardCommand,
    AddPieceCommand,
    EditBoardCommand,
    EditPieceCommand,
)
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices


def _services_with_project(**project_kwargs) -> StudioServices:
    services = StudioServices()
    project = StudioProject(project_id="proj-1", name="Demo", **project_kwargs)
    services.projects.new_project(project)
    return services


def test_add_board_command_appends_the_board():
    services = _services_with_project()
    board = StudioBoard("B1", 2000, 300)
    command = AddBoardCommand(services, board)

    command.execute()

    assert services.projects.current_project.boards == [board]


def test_add_board_command_undo_removes_it():
    services = _services_with_project()
    board = StudioBoard("B1", 2000, 300)
    command = AddBoardCommand(services, board)
    command.execute()

    command.undo()

    assert services.projects.current_project.boards == []


def test_add_board_command_redo_reapplies_it():
    services = _services_with_project()
    board = StudioBoard("B1", 2000, 300)
    command = AddBoardCommand(services, board)
    command.execute()
    command.undo()

    command.redo()

    assert services.projects.current_project.boards == [board]


def test_edit_board_command_replaces_the_board():
    old_board = StudioBoard("B1", 2000, 300)
    services = _services_with_project(boards=[old_board])
    new_board = StudioBoard("B1", 2500, 400)
    command = EditBoardCommand(services, old_board, new_board)

    command.execute()

    assert services.projects.current_project.boards == [new_board]


def test_edit_board_command_undo_restores_the_old_board():
    old_board = StudioBoard("B1", 2000, 300)
    services = _services_with_project(boards=[old_board])
    new_board = StudioBoard("B1", 2500, 400)
    command = EditBoardCommand(services, old_board, new_board)
    command.execute()

    command.undo()

    assert services.projects.current_project.boards == [old_board]


def test_add_piece_command_appends_the_piece_and_an_initial_placement():
    services = _services_with_project()
    piece = StudioPiece("p1", 500, 200)
    placement = StudioPlacement("p1", 0, 0, board_id="B1")
    command = AddPieceCommand(services, piece, placement)

    command.execute()

    project = services.projects.current_project
    assert project.pieces == [piece]
    assert project.placements == [placement]


def test_add_piece_command_undo_removes_both():
    services = _services_with_project()
    piece = StudioPiece("p1", 500, 200)
    placement = StudioPlacement("p1", 0, 0, board_id="B1")
    command = AddPieceCommand(services, piece, placement)
    command.execute()

    command.undo()

    project = services.projects.current_project
    assert project.pieces == []
    assert project.placements == []


def test_edit_piece_command_replaces_the_piece():
    old_piece = StudioPiece("p1", 500, 200)
    services = _services_with_project(pieces=[old_piece])
    new_piece = StudioPiece("p1", 600, 250)
    command = EditPieceCommand(services, old_piece, new_piece)

    command.execute()

    assert services.projects.current_project.pieces == [new_piece]


def test_edit_piece_command_undo_restores_the_old_piece():
    old_piece = StudioPiece("p1", 500, 200)
    services = _services_with_project(pieces=[old_piece])
    new_piece = StudioPiece("p1", 600, 250)
    command = EditPieceCommand(services, old_piece, new_piece)
    command.execute()

    command.undo()

    assert services.projects.current_project.pieces == [old_piece]
