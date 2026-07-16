"""Move-piece-to-board dialog."""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
)


class MoveToBoardDialog(QDialog):
    def __init__(self, parent=None, *, board_ids: list[str]):
        super().__init__(parent)
        self.setWindowTitle("Mover a tablero")

        self.board_combo = QComboBox()
        self.board_combo.addItems(board_ids)

        form = QFormLayout()
        form.addRow("Tablero destino", self.board_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def selected_board_id(self) -> str:
        return self.board_combo.currentText()
