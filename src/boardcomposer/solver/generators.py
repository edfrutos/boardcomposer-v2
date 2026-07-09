from collections.abc import Callable

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.free_space_generator import generate_free_space_solution
from boardcomposer.solver.skyline_generator import generate_skyline_solution
from boardcomposer.solver.maxrects_generator import generate_maxrects_solution
from boardcomposer.solver.maxrects_search import generate_beam_maxrects_solution
from boardcomposer.solver.layout_generator import (
    generate_horizontal_permutations,
    generate_vertical_permutations,
)

MAXRECTS_BEAM_WIDTH = 4

LayoutGenerator = Callable[[Project], list[AssemblySolution]]


def horizontal_generator(project: Project) -> list[AssemblySolution]:
    return generate_horizontal_permutations(project)


def vertical_generator(project: Project) -> list[AssemblySolution]:
    return generate_vertical_permutations(project)


def free_space_generator(project: Project) -> list[AssemblySolution]:
    return [generate_free_space_solution(project)]


def skyline_generator(project: Project) -> list[AssemblySolution]:
    return [generate_skyline_solution(project)]


def maxrects_generator(project: Project) -> list[AssemblySolution]:
    return [generate_maxrects_solution(project)]


def maxrects_beam_generator(project: Project) -> list[AssemblySolution]:
    return [generate_beam_maxrects_solution(project, beam_width=MAXRECTS_BEAM_WIDTH)]


GENERATOR_REGISTRY: dict[str, LayoutGenerator] = {
    "horizontal": horizontal_generator,
    "vertical": vertical_generator,
    "free_space": free_space_generator,
    "skyline": skyline_generator,
    "maxrects": maxrects_generator,
    "maxrects_beam": maxrects_beam_generator,
}


def generators_by_name(names: list[str]) -> list[LayoutGenerator]:
    return [GENERATOR_REGISTRY[name] for name in names]
