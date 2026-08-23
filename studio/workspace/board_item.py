from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPen
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSimpleTextItem

from studio.models import StudioBoard

# A fixed 48pt label used to dwarf a thin board (e.g. a 460x40mm baton) —
# scaled to the board's shorter side instead, capped so a large board still
# gets a comfortably readable size rather than an ever-growing one.
_MIN_LABEL_FONT_SIZE = 12
_MAX_LABEL_FONT_SIZE = 48
_LABEL_FONT_SIZE_RATIO = 0.5
_LABEL_MARGIN_MM = 8


def _label_font_size(length_mm: float, width_mm: float) -> int:
    shorter_side = min(length_mm, width_mm)
    return int(
        max(
            _MIN_LABEL_FONT_SIZE,
            min(_MAX_LABEL_FONT_SIZE, shorter_side * _LABEL_FONT_SIZE_RATIO),
        )
    )


def create_board_item(board_model: StudioBoard) -> QGraphicsRectItem:
    board = QGraphicsRectItem(
        0,
        0,
        board_model.length_mm,
        board_model.width_mm,
    )
    board.setBrush(QColor("#f8fafc"))
    board.setPen(QPen(QColor("#111827"), 4))

    # Pieces label themselves (piece_factory.py); the board rect never did,
    # so the only way to tell which board is active was the Explorer tree
    # or the Inspector — not the canvas itself. Placed above the rect,
    # outside its own bounds, so it never overlaps a piece placed near the
    # board's origin — the vertical offset is derived from the font's own
    # metrics (not a fixed guess) so it clears the rect at any font size.
    label = QGraphicsSimpleTextItem(board_model.board_id, board)
    font = QFont("Arial", _label_font_size(board_model.length_mm, board_model.width_mm))
    label.setFont(font)
    label.setBrush(QColor("#111827"))
    label.setPos(0, -(QFontMetricsF(font).height() + _LABEL_MARGIN_MM))

    return board
