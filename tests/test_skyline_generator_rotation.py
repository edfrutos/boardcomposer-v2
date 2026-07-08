from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.skyline_generator import generate_skyline_solution


def test_skyline_generator_uses_rotation_when_allowed():
    project = Project(
        constraints=ProjectConstraints(
            max_width_mm=500,
            allow_rotation=True,
        )
    )
    project.add_board(Board(800, 400, 20, "A"))

    solution = generate_skyline_solution(project)

    assert len(solution.placements) == 1
    assert solution.placements[0].rotated is True
    assert solution.placements[0].length_mm == 400
    assert solution.placements[0].width_mm == 800


def test_skyline_default_width_considers_rotation():
    project = Project(
        constraints=ProjectConstraints(
            allow_rotation=True,
        )
    )
    project.add_board(Board(800, 400, 20, "A"))

    solution = generate_skyline_solution(project)

    assert len(solution.placements) == 1
    assert solution.placements[0].rotated is True
    assert solution.placements[0].length_mm == 400
