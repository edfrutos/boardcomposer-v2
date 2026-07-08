from copy import deepcopy
from dataclasses import dataclass

from boardcomposer.domain import Board, BoardPlacement
from boardcomposer.solver.maxrects.maxrects import MaxRects


@dataclass
class MaxRectsState:
    packer: MaxRects
    placements: list[BoardPlacement]
    next_board: int

    def clone(self) -> "MaxRectsState":
        return MaxRectsState(
            packer=deepcopy(self.packer),
            placements=self.placements.copy(),
            next_board=self.next_board,
        )

    def expand(
        self,
        boards: list[Board],
        allow_rotation: bool,
    ) -> list["MaxRectsState"]:
        if self.next_board >= len(boards):
            return []

        board = boards[self.next_board]
        candidates = self.packer.find_candidates(
            board.length_mm,
            board.width_mm,
            allow_rotation=allow_rotation,
        )

        states = []

        for candidate in candidates:
            state = self.clone()
            placement = state.packer.place_candidate(candidate)
            state.placements.append(
                BoardPlacement(
                    board_id=board.id or f"board-{self.next_board + 1}",
                    x_mm=placement.x_mm,
                    y_mm=placement.y_mm,
                    length_mm=placement.length_mm,
                    width_mm=placement.width_mm,
                    rotated=placement.rotated,
                )
            )
            state.next_board += 1
            states.append(state)

        return states
