from collections.abc import Iterator

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.solver.maxrects_beam_runner import (
    iter_beam_maxrects_solutions,
)
from boardcomposer.solver.maxrects_runner import iter_maxrects_solutions


def iter_maxrects_candidates(
    project: Project,
    beam_width: int = 1,
) -> Iterator[AssemblySolution]:
    if beam_width <= 1:
        yield from iter_maxrects_solutions(project)
        return

    yield from iter_beam_maxrects_solutions(
        project,
        beam_width=beam_width,
    )
