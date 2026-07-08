from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.search import search_best_solution
from boardcomposer.solver.skyline_runner import iter_skyline_solutions


def generate_best_skyline_solution(project: Project) -> AssemblySolution:
    return search_best_solution(iter_skyline_solutions(project))
