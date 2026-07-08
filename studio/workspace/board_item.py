from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import QGraphicsRectItem

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
    return board
