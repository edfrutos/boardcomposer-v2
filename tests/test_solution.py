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
