from __future__ import annotations

from PySide6.QtCore import QRectF
from PySide6 import QtCore

from studio.workspace.board_piece_item import BoardPieceItem

SNAP_THRESHOLD_MM = 20.0


class PlacementValidator:
    """Única fuente de verdad para validar colocaciones."""

    def __init__(self, board_rect: QtCore.QRectF):
        self.board_rect = board_rect

    def constrain_position(
        self,
        item: BoardPieceItem,
        new_pos: QtCore.QPointF,
        gap_mm: float = 0.0,
    ) -> QtCore.QPointF:
        snapped = self._snap_to_neighbors(item, new_pos, gap_mm)

        rect = item.rect()

        x = min(
            max(snapped.x(), self.board_rect.left()),
            self.board_rect.right() - rect.width(),
        )
        y = min(
            max(snapped.y(), self.board_rect.top()),
            self.board_rect.bottom() - rect.height(),
        )

        return QtCore.QPointF(x, y)

    def _snap_to_neighbors(
        self,
        item: BoardPieceItem,
        new_pos: QtCore.QPointF,
        gap_mm: float,
    ) -> QtCore.QPointF:
        """Efecto imán: si al arrastrar una pieza su borde queda a menos de
        SNAP_THRESHOLD_MM del borde de otra ya colocada, la sitúa justo al
        lado (a `gap_mm` de distancia, el ancho de corte de sierra
        configurado) en vez de dejarla montarse encima o quedar a ojo."""
        if item.scene() is None:
            return new_pos

        rect = item.rect()
        width, height = rect.width(), rect.height()
        left, top = new_pos.x(), new_pos.y()
        right, bottom = left + width, top + height

        best_axis: str | None = None
        best_value = 0.0
        best_distance = SNAP_THRESHOLD_MM

        for other in item.scene().items():
            if other is item or not isinstance(other, BoardPieceItem):
                continue

            other_rect = self.piece_rect(other)

            shares_vertical_span = (
                top < other_rect.bottom() and bottom > other_rect.top()
            )
            shares_horizontal_span = (
                left < other_rect.right() and right > other_rect.left()
            )

            if shares_vertical_span:
                for candidate_x in (
                    other_rect.right() + gap_mm,
                    other_rect.left() - width - gap_mm,
                ):
                    distance = abs(left - candidate_x)
                    if distance < best_distance:
                        best_axis, best_value, best_distance = (
                            "x",
                            candidate_x,
                            distance,
                        )

            if shares_horizontal_span:
                for candidate_y in (
                    other_rect.bottom() + gap_mm,
                    other_rect.top() - height - gap_mm,
                ):
                    distance = abs(top - candidate_y)
                    if distance < best_distance:
                        best_axis, best_value, best_distance = (
                            "y",
                            candidate_y,
                            distance,
                        )

        if best_axis == "x":
            return QtCore.QPointF(best_value, new_pos.y())
        if best_axis == "y":
            return QtCore.QPointF(new_pos.x(), best_value)
        return new_pos

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
