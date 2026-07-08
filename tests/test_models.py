import pytest

from boardcomposer import Board, Project


def test_board_area():
    board = Board(length_mm=2000, width_mm=300, thickness_mm=20)
    assert board.area_mm2 == 600000


def test_board_requires_positive_dimensions():
    with pytest.raises(ValueError):
        Board(length_mm=0, width_mm=300, thickness_mm=20)


def test_project_total_area():
    project = Project()
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20))
    project.add_board(Board(length_mm=1000, width_mm=200, thickness_mm=20))

    assert project.total_area_mm2 == 800000
