from boardcomposer import Board, Project
from boardcomposer.solver.layout_generator import generate_horizontal_permutations


def test_generate_horizontal_permutations():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = generate_horizontal_permutations(project)

    assert len(solutions) == 2
    assert {s.placements[0].board_id for s in solutions} == {"A", "B"}


def test_horizontal_permutations_fallback_when_too_many_boards():

    project = Project()

    for index in range(7):
        project.add_board(Board(1000, 200, 20, f"B{index}"))

    solutions = generate_horizontal_permutations(project)

    assert len(solutions) == 1

    assert solutions[0].explanation.notes == ["horizontal"]


def test_generate_vertical_permutations():
    from boardcomposer.solver.layout_generator import generate_vertical_permutations

    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = generate_vertical_permutations(project)

    assert len(solutions) == 2
    assert {s.placements[0].board_id for s in solutions} == {"A", "B"}
