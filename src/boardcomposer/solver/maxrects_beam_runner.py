from collections.abc import Iterator

from boardcomposer.domain import AssemblySolution, Board, Project, SolutionExplanation
from boardcomposer.solver.maxrects.beam import search_states
from boardcomposer.solver.maxrects.heuristics import Heuristic
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.orderings import MAXRECTS_BOARD_ORDERINGS
from boardcomposer.solver.maxrects.scoring import score_state
from boardcomposer.solver.maxrects.state import MaxRectsState
from boardcomposer.solver.maxrects.strategies import MAXRECTS_HEURISTICS
from boardcomposer.solver.maxrects_runner import _maxrects_size


def _beam_candidate(
    project: Project,
    boards: list[Board],
    ordering_name: str,
    heuristic_name: str,
    heuristic: Heuristic,
    beam_width: int,
) -> AssemblySolution:
    length, width = _maxrects_size(project)

    initial = MaxRectsState(
        packer=MaxRects(
            length_mm=length,
            width_mm=width,
            heuristic=heuristic,
        ),
        placements=[],
        next_board=0,
    )

    states = search_states(
        initial=initial,
        boards=boards,
        allow_rotation=project.constraints.allow_rotation,
        width=beam_width,
    )

    best_state = max(states, key=score_state)

    return AssemblySolution(
        placements=best_state.placements,
        explanation=SolutionExplanation(
            notes=[
                "maxrects",
                "beam",
                heuristic_name,
                ordering_name,
                f"width={beam_width}",
            ]
        ),
    )


def iter_beam_maxrects_solutions(
    project: Project,
    beam_width: int,
) -> Iterator[AssemblySolution]:
    for heuristic_name, heuristic in MAXRECTS_HEURISTICS:
        for ordering_name, ordering in MAXRECTS_BOARD_ORDERINGS:
            yield _beam_candidate(
                project=project,
                boards=ordering(project.boards),
                ordering_name=ordering_name,
                heuristic_name=heuristic_name,
                heuristic=heuristic,
                beam_width=beam_width,
            )
