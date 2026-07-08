from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.skyline_generator import generate_skyline_solution


def test_generate_skyline_solution():
    project = Project(
        constraints=ProjectConstraints(
            max_width_mm=3000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_skyline_solution(project)

    assert len(solution.placements) == 2
    assert "skyline" in solution.explanation.notes


def test_skyline_generator_preserves_layout_name():
    project = Project(
        constraints=ProjectConstraints(
            max_width_mm=3000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))

    solution = generate_skyline_solution(project)

    assert "skyline" in solution.explanation.notes


def test_skyline_generator_stacks_when_width_is_limited():
    project = Project(
        constraints=ProjectConstraints(
            max_width_mm=2000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_skyline_solution(project)

    assert len(solution.placements) == 2
    assert solution.total_length_mm == 2000
    assert solution.total_width_mm == 600
