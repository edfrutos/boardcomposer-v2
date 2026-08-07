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
        self.resize(640, 360)

        table = QTableWidget(len(pieces), len(_HEADERS))
        table.setHorizontalHeaderLabels(_HEADERS)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
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

        # An equal Stretch on every column squeezed Id/Material — the two
        # with unpredictable, often-long content (e.g. the container
        # generator's "caja_simple-lateral-izquierdo") — down to whatever an
        # even split of the dialog's width happened to leave them, same
        # class of bug as the board picker's combo box. Id/Material size to
        # their actual content instead; the three numeric columns keep
        # sharing the rest.
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(table)
        layout.addWidget(buttons)
