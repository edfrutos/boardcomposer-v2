from boardcomposer import AssemblySolution, BoardPlacement, SolutionScore


def test_solution_dimensions_and_area():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 2000, 300),
            BoardPlacement("B", 2000, 0, 1000, 300),
        ],
        score=SolutionScore(waste_score=30),
    )

    assert solution.total_length_mm == 3000
    assert solution.total_width_mm == 300
    assert solution.used_area_mm2 == 900000
    assert solution.bounding_area_mm2 == 900000
    assert solution.waste_area_mm2 == 0
    assert solution.waste_ratio == 0


def test_solution_with_empty_placements():
    solution = AssemblySolution(placements=[])

    assert solution.total_length_mm == 0
    assert solution.total_width_mm == 0
    assert solution.used_area_mm2 == 0
    assert solution.bounding_area_mm2 == 0
    assert solution.waste_ratio == 0


def test_solution_id_is_stable_regardless_of_placement_order():
    placements = [
        BoardPlacement("A", 0, 0, 2000, 300),
        BoardPlacement("B", 2000, 0, 1000, 300),
    ]

    forward = AssemblySolution(placements=placements)
    reversed_ = AssemblySolution(placements=list(reversed(placements)))

    assert forward.solution_id == reversed_.solution_id
    assert len(forward.solution_id) == 8


def test_solution_id_differs_for_different_content():
    a = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 2000, 300)])
    b = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 1000, 300)])

    assert a.solution_id != b.solution_id
