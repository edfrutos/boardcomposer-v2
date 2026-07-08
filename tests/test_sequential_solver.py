from boardcomposer import Board, Project
from boardcomposer.solver import SequentialSolver


def test_sequential_solver_returns_one_solution():
    project = Project()
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))

    solver = SequentialSolver(project)
    solutions = solver.solve()

    assert len(solutions) == 1


def test_sequential_solver_places_boards_in_sequence():
    project = Project()
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))

    solution = SequentialSolver(project).solve()[0]

    assert solution.placements[0].x_mm == 0
    assert solution.placements[1].x_mm == 2000
    assert solution.total_length_mm == 3000
    assert solution.total_width_mm == 300


def test_solver_rotates_board_when_allowed():
    from boardcomposer import ProjectConstraints

    project = Project(
        constraints=ProjectConstraints(max_length_mm=2300, allow_rotation=True)
    )
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))

    solution = SequentialSolver(project).solve()[0]

    assert len(solution.placements) == 2
    assert solution.placements[1].rotated is True
    assert solution.total_length_mm == 2300


def test_solver_respects_max_width():
    from boardcomposer import ProjectConstraints

    project = Project(constraints=ProjectConstraints(max_width_mm=250))
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))

    solution = SequentialSolver(project).solve()[0]

    assert len(solution.placements) == 0


def test_solver_wraps_to_next_row_when_length_exceeded():
    from boardcomposer import ProjectConstraints

    project = Project(
        constraints=ProjectConstraints(max_length_mm=2500, max_width_mm=600)
    )
    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))

    solution = SequentialSolver(project).solve()[0]

    assert len(solution.placements) == 2
    assert solution.placements[1].x_mm == 0
    assert solution.placements[1].y_mm == 300
    assert solution.total_length_mm == 2000
    assert solution.total_width_mm == 600


def test_solver_score_combines_usage_and_waste():
    project = Project()
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="A"))
    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))

    solution = SequentialSolver(project).solve()[0]

    assert solution.score.material_usage_score == 50
    assert solution.score.waste_score == 50
    assert solution.score.total == 100
