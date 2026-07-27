from studio.export.solution_bridge import studio_project_to_solution
from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject


def test_studio_project_to_solution_converts_placements():
    project = StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[StudioPiece("p1", 500, 200)],
        placements=[StudioPlacement("p1", 10, 20, board_id="A")],
    )

    solution = studio_project_to_solution(project)

    assert len(solution.placements) == 1
    placement = solution.placements[0]
    assert placement.board_id == "p1"
    assert placement.x_mm == 10
    assert placement.y_mm == 20
    assert placement.length_mm == 500
    assert placement.width_mm == 200


def test_studio_project_to_solution_swaps_dimensions_when_rotated():
    project = StudioProject(
        project_id="proj-1",
        name="Demo",
        pieces=[StudioPiece("p1", 500, 200)],
        placements=[
            StudioPlacement("p1", 0, 0, board_id="A", rotated=True, rotation=90)
        ],
    )

    solution = studio_project_to_solution(project)

    placement = solution.placements[0]
    assert placement.length_mm == 200
    assert placement.width_mm == 500
    assert placement.rotated is True


def test_studio_project_to_solution_skips_placements_without_a_matching_piece():
    project = StudioProject(
        project_id="proj-1",
        name="Demo",
        pieces=[],
        placements=[StudioPlacement("missing", 0, 0, board_id="A")],
    )

    solution = studio_project_to_solution(project)

    assert solution.placements == []


def test_the_kerf_never_reaches_the_exported_plan():
    # The kerf is packing slack, not part of the piece: LayoutService adds it
    # when handing pieces to the solver, and it has to stop there. A plan
    # drawn 3mm too big on every side would be cut wrong.
    project = StudioProject(
        project_id="proj-1",
        name="Demo",
        kerf_mm=3,
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[StudioPiece("p1", 500, 200)],
        placements=[StudioPlacement("p1", 10, 20, board_id="A")],
    )

    placement = studio_project_to_solution(project).placements[0]

    assert (placement.length_mm, placement.width_mm) == (500, 200)


def test_studio_project_to_solution_with_no_placements_is_empty():
    project = StudioProject(project_id="proj-1", name="Demo")

    solution = studio_project_to_solution(project)

    assert solution.placements == []
