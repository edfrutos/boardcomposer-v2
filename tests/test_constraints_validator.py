from boardcomposer import AssemblySolution, BoardPlacement, ProjectConstraints
from boardcomposer.solver.constraints_validator import respects_constraints


def test_respects_constraints_accepts_valid_solution():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    constraints = ProjectConstraints(max_length_mm=100, max_width_mm=50)

    assert respects_constraints(solution, constraints) is True


def test_respects_constraints_rejects_excess_length():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 101, 50)])

    constraints = ProjectConstraints(max_length_mm=100)

    assert respects_constraints(solution, constraints) is False
