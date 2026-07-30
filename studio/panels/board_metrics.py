"""Metrics shared by panel render functions that show board utilization
(inspector_panel.render_board, timeline_panel.render_overview) — kept as a
neutral sibling both import, rather than one panel depending on another.
"""

from studio.models import StudioBoard, StudioPiece, StudioPlacement


def board_utilization(
    board: StudioBoard,
    placements: list[StudioPlacement],
    pieces_by_id: dict[str, StudioPiece],
) -> float:
    board_area = board.length_mm * board.width_mm
    used_area = sum(
        pieces_by_id[placement.piece_id].length_mm
        * pieces_by_id[placement.piece_id].width_mm
        for placement in placements
        if placement.piece_id in pieces_by_id
    )
    return used_area / board_area if board_area else 0.0
