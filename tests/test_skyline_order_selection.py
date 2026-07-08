from boardcomposer import Board, Project

from boardcomposer.solver.skyline_runner import _candidate_orders


def test_candidate_orders():

    project = Project()

    project.add_board(Board(1000, 300, 20, "A"))

    project.add_board(Board(2500, 600, 20, "B"))

    names = [name for name, _ in _candidate_orders(project)]

    assert names == ["original", "largest_area", "longest_edge"]
