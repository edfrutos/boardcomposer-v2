from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.maxrects_search import generate_best_maxrects_solution


def generate_maxrects_solution(project: Project) -> AssemblySolution:
    return generate_best_maxrects_solution(project)
