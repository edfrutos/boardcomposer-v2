from collections.abc import Callable

from boardcomposer.domain import AssemblySolution, Project

SolutionGenerator = Callable[[Project], AssemblySolution]
LayoutGenerator = Callable[[Project], list[AssemblySolution]]


def single_solution_generator(
    generator: SolutionGenerator,
) -> LayoutGenerator:
    def wrapped(project: Project) -> list[AssemblySolution]:
        return [generator(project)]

    return wrapped
