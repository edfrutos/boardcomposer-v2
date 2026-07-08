"""Generate Skyline-based layout solutions."""

from boardcomposer.domain import AssemblySolution, Project

from boardcomposer.solver.skyline_search import generate_best_skyline_solution


def generate_skyline_solution(project: Project) -> AssemblySolution:
    """Generate the best Skyline layout solution for the given project."""

    return generate_best_skyline_solution(project)
