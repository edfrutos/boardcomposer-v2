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


def _project_with_two_boards() -> StudioProject:
    return StudioProject(
        project_id="proj-2",
        name="Demo",
        boards=[
            StudioBoard("A", 2000, 300),
            StudioBoard("B", 1000, 300),
        ],
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


def test_to_core_project_uses_active_board_dimensions():
    services = StudioServices()
    services.projects.new_project(_project_with_two_boards())

    core_project = services.layout.to_core_project("B")

    assert core_project.constraints.max_length_mm == 1000


def test_to_core_project_falls_back_to_first_board_without_active_board():
    services = StudioServices()
    services.projects.new_project(_project_with_two_boards())

    core_project = services.layout.to_core_project()

    assert core_project.constraints.max_length_mm == 2000


def test_to_core_project_uses_each_pieces_own_thickness():
    services = StudioServices()
    project = StudioProject(
        project_id="proj-3",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[StudioPiece("p1", 700, 300, thickness_mm=25.0)],
    )
    services.projects.new_project(project)

    core_project = services.layout.to_core_project()

    assert core_project.boards[0].thickness_mm == 25.0


def test_apply_last_solution_assigns_placements_to_active_board():
    services = StudioServices()
    services.projects.new_project(_project_with_two_boards())
    services.layout.solve_current_project("B")

    assert services.layout.apply_last_solution_to_current_project("B") is True

    placements = services.projects.current_project.placements
    assert placements
    assert all(placement.board_id == "B" for placement in placements)
