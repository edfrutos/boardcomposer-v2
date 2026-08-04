"""Container-template input dialog (IDE-0028/IDE-0031).

Gathers the parameters for whichever template `CONTAINER_TEMPLATES` maps
the chosen type to and hands them over via `values()`. Each template has
its own parameter shape (caja_simple takes outer dimensions directly,
cajón sin rieles takes a cabinet opening plus clearance) so the combo
selection toggles which form rows are visible — adding a template means a
new set of rows plus a new `values()` branch, not a new dialog.
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
    "cajon_sin_rieles": "Cajón sin rieles (por hueco de mueble + holgura)",
}

_PREFIX_DEFAULTS = {
    "caja_simple": "caja",
    "cajon_sin_rieles": "cajon",
}


class ContainerGeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generar piezas de contenedor")

        self.template_combo = QComboBox()
        for key in CONTAINER_TEMPLATES:
            self.template_combo.addItem(_TEMPLATE_LABELS.get(key, key), userData=key)
        self.template_combo.currentIndexChanged.connect(self._update_field_visibility)

        self.length_spin = self._make_spin(300.0)
        self.width_spin = self._make_spin(200.0)
        self.height_spin = self._make_spin(100.0)

        self.opening_length_spin = self._make_spin(300.0)
        self.opening_height_spin = self._make_spin(100.0)
        self.depth_spin = self._make_spin(200.0)
        self.clearance_spin = QDoubleSpinBox()
        self.clearance_spin.setRange(0.0, MAX_DIMENSION_MM)
        self.clearance_spin.setSuffix(" mm")
        self.clearance_spin.setValue(1.5)

        self.thickness_spin = self._make_spin(19.0)

        self.material_edit = QLineEdit("Demo")
        self.prefix_edit = QLineEdit("caja")

        self.form = QFormLayout()
        self.form.addRow("Tipo de contenedor", self.template_combo)
        self.form.addRow("Largo exterior", self.length_spin)
        self.form.addRow("Ancho exterior", self.width_spin)
        self.form.addRow("Alto exterior", self.height_spin)
        self.form.addRow("Ancho del hueco", self.opening_length_spin)
        self.form.addRow("Alto del hueco", self.opening_height_spin)
        self.form.addRow("Profundidad del cajón", self.depth_spin)
        self.form.addRow("Holgura por lado", self.clearance_spin)
        self.form.addRow("Grosor de tablero", self.thickness_spin)
        self.form.addRow("Material", self.material_edit)
        self.form.addRow("Prefijo de id", self.prefix_edit)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._try_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(self.form)
        layout.addWidget(self.error_label)
        layout.addWidget(buttons)

        self._update_field_visibility()

    def _make_spin(self, default: float) -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(0.01, MAX_DIMENSION_MM)
        spin.setSuffix(" mm")
        spin.setValue(default)
        return spin

    def _update_field_visibility(self) -> None:
        is_drawer = self.template_key() == "cajon_sin_rieles"
        for widget in (self.length_spin, self.width_spin, self.height_spin):
            self.form.setRowVisible(widget, not is_drawer)
        for widget in (
            self.opening_length_spin,
            self.opening_height_spin,
            self.depth_spin,
            self.clearance_spin,
        ):
            self.form.setRowVisible(widget, is_drawer)

        default_prefix = _PREFIX_DEFAULTS.get(self.template_key(), "caja")
        if self.prefix_edit.text().strip() in _PREFIX_DEFAULTS.values():
            self.prefix_edit.setText(default_prefix)

    def _try_accept(self) -> None:
        if not self.prefix_edit.text().strip():
            self.error_label.setText("El contenedor necesita un prefijo de id.")
            self.error_label.show()
            return
        self.accept()

    def template_key(self) -> str:
        return self.template_combo.currentData()

    def values(self) -> dict:
        default_prefix = _PREFIX_DEFAULTS.get(self.template_key(), "caja")
        material = self.material_edit.text().strip() or "Demo"
        id_prefix = self.prefix_edit.text().strip() or default_prefix

        if self.template_key() == "cajon_sin_rieles":
            return {
                "opening_length_mm": self.opening_length_spin.value(),
                "opening_height_mm": self.opening_height_spin.value(),
                "depth_mm": self.depth_spin.value(),
                "clearance_mm": self.clearance_spin.value(),
                "thickness_mm": self.thickness_spin.value(),
                "material": material,
                "id_prefix": id_prefix,
            }

        return {
            "outer_length_mm": self.length_spin.value(),
            "outer_width_mm": self.width_spin.value(),
            "outer_height_mm": self.height_spin.value(),
            "thickness_mm": self.thickness_spin.value(),
            "material": material,
            "id_prefix": id_prefix,
        }
