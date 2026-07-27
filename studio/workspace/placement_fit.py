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
    kerf_mm: float = 0.0,
) -> bool:
    """`kerf_mm` is the saw cut that has to run between two pieces before
    either can come off the board. Every piece — the candidate and each
    neighbour alike — is widened to the right and downwards only, the same
    asymmetric convention LayoutService uses when it hands pieces to the
    solver. Widening both sides of the comparison is what makes the demanded
    gap exactly one kerf in either direction: widening only the candidate
    would miss the neighbour sitting to its left, whose own cut is the one
    being encroached on. The board's own edge is not a cut between two
    pieces, so a piece flush against it stays legal.
    """
    length_mm, width_mm = piece.length_mm, piece.width_mm
    if rotated:
        length_mm, width_mm = width_mm, length_mm

    rect = Rectangle(x_mm, y_mm, length_mm, width_mm)

    if rect.x_mm < 0 or rect.y_mm < 0:
        return False
    if rect.right_mm > board.length_mm or rect.top_mm > board.width_mm:
        return False

    # Bounds are checked against the real piece; overlap, against the piece
    # plus its cut.
    rect = Rectangle(x_mm, y_mm, length_mm + kerf_mm, width_mm + kerf_mm)

    for other in other_placements:
        other_piece = pieces_by_id.get(other.piece_id)
        if other_piece is None:
            continue

        other_length_mm, other_width_mm = other_piece.length_mm, other_piece.width_mm
        if other.rotated:
            other_length_mm, other_width_mm = other_width_mm, other_length_mm

        other_rect = Rectangle(
            other.x_mm,
            other.y_mm,
            other_length_mm + kerf_mm,
            other_width_mm + kerf_mm,
        )
        if rect.overlaps(other_rect):
            return False

    return True


def find_free_position(
    board: StudioBoard,
    length_mm: float,
    width_mm: float,
    other_placements: list[StudioPlacement],
    pieces_by_id: dict[str, StudioPiece],
    kerf_mm: float = 0.0,
) -> tuple[float, float] | None:
    """Finds a top-left corner where a length_mm x width_mm rectangle fits
    on `board` without leaving its bounds or overlapping `other_placements`,
    leaving `kerf_mm` of saw cut between it and each neighbour.

    A corner-search heuristic, not full bin-packing: candidates are the
    board's origin plus the right/bottom edge (plus the cut) of every
    existing placement, scanned top-to-bottom then left-to-right. Good
    enough to relocate one piece into free space a move/rotate would
    otherwise be rejected for — solving a whole layout from scratch is what
    Generar (the solver) is for.
    """
    other_rects = []
    candidates_x = {0.0}
    candidates_y = {0.0}

    for placement in other_placements:
        piece = pieces_by_id.get(placement.piece_id)
        if piece is None:
            continue

        piece_length_mm, piece_width_mm = piece.length_mm, piece.width_mm
        if placement.rotated:
            piece_length_mm, piece_width_mm = piece_width_mm, piece_length_mm

        other_rects.append(
            Rectangle(
                placement.x_mm,
                placement.y_mm,
                piece_length_mm + kerf_mm,
                piece_width_mm + kerf_mm,
            )
        )
        candidates_x.add(placement.x_mm + piece_length_mm + kerf_mm)
        candidates_y.add(placement.y_mm + piece_width_mm + kerf_mm)

    for y_mm in sorted(candidates_y):
        for x_mm in sorted(candidates_x):
            candidate = Rectangle(x_mm, y_mm, length_mm, width_mm)
            if candidate.right_mm > board.length_mm:
                continue
            if candidate.top_mm > board.width_mm:
                continue

            # Same split as piece_fits_on_board: the board's own edge needs
            # no clearance, a neighbour does.
            with_cut = Rectangle(x_mm, y_mm, length_mm + kerf_mm, width_mm + kerf_mm)
            if any(with_cut.overlaps(other) for other in other_rects):
                continue
            return (x_mm, y_mm)

    return None
