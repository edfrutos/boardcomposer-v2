from typing import Protocol

from boardcomposer.domain import Board, BoardPlacement


class PlacementLike(Protocol):
    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float
    rotated: bool


class PackingAlgorithm(Protocol):
    def place(
        self,
        length_mm: float,
        width_mm: float,
        allow_rotation: bool = False,
    ) -> PlacementLike | None: ...


def to_board_placement(
    placement: PlacementLike,
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


def place_all_boards(
    packer: PackingAlgorithm,
    boards: list[Board],
    allow_rotation: bool,
) -> list[BoardPlacement]:
    placements: list[BoardPlacement] = []

    for index, board in enumerate(boards):
        placement = packer.place(
            length_mm=board.length_mm,
            width_mm=board.width_mm,
            allow_rotation=allow_rotation,
        )

        if placement is None:
            continue

        placements.append(to_board_placement(placement, board, index))

    return placements
