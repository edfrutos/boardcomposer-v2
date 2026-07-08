from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.free_space_generator import generate_free_space_solution


def test_generate_free_space_solution():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=600,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_free_space_solution(project)

    assert len(solution.placements) == 2
    assert solution.explanation.notes == ["free_space"]


def test_generate_free_space_solution_skips_boards_that_do_not_fit():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=1000,
            max_width_mm=300,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))

    solution = generate_free_space_solution(project)

    assert len(solution.placements) == 0
