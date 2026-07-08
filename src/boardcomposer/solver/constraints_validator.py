from boardcomposer.domain import AssemblySolution, ProjectConstraints


def respects_constraints(
    solution: AssemblySolution,
    constraints: ProjectConstraints,
) -> bool:
    if (
        constraints.max_length_mm is not None
        and solution.total_length_mm > constraints.max_length_mm
    ):
        return False

    if (
        constraints.max_width_mm is not None
        and solution.total_width_mm > constraints.max_width_mm
    ):
        return False

    return True
