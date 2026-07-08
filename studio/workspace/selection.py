from PySide6.QtGui import QColor, QPen

from studio.workspace.board_piece_item import BoardPieceItem


def apply_selection(item: BoardPieceItem, selected: bool) -> None:
    item.setSelected(selected)

    if selected:
        item.setBrush(QColor("#bfdbfe"))
        item.setPen(QPen(QColor("#dc2626"), 10))
    else:
        item.setBrush(QColor("#dbeafe"))
        item.setPen(QPen(QColor("#1d4ed8"), 3))
