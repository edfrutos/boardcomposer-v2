"""Preferences dialog (IDE-0025) — currently just the color theme, the only
global setting BoardComposer Studio actually has. Idioma/unidades aren't
here: neither has real infrastructure behind it yet (no i18n, the domain
works in mm end to end), so a control for either would do nothing — see
IDE-0025 in docs/masterplan/DOC-004-Backlog.md.
"""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QVBoxLayout,
)

THEME_LABELS = {
    "auto": "Automático (sistema)",
    "light": "Claro",
    "dark": "Oscuro",
}
THEME_KEYS = list(THEME_LABELS)


class PreferencesDialog(QDialog):
    def __init__(self, parent=None, *, theme_key: str = "auto"):
        super().__init__(parent)
        self.setWindowTitle("Preferencias")

        self.theme_combo = QComboBox()
        for key in THEME_KEYS:
            self.theme_combo.addItem(THEME_LABELS[key], userData=key)
        self.theme_combo.setCurrentIndex(THEME_KEYS.index(theme_key))

        form = QFormLayout()
        form.addRow("Tema", self.theme_combo)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

    def theme_key(self) -> str:
        return self.theme_combo.currentData()
