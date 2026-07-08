from boardcomposer import Board
from boardcomposer.layout.free_space_manager import FreeSpaceManager
from boardcomposer.layout.placer import place_board_in_first_space


def test_place_board_in_first_space():
    manager = FreeSpaceManager.from_bounds(3000, 600)
    board = Board(2000, 300, 20, "A")

    placement = place_board_in_first_space(board, manager, "A")

    assert placement is not None
    assert placement.x_mm == 0
    assert placement.y_mm == 0
    assert placement.length_mm == 2000
    assert placement.width_mm == 300


def test_place_board_returns_none_when_no_space():
    manager = FreeSpaceManager.from_bounds(1000, 300)
    board = Board(2000, 300, 20, "A")

    placement = place_board_in_first_space(board, manager, "A")

    assert placement is None
