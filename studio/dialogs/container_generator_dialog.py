"""Container-template input dialog (IDE-0028).

Gathers the container's outer dimensions and hands them to whichever
template `CONTAINER_TEMPLATES` maps the chosen type to — the combo only
has one entry today ("Caja simple"), but is already driven by the
registry, so a future template needs no changes here, only a new entry in
`studio/containers/`.
"""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)

from studio.containers import CONTAINER_TEMPLATES

MAX_DIMENSION_MM = 100_000.0

_TEMPLATE_LABELS = {
    "caja_simple": "Caja simple (a tope, sin divisores)",
}


class ContainerGeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generar piezas de contenedor")

        self.template_combo = QComboBox()
        for key in CONTAINER_TEMPLATES:
            self.template_combo.addItem(_TEMPLATE_LABELS.get(key, key), userData=key)

        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.length_spin.setSuffix(" mm")
        self.length_spin.setValue(300.0)

        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.width_spin.setSuffix(" mm")
        self.width_spin.setValue(200.0)

        self.height_spin = QDoubleSpinBox()
        self.height_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.height_spin.setSuffix(" mm")
        self.height_spin.setValue(100.0)

        self.thickness_spin = QDoubleSpinBox()
        self.thickness_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.thickness_spin.setSuffix(" mm")
        self.thickness_spin.setValue(19.0)

        self.material_edit = QLineEdit("Demo")
        self.prefix_edit = QLineEdit("caja")

        form = QFormLayout()
        form.addRow("Tipo de contenedor", self.template_combo)
        form.addRow("Largo exterior", self.length_spin)
        form.addRow("Ancho exterior", self.width_spin)
        form.addRow("Alto exterior", self.height_spin)
        form.addRow("Grosor de tablero", self.thickness_spin)
        form.addRow("Material", self.material_edit)
        form.addRow("Prefijo de id", self.prefix_edit)

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
        if not self.prefix_edit.text().strip():
            self.error_label.setText("El contenedor necesita un prefijo de id.")
            self.error_label.show()
            return
        self.accept()

    def template_key(self) -> str:
        return self.template_combo.currentData()

    def values(self) -> dict:
        return {
            "outer_length_mm": self.length_spin.value(),
            "outer_width_mm": self.width_spin.value(),
            "outer_height_mm": self.height_spin.value(),
            "thickness_mm": self.thickness_spin.value(),
            "material": self.material_edit.text().strip() or "Demo",
            "id_prefix": self.prefix_edit.text().strip() or "caja",
        }
