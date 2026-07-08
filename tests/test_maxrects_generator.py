from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.maxrects_generator import generate_maxrects_solution


def test_generate_maxrects_solution():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_maxrects_solution(project)

    assert len(solution.placements) == 2
    assert "maxrects" in solution.explanation.notes


def test_generate_maxrects_solution_records_selected_heuristic():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_maxrects_solution(project)

    assert "maxrects" in solution.explanation.notes
    assert any(
        name in solution.explanation.notes
        for name in [
            "best_area_fit",
            "best_short_side_fit",
            "best_long_side_fit",
            "best_bottom_left_fit",
        ]
    )


def test_generate_maxrects_solution_records_selected_ordering():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_maxrects_solution(project)

    assert any(
        name in solution.explanation.notes
        for name in ["original", "largest_area", "longest_edge"]
    )
