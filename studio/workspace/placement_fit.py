"""Plain-data placement fit check, no Qt dependency.

PlacementValidator (placement_validator.py) does the same job but only for
the interactive drag/rotate path, coupled to live Qt graphics items. Actions
that reassign a piece to a different board (MoveToBoardCommand) happen
outside that scene, so they need a Qt-free equivalent to check the move
before committing it — otherwise a piece keeps its old x/y and rotation and
can silently end up outside the destination board's bounds, or overlapping
a piece already there.
"""

from boardcomposer.geometry.rectangle import Rectangle

from studio.models import StudioBoard, StudioPiece, StudioPlacement


def piece_fits_on_board(
    board: StudioBoard,
    piece: StudioPiece,
    x_mm: float,
    y_mm: float,
    rotated: bool,
    other_placements: list[StudioPlacement],
    pieces_by_id: dict[str, StudioPiece],
) -> bool:
    length_mm, width_mm = piece.length_mm, piece.width_mm
    if rotated:
        length_mm, width_mm = width_mm, length_mm

    rect = Rectangle(x_mm, y_mm, length_mm, width_mm)

    if rect.x_mm < 0 or rect.y_mm < 0:
        return False
    if rect.right_mm > board.length_mm or rect.top_mm > board.width_mm:
        return False

    for other in other_placements:
        other_piece = pieces_by_id.get(other.piece_id)
        if other_piece is None:
            continue

        other_length_mm, other_width_mm = other_piece.length_mm, other_piece.width_mm
        if other.rotated:
            other_length_mm, other_width_mm = other_width_mm, other_length_mm

        other_rect = Rectangle(other.x_mm, other.y_mm, other_length_mm, other_width_mm)
        if rect.overlaps(other_rect):
            return False

    return True
