"""Saw kerf (cut width) configuration dialog."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QVBoxLayout,
)

MAX_KERF_MM = 50.0


class KerfDialog(QDialog):
    def __init__(self, parent=None, *, kerf_mm: float = 0.0):
        super().__init__(parent)
        self.setWindowTitle("Ancho de sierra")

        self.kerf_spin = QDoubleSpinBox()
        self.kerf_spin.setRange(0.0, MAX_KERF_MM)
        self.kerf_spin.setSuffix(" mm")
        self.kerf_spin.setValue(kerf_mm)

        form = QFormLayout()
        form.addRow("Ancho de corte", self.kerf_spin)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def kerf_mm(self) -> float:
        return self.kerf_spin.value()
