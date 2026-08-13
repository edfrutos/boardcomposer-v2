"""Add/edit piece dialog (IDE-0013 Fase D)."""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)

MAX_DIMENSION_MM = 100_000.0
MAX_QUANTITY = 999


class PieceDialog(QDialog):
    def __init__(
        self,
        parent=None,
        *,
        piece_id: str = "",
        length_mm: float = 1.0,
        width_mm: float = 1.0,
        material: str = "Demo",
        thickness_mm: float = 19.0,
        id_editable: bool = True,
        existing_ids: frozenset[str] = frozenset(),
        materials: list[str] | None = None,
    ):
        super().__init__(parent)
        self.setWindowTitle("Pieza")
        self._existing_ids = existing_ids

        self.id_edit = QLineEdit(piece_id)
        self.id_edit.setEnabled(id_editable)

        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.length_spin.setSuffix(" mm")
        self.length_spin.setValue(length_mm)

        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.width_spin.setSuffix(" mm")
        self.width_spin.setValue(width_mm)

        self.thickness_spin = QDoubleSpinBox()
        self.thickness_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.thickness_spin.setSuffix(" mm")
        self.thickness_spin.setValue(thickness_mm)

        # Editable combo (IDE-0041) — same reasoning as BoardDialog.
        self.material_edit = QComboBox()
        self.material_edit.setEditable(True)
        self.material_edit.addItems(materials or [])
        self.material_edit.setCurrentText(material)

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, MAX_QUANTITY)
        self.quantity_spin.setValue(1)

        form = QFormLayout()
        form.addRow("Id", self.id_edit)
        form.addRow("Largo", self.length_spin)
        form.addRow("Ancho", self.width_spin)
        form.addRow("Grosor", self.thickness_spin)
        form.addRow("Material", self.material_edit)
        if id_editable:
            form.addRow("Cantidad", self.quantity_spin)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._try_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(self.error_label)
        layout.addWidget(buttons)

    def _try_accept(self) -> None:
        piece_id = self.id_edit.text().strip()

        if not piece_id:
            self.error_label.setText("La pieza necesita un id.")
            self.error_label.show()
            return

        if piece_id in self._existing_ids:
            self.error_label.setText(f"Ya existe una pieza con id '{piece_id}'.")
            self.error_label.show()
            return

        self.accept()

    def values(self) -> tuple[str, float, float, str, float]:
        return (
            self.id_edit.text().strip(),
            self.length_spin.value(),
            self.width_spin.value(),
            self.material_edit.currentText().strip() or "Demo",
            self.thickness_spin.value(),
        )

    def quantity(self) -> int:
        return self.quantity_spin.value()
