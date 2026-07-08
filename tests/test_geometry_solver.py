from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver import GeometrySolver


def build_two_board_project() -> Project:
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))
    return project


def test_geometry_solver_returns_solutions():
    solutions = GeometrySolver(build_two_board_project()).solve()

    assert len(solutions) > 0


def test_geometry_solver_includes_expected_layout_families():
    solutions = GeometrySolver(build_two_board_project()).solve()
    layouts = {tuple(solution.explanation.notes) for solution in solutions}

    assert ("horizontal_permutation",) in layouts
    assert ("vertical_permutation",) in layouts


def test_geometry_solver_sorts_solutions_by_score():
    solutions = GeometrySolver(build_two_board_project()).solve()

    scores = [solution.score.total for solution in solutions]

    assert scores == sorted(scores, reverse=True)


def test_geometry_solver_respects_constraints():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=2500,
            max_width_mm=600,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = GeometrySolver(project).solve()

    assert len(solutions) > 0
    assert all(solution.total_length_mm <= 2500 for solution in solutions)
    assert all(solution.total_width_mm <= 600 for solution in solutions)


def test_geometry_solver_matches_candidate_pipeline():
    from boardcomposer.solver.candidate_pipeline import CandidatePipeline
    from boardcomposer.solver.strategies import balanced_strategy

    project = build_two_board_project()
    strategy = balanced_strategy()

    solver_solutions = GeometrySolver(project, strategy=strategy).solve()
    pipeline_solutions = CandidatePipeline(project, strategy).run()

    assert [s.score.total for s in solver_solutions] == [
        s.score.total for s in pipeline_solutions
    ]
