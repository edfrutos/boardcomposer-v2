from boardcomposer import Board
from boardcomposer.solver.board_ordering import (
    largest_area_first,
    longest_edge_first,
    original_order,
)


def test_original_order():
    boards = [
        Board(1000, 300, 20, "B"),
        Board(2500, 600, 20, "A"),
    ]

    assert [board.id for board in original_order(boards)] == ["B", "A"]


def test_largest_area_first():
    boards = [
        Board(1000, 300, 20, "B"),
        Board(2500, 600, 20, "A"),
        Board(800, 250, 20, "C"),
    ]

    assert [board.id for board in largest_area_first(boards)] == ["A", "B", "C"]


def test_longest_edge_first():
    boards = [
        Board(1000, 300, 20, "B"),
        Board(2500, 200, 20, "A"),
        Board(800, 800, 20, "C"),
    ]

    assert [board.id for board in longest_edge_first(boards)] == ["A", "B", "C"]
