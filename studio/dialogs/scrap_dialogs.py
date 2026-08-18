"""Scrap inventory dialogs (IDE-0039)."""

from PySide6.QtWidgets import (
    QAbstractItemView,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from studio.project.scrap_inventory import ScrapRecord

MAX_DIMENSION_MM = 100_000.0


class AddScrapDialog(QDialog):
    def __init__(self, parent=None, *, existing_ids: frozenset[str] = frozenset()):
        super().__init__(parent)
        self.setWindowTitle("Añadir retal al inventario")
        self._existing_ids = existing_ids

        self.id_edit = QLineEdit()

        self.length_spin = QDoubleSpinBox()
        self.length_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.length_spin.setSuffix(" mm")
        self.length_spin.setValue(1.0)

        self.width_spin = QDoubleSpinBox()
        self.width_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.width_spin.setSuffix(" mm")
        self.width_spin.setValue(1.0)

        self.thickness_spin = QDoubleSpinBox()
        self.thickness_spin.setRange(0.01, MAX_DIMENSION_MM)
        self.thickness_spin.setSuffix(" mm")
        self.thickness_spin.setValue(19.0)

        self.material_edit = QLineEdit()
        self.origin_edit = QLineEdit()

        form = QFormLayout()
        form.addRow("Id", self.id_edit)
        form.addRow("Largo", self.length_spin)
        form.addRow("Ancho", self.width_spin)
        form.addRow("Grosor", self.thickness_spin)
        form.addRow("Material", self.material_edit)
        form.addRow("Procedencia", self.origin_edit)

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
        scrap_id = self.id_edit.text().strip()

        if not scrap_id:
            self.error_label.setText("El retal necesita un id.")
            self.error_label.show()
            return

        if scrap_id in self._existing_ids:
            self.error_label.setText(f"Ya existe un retal con id '{scrap_id}'.")
            self.error_label.show()
            return

        self.accept()

    def values(self) -> tuple[str, float, float, float, str, str]:
        return (
            self.id_edit.text().strip(),
            self.length_spin.value(),
            self.width_spin.value(),
            self.thickness_spin.value(),
            self.material_edit.text().strip(),
            self.origin_edit.text().strip(),
        )


_HEADERS = ["Id", "Largo (mm)", "Ancho (mm)", "Grosor (mm)", "Material", "Procedencia"]


class UseScrapDialog(QDialog):
    def __init__(self, parent=None, *, scraps: list[ScrapRecord]):
        super().__init__(parent)
        self.setWindowTitle("Añadir tablero")
        self.resize(640, 360)
        self._scraps = scraps
        # Set by the "Tablero nuevo…" button (IDE-0044): the dialog still
        # rejects in that case (nothing was selected), but the caller needs
        # to tell "cancelled outright" apart from "wants BoardDialog
        # instead" — a plain attribute is simpler than a custom result code.
        self.new_board_requested = False

        self.table = QTableWidget(len(scraps), len(_HEADERS))
        self.table.setHorizontalHeaderLabels(_HEADERS)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)

        for row, scrap in enumerate(scraps):
            values = [
                scrap.scrap_id,
                f"{scrap.length_mm:g}",
                f"{scrap.width_mm:g}",
                f"{scrap.thickness_mm:g}",
                scrap.material,
                scrap.origin,
            ]
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))

        if scraps:
            self.table.selectRow(0)

        # Same fix as CsvImportPreviewDialog/BoardCsvImportPreviewDialog:
        # Id/Material/Procedencia have unpredictable, often long content —
        # they size to it, the numeric columns keep sharing the rest.
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        for column in (0, 4, 5):
            header.setSectionResizeMode(column, QHeaderView.ResizeMode.ResizeToContents)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")
        self.error_label.hide()

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._try_accept)
        buttons.rejected.connect(self.reject)
        new_board_button = buttons.addButton(
            "Tablero nuevo…", QDialogButtonBox.ButtonRole.ActionRole
        )
        new_board_button.clicked.connect(self._request_new_board)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)
        layout.addWidget(self.error_label)
        layout.addWidget(buttons)

    def _try_accept(self) -> None:
        if self.table.currentRow() < 0:
            self.error_label.setText("Selecciona un retal.")
            self.error_label.show()
            return

        self.accept()

    def _request_new_board(self) -> None:
        self.new_board_requested = True
        self.reject()

    def selected_scrap(self) -> ScrapRecord:
        return self._scraps[self.table.currentRow()]
