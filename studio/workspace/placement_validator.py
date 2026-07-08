from __future__ import annotations

from PySide6.QtCore import QRectF
from PySide6 import QtCore

from studio.workspace.board_piece_item import BoardPieceItem


class PlacementValidator:
    """Única fuente de verdad para validar colocaciones."""

    def __init__(self, board_rect: QtCore.QRectF):
        self.board_rect = board_rect

    def constrain_position(
        self,
        item: BoardPieceItem,
        new_pos: QtCore.QPointF,
    ) -> QtCore.QPointF:
        rect = item.rect()

        x = min(
            max(new_pos.x(), self.board_rect.left()),
            self.board_rect.right() - rect.width(),
        )
        y = min(
            max(new_pos.y(), self.board_rect.top()),
            self.board_rect.bottom() - rect.height(),
        )

        return QtCore.QPointF(x, y)

    def collides(self, item: BoardPieceItem) -> bool:
        item_rect = self.piece_rect(item)

        for other in item.scene().items():
            if other is item or not isinstance(other, BoardPieceItem):
                continue

            if self.overlaps(item_rect, self.piece_rect(other)):
                return True

        return False

    def item_logical_rect(self, item: BoardPieceItem) -> QRectF:
        return QRectF(
            item.pos().x(),
            item.pos().y(),
            item.rect().width(),
            item.rect().height(),
        )

    def piece_rect(self, item: BoardPieceItem) -> QRectF:

        return QRectF(
            item.pos().x(),
            item.pos().y(),
            item.rect().width(),
            item.rect().height(),
        )

    def overlaps(self, first: QRectF, second: QRectF) -> bool:
        return first.intersects(second)

    def rotated_rect(self, item: BoardPieceItem, angle: int) -> QRectF:
        angle = angle % 180

        if angle == 90:
            return QRectF(
                item.pos().x(),
                item.pos().y(),
                item.width_mm,
                item.length_mm,
            )

        return QRectF(
            item.pos().x(),
            item.pos().y(),
            item.length_mm,
            item.width_mm,
        )

    def can_rotate(self, item: BoardPieceItem, angle: int) -> bool:
        rotated = self.rotated_rect(item, angle)

        if not self.board_rect.contains(rotated):
            return False

        for other in item.scene().items():
            if other is item or not isinstance(other, BoardPieceItem):
                continue

            if self.overlaps(rotated, self.piece_rect(other)):
                return False

        return True

    def can_place(self, item: BoardPieceItem) -> bool:
        return self.board_rect.contains(self.piece_rect(item)) and not self.collides(
            item
        )
