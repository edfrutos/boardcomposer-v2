from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.maxrects_search import (
    generate_beam_maxrects_solution,
    generate_best_maxrects_solution,
)


def _project() -> Project:
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))
    return project


def test_beam_width_one_matches_classic():
    project = _project()

    classic = generate_best_maxrects_solution(project)
    beam = generate_beam_maxrects_solution(
        project,
        beam_width=1,
    )

    assert len(classic.placements) == len(beam.placements)


def test_beam_solution_records_strategy():
    project = _project()

    solution = generate_beam_maxrects_solution(
        project,
        beam_width=3,
    )

    assert "beam" in solution.explanation.notes
    assert "width=3" in solution.explanation.notes


def test_beam_records_selected_heuristic():
    project = _project()

    solution = generate_beam_maxrects_solution(
        project,
        beam_width=2,
    )

    assert any(
        heuristic in solution.explanation.notes
        for heuristic in (
            "best_area_fit",
            "best_short_side_fit",
            "best_long_side_fit",
            "best_bottom_left_fit",
        )
    )
