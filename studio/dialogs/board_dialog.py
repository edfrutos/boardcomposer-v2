"""Add/edit board dialog (IDE-0013 Fase D)."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

MAX_DIMENSION_MM = 100_000.0


class BoardDialog(QDialog):
    def __init__(
        self,
        parent=None,
        *,
        board_id: str = "",
        length_mm: float = 1.0,
        width_mm: float = 1.0,
        id_editable: bool = True,
    ):
        super().__init__(parent)
        self.setWindowTitle("Tablero")

        self.id_edit = QLineEdit(board_id)
        self.id_edit.setEnabled(id_editable)

        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.length_spin.setSuffix(" mm")
        self.length_spin.setValue(length_mm)

        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.width_spin.setSuffix(" mm")
        self.width_spin.setValue(width_mm)

        form = QFormLayout()
        form.addRow("Id", self.id_edit)
        form.addRow("Largo", self.length_spin)
        form.addRow("Ancho", self.width_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def values(self) -> tuple[str, float, float]:
        return (
            self.id_edit.text().strip(),
            self.length_spin.value(),
            self.width_spin.value(),
        )
