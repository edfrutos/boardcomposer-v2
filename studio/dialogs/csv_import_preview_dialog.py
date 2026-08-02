"""Preview dialog shown before committing a parsed CSV import (IDE-0024).

`load_pieces_from_csv()` already validates the whole file up front —
all-or-nothing, same as before this dialog existed. This only adds a
confirmation step between "the file parsed successfully" and "the pieces
are actually added to the project", so the user sees what's about to be
imported instead of finding out after the fact.
"""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from studio.models import StudioPiece

_HEADERS = ["Id", "Largo (mm)", "Ancho (mm)", "Material", "Grosor (mm)"]


class CsvImportPreviewDialog(QDialog):
    def __init__(self, parent=None, *, pieces: list[StudioPiece]):
        super().__init__(parent)
        self.setWindowTitle(f"Importar {len(pieces)} pieza(s) desde CSV")
        self.resize(480, 320)

        table = QTableWidget(len(pieces), len(_HEADERS))
        table.setHorizontalHeaderLabels(_HEADERS)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)

        for row, piece in enumerate(pieces):
            values = [
                piece.piece_id,
                f"{piece.length_mm:g}",
                f"{piece.width_mm:g}",
                piece.material,
                f"{piece.thickness_mm:g}",
            ]
            for column, value in enumerate(values):
                table.setItem(row, column, QTableWidgetItem(value))

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(table)
        layout.addWidget(buttons)
