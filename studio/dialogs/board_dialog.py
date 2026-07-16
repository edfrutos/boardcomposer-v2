"""Add/edit board dialog (IDE-0013 Fase D)."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
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
        material: str = "Demo",
        id_editable: bool = True,
        existing_ids: frozenset[str] = frozenset(),
    ):
        super().__init__(parent)
        self.setWindowTitle("Tablero")
        self._existing_ids = existing_ids

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

        self.material_edit = QLineEdit(material)

        form = QFormLayout()
        form.addRow("Id", self.id_edit)
        form.addRow("Largo", self.length_spin)
        form.addRow("Ancho", self.width_spin)
        form.addRow("Material", self.material_edit)

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
        board_id = self.id_edit.text().strip()

        if not board_id:
            self.error_label.setText("El tablero necesita un id.")
            self.error_label.show()
            return

        if board_id in self._existing_ids:
            self.error_label.setText(f"Ya existe un tablero con id '{board_id}'.")
            self.error_label.show()
            return

        self.accept()

    def values(self) -> tuple[str, float, float, str]:
        return (
            self.id_edit.text().strip(),
            self.length_spin.value(),
            self.width_spin.value(),
            self.material_edit.text().strip() or "Demo",
        )
