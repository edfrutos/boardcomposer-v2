"""Preview dialog shown before committing a parsed board CSV import
(IDE-0029), same pattern as `CsvImportPreviewDialog` (IDE-0024) but for
`StudioBoard` (`board_id`) instead of `StudioPiece` (`piece_id`)."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from studio.models import StudioBoard

_HEADERS = ["Id", "Largo (mm)", "Ancho (mm)", "Material", "Grosor (mm)"]


class BoardCsvImportPreviewDialog(QDialog):
    def __init__(self, parent=None, *, boards: list[StudioBoard]):
        super().__init__(parent)
        self.setWindowTitle(f"Importar {len(boards)} tablero(s) desde CSV")
        self.resize(480, 320)

        table = QTableWidget(len(boards), len(_HEADERS))
        table.setHorizontalHeaderLabels(_HEADERS)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.verticalHeader().setVisible(False)

        for row, board in enumerate(boards):
            values = [
                board.board_id,
                f"{board.length_mm:g}",
                f"{board.width_mm:g}",
                board.material,
                f"{board.thickness_mm:g}",
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
