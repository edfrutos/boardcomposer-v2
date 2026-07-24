from PySide6.QtGui import QColor, QFont, QPen
from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsSimpleTextItem

from studio.models import StudioBoard


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
    # board's origin.
    label = QGraphicsSimpleTextItem(board_model.board_id, board)
    label.setFont(QFont("Arial", 48))
    label.setBrush(QColor("#111827"))
    label.setPos(0, -60)

    return board
