from PySide6.QtGui import QColor, QFont, QPen
from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsSimpleTextItem


class BoardPieceItem(QGraphicsRectItem):
    def __init__(
        self,
        piece_id: str,
        x_mm: float,
        y_mm: float,
        length_mm: float,
        width_mm: float,
    ):
        super().__init__(0, 0, length_mm, width_mm)

        self.piece_id = piece_id
        self.length_mm = length_mm
        self.width_mm = width_mm

        self.setPos(x_mm, y_mm)

        self.setBrush(QColor("#dbeafe"))
        self.setPen(QPen(QColor("#1d4ed8"), 3))

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )

        label = QGraphicsSimpleTextItem(piece_id, self)
        label.setFont(QFont("Arial", 40))
        label.setBrush(QColor("#1e3a8a"))
        label.setPos(24, 20)

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            workspace = (
                self.scene().views()[0]
                if self.scene() and self.scene().views()
                else None
            )

            if workspace is not None:
                return workspace.constrain_piece_position(self, value)

        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            workspace = (
                self.scene().views()[0]
                if self.scene() and self.scene().views()
                else None
            )

            if workspace is not None:
                workspace.piece_moved(
                    self.piece_id,
                    value.x(),
                    value.y(),
                )

        return super().itemChange(change, value)

    def set_valid(self):
        self.setBrush(QColor("#bbf7d0"))
        self.setPen(QPen(QColor("#15803d"), 3))

    def set_invalid(self):
        self.setBrush(QColor("#fecaca"))
        self.setPen(QPen(QColor("#dc2626"), 3))

    def set_normal(self):
        if self.isSelected():
            self.setBrush(QColor("#bfdbfe"))
            self.setPen(QPen(QColor("#dc2626"), 10))
        else:
            self.setBrush(QColor("#dbeafe"))
            self.setPen(QPen(QColor("#1d4ed8"), 3))

    def set_rotation(self, angle: int) -> None:
        angle = angle % 180

        if angle == 90:
            self.setRect(0, 0, self.width_mm, self.length_mm)
        else:
            self.setRect(0, 0, self.length_mm, self.width_mm)

        self.setTransformOriginPoint(self.rect().center())
        self.setRotation(0)
