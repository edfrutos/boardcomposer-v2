from collections.abc import Callable, Iterator

from boardcomposer.domain import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Project,
    SolutionExplanation,
)
from boardcomposer.solver.maxrects.heuristics import Heuristic
from boardcomposer.solver.maxrects.maxrects import MaxRects
from boardcomposer.solver.maxrects.orderings import MAXRECTS_BOARD_ORDERINGS
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement
from boardcomposer.solver.maxrects.strategies import MAXRECTS_HEURISTICS

BoardOrdering = Callable[[list[Board]], list[Board]]


def _maxrects_size(project: Project) -> tuple[float, float]:
    length = project.constraints.max_length_mm or sum(
        board.length_mm for board in project.boards
    )
    width = project.constraints.max_width_mm or max(
        (board.width_mm for board in project.boards),
        default=0,
    )

    return length, width


def _to_board_placement(
    placement: MaxRectsPlacement,
    board: Board,
    index: int,
) -> BoardPlacement:
    return BoardPlacement(
        board_id=board.id or f"board-{index + 1}",
        x_mm=placement.x_mm,
        y_mm=placement.y_mm,
        length_mm=placement.length_mm,
        width_mm=placement.width_mm,
        rotated=placement.rotated,
    )


def _place_all_boards(
    maxrects: MaxRects,
    boards: list[Board],
    allow_rotation: bool,
) -> list[BoardPlacement]:
    placements: list[BoardPlacement] = []

    for index, board in enumerate(boards):
        placement = maxrects.place(
            length_mm=board.length_mm,
            width_mm=board.width_mm,
            allow_rotation=allow_rotation,
        )

        if placement is None:
            continue

        placements.append(_to_board_placement(placement, board, index))

    return placements


def generate_maxrects_candidate(
    project: Project,
    heuristic_name: str,
    heuristic: Heuristic,
    ordering_name: str,
    ordering: BoardOrdering,
) -> AssemblySolution:
    length, width = _maxrects_size(project)
    maxrects = MaxRects(
        length_mm=length,
        width_mm=width,
        heuristic=heuristic,
    )

    placements = _place_all_boards(
        maxrects=maxrects,
        boards=ordering(project.boards),
        allow_rotation=project.constraints.allow_rotation,
    )

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(
            notes=["maxrects", heuristic_name, ordering_name]
        ),
    )


def iter_maxrects_solutions(project: Project) -> Iterator[AssemblySolution]:
    for heuristic_name, heuristic in MAXRECTS_HEURISTICS:
        for ordering_name, ordering in MAXRECTS_BOARD_ORDERINGS:
            yield generate_maxrects_candidate(
                project=project,
                heuristic_name=heuristic_name,
                heuristic=heuristic,
                ordering_name=ordering_name,
                ordering=ordering,
            )
