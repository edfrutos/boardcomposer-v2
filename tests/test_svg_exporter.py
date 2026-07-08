from boardcomposer import AssemblySolution, BoardPlacement
from boardcomposer.export import solution_to_svg


def test_solution_to_svg():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    svg = solution_to_svg(solution)

    assert svg.startswith("<svg")
    assert "<rect" in svg
    assert "A" in svg
