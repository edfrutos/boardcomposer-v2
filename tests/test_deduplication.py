from boardcomposer import AssemblySolution, BoardPlacement
from boardcomposer.solver.deduplication import deduplicate_solutions


def test_deduplicate_solutions_removes_duplicates():
    solution_a = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])
    solution_b = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    unique = deduplicate_solutions([solution_a, solution_b])

    assert len(unique) == 1
