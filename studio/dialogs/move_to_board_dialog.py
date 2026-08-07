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
        self.setMinimumWidth(320)

        self.board_combo = QComboBox()
        self.board_combo.addItems(board_ids)
        # Default sizing goes off the combo's own (initially narrow) width,
        # not its widest entry — with real board ids that share a long
        # prefix (TAB-A01, TAB-A02, ...) both the closed combo and its
        # dropdown truncated to something like "TAB-A0" for every item,
        # making them indistinguishable from each other.
        self.board_combo.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )

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
