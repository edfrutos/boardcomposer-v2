"""Materials catalog dialogs (IDE-0041).

`MaterialDialog` follows the same pure "collect values, validate on
accept" shape as every other entity dialog in this package
(BoardDialog/PieceDialog/AddScrapDialog). `MaterialsLibraryDialog` is a
deliberate departure from that: it owns a `MaterialsLibraryService`
directly and mutates the catalog live (add/edit/delete/import all commit
immediately, no separate MainWindow-mediated step) — appropriate here
because the catalog isn't project/undo state, it's workshop reference
data the user is managing as a list, the same way a contacts or
bookmarks manager works.
"""

from PySide6.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from studio.materials_service import MaterialsLibraryService
from studio.project.materials_csv import MaterialsCsvError
from studio.project.materials_library import MaterialsLibraryError

MAX_DIMENSION_MM = 100_000.0
MAX_PRICE = 1_000_000.0

PRICE_UNIT_LABELS = {"board": "Por tablero", "m2": "Por m²"}
PRICE_UNIT_KEYS = list(PRICE_UNIT_LABELS)


class MaterialDialog(QDialog):
    def __init__(
        self,
        parent=None,
        *,
        material_id: str = "",
        name: str = "",
        thickness_mm: float = 19.0,
        provider: str = "",
        price: float = 0.0,
        price_unit: str = "board",
        id_editable: bool = True,
        existing_ids: frozenset[str] = frozenset(),
    ):
        super().__init__(parent)
        self.setWindowTitle("Material")
        self._existing_ids = existing_ids

        self.id_edit = QLineEdit(material_id)
        self.id_edit.setEnabled(id_editable)

        self.name_edit = QLineEdit(name)

        self.thickness_spin = QDoubleSpinBox()
        self.thickness_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.thickness_spin.setSuffix(" mm")
        self.thickness_spin.setValue(thickness_mm)

        self.provider_edit = QLineEdit(provider)

        self.price_spin = QDoubleSpinBox()
        self.price_spin.setRange(0.0, MAX_PRICE)
        self.price_spin.setDecimals(2)
        self.price_spin.setValue(price)

        self.price_unit_combo = QComboBox()
        for key in PRICE_UNIT_KEYS:
            self.price_unit_combo.addItem(PRICE_UNIT_LABELS[key], key)
        self.price_unit_combo.setCurrentIndex(
            PRICE_UNIT_KEYS.index(price_unit) if price_unit in PRICE_UNIT_KEYS else 0
        )

        form = QFormLayout()
        form.addRow("Id", self.id_edit)
        form.addRow("Nombre", self.name_edit)
        form.addRow("Grosor", self.thickness_spin)
        form.addRow("Proveedor", self.provider_edit)
        form.addRow("Precio", self.price_spin)
        form.addRow("Unidad de precio", self.price_unit_combo)

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
        material_id = self.id_edit.text().strip()

        if not material_id:
            self.error_label.setText("El material necesita un id.")
            self.error_label.show()
            return

        if material_id in self._existing_ids:
            self.error_label.setText(f"Ya existe un material con id '{material_id}'.")
            self.error_label.show()
            return

        if not self.name_edit.text().strip():
            self.error_label.setText("El material necesita un nombre.")
            self.error_label.show()
            return

        self.accept()

    def values(self) -> tuple[str, str, float, str, float, str]:
        return (
            self.id_edit.text().strip(),
            self.name_edit.text().strip(),
            self.thickness_spin.value(),
            self.provider_edit.text().strip(),
            self.price_spin.value(),
            self.price_unit_combo.currentData(),
        )


_HEADERS = ["Id", "Nombre", "Grosor (mm)", "Proveedor", "Precio", "Unidad"]


class MaterialsLibraryDialog(QDialog):
    def __init__(self, parent=None, *, service: MaterialsLibraryService):
        super().__init__(parent)
        self.setWindowTitle("Biblioteca de materiales")
        self.resize(720, 420)
        self._service = service

        self.table = QTableWidget(0, len(_HEADERS))
        self.table.setHorizontalHeaderLabels(_HEADERS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for column in (0, 1, 3):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)

        self.add_button = QPushButton("Añadir…")
        self.edit_button = QPushButton("Editar…")
        self.delete_button = QPushButton("Eliminar")
        self.import_button = QPushButton("Importar CSV…")
        self.export_button = QPushButton("Exportar CSV…")
        self.close_button = QPushButton("Cerrar")

        self.add_button.clicked.connect(self._add_material)
        self.edit_button.clicked.connect(self._edit_material)
        self.delete_button.clicked.connect(self._delete_material)
        self.import_button.clicked.connect(self._import_csv)
        self.export_button.clicked.connect(self._export_csv)
        self.close_button.clicked.connect(self.accept)

        buttons_row = QHBoxLayout()
        buttons_row.addWidget(self.add_button)
        buttons_row.addWidget(self.edit_button)
        buttons_row.addWidget(self.delete_button)
        buttons_row.addStretch()
        buttons_row.addWidget(self.import_button)
        buttons_row.addWidget(self.export_button)
        buttons_row.addStretch()
        buttons_row.addWidget(self.close_button)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.error_label)
        layout.addLayout(buttons_row)

        self._reload()

    def _reload(self) -> None:
        self.error_label.hide()
        materials = self._service.list_materials()
        self.table.setRowCount(len(materials))
        for row, material in enumerate(materials):
            values = [
                material.material_id,
                material.name,
                f"{material.thickness_mm:g}",
                material.provider,
                f"{material.price:.2f}",
                PRICE_UNIT_LABELS.get(material.price_unit, material.price_unit),
            ]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))

    def _selected_material(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        materials = self._service.list_materials()
        return materials[row] if row < len(materials) else None

    def _add_material(self) -> None:
        existing_ids = frozenset(
            material.material_id for material in self._service.list_materials()
        )
        dialog = MaterialDialog(self, existing_ids=existing_ids)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        material_id, name, thickness_mm, provider, price, price_unit = dialog.values()
        try:
            self._service.add(
                material_id, name, thickness_mm, provider, price, price_unit
            )
        except MaterialsLibraryError as error:
            self.error_label.setText(str(error))
            self.error_label.show()
            return
        self._reload()

    def _edit_material(self) -> None:
        material = self._selected_material()
        if material is None:
            self.error_label.setText("Selecciona un material.")
            self.error_label.show()
            return

        dialog = MaterialDialog(
            self,
            material_id=material.material_id,
            name=material.name,
            thickness_mm=material.thickness_mm,
            provider=material.provider,
            price=material.price,
            price_unit=material.price_unit,
            id_editable=False,
        )
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        _, name, thickness_mm, provider, price, price_unit = dialog.values()
        try:
            self._service.update(
                material.material_id, name, thickness_mm, provider, price, price_unit
            )
        except MaterialsLibraryError as error:
            self.error_label.setText(str(error))
            self.error_label.show()
            return
        self._reload()

    def _delete_material(self) -> None:
        material = self._selected_material()
        if material is None:
            self.error_label.setText("Selecciona un material.")
            self.error_label.show()
            return

        confirmed = QMessageBox.question(
            self,
            "Eliminar material",
            f"¿Eliminar '{material.name}' ({material.thickness_mm:g} mm) de la "
            "biblioteca?",
        )
        if confirmed != QMessageBox.StandardButton.Yes:
            return

        try:
            self._service.delete(material.material_id)
        except MaterialsLibraryError as error:
            self.error_label.setText(str(error))
            self.error_label.show()
            return
        self._reload()

    def _import_csv(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Importar biblioteca de materiales (CSV)", "", "CSV (*.csv)"
        )
        if not path:
            return

        try:
            self._service.import_csv(path)
        except (MaterialsCsvError, MaterialsLibraryError) as error:
            self.error_label.setText(str(error))
            self.error_label.show()
            return
        self._reload()

    def _export_csv(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self, "Exportar biblioteca de materiales (CSV)", "", "CSV (*.csv)"
        )
        if not path:
            return

        self._service.export_csv(path)
