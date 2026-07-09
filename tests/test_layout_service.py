from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.services import StudioServices


def _project_with_pieces() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[
            StudioPiece("p1", 700, 300),
            StudioPiece("p2", 520, 300),
        ],
    )


def test_compare_solutions_returns_empty_list_without_a_project():
    services = StudioServices()

    assert services.layout.compare_solutions() == []


def test_compare_solutions_returns_up_to_four_ranked_solutions():
    services = StudioServices()
    services.projects.new_project(_project_with_pieces())

    solutions = services.layout.compare_solutions()

    assert 1 <= len(solutions) <= 4
    scores = [solution.score.total for solution in solutions]
    assert scores == sorted(scores, reverse=True)


def test_apply_comparison_solution_applies_the_chosen_index():
    services = StudioServices()
    services.projects.new_project(_project_with_pieces())
    services.layout.compare_solutions()

    assert services.layout.apply_comparison_solution(0) is True
    assert len(services.projects.current_project.placements) > 0


def test_apply_comparison_solution_rejects_out_of_range_index():
    services = StudioServices()
    services.projects.new_project(_project_with_pieces())
    services.layout.compare_solutions()

    assert services.layout.apply_comparison_solution(99) is False
