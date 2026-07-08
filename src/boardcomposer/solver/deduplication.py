from boardcomposer.domain import AssemblySolution


def solution_signature(solution: AssemblySolution) -> tuple:
    return tuple(
        sorted(
            (
                placement.board_id,
                placement.x_mm,
                placement.y_mm,
                placement.length_mm,
                placement.width_mm,
                placement.rotated,
            )
            for placement in solution.placements
        )
    )


def deduplicate_solutions(
    solutions: list[AssemblySolution],
) -> list[AssemblySolution]:
    seen = set()
    unique = []

    for solution in solutions:
        signature = solution_signature(solution)

        if signature in seen:
            continue

        seen.add(signature)
        unique.append(solution)

    return unique
