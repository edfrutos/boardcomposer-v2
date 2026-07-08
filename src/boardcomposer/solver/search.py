from collections.abc import Iterable

from boardcomposer.domain import AssemblySolution


def search_best_solution(
    solutions: Iterable[AssemblySolution],
) -> AssemblySolution:
    return max(
        solutions,
        key=lambda solution: (
            len(solution.placements),
            -solution.total_width_mm,
            -solution.total_length_mm,
        ),
    )
