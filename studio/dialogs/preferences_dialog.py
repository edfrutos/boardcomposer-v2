"""Preferences dialog (IDE-0025) — theme plus the Anthropic API key
(IDE-0032 follow-up). Idioma/unidades aren't here: neither has real
infrastructure behind it yet (no i18n, the domain works in mm end to end),
so a control for either would do nothing — see IDE-0025 in
docs/masterplan/DOC-004-Backlog.md. The API key is different: real
infrastructure (boardcomposer.ai.default_provider()) already exists and
already reads ANTHROPIC_API_KEY — a double-clicked .app just never
inherits a Terminal's exported env var, so without a field here the
Asistente silently falls back to MockAIProvider with no way to fix it
short of relaunching from a shell.
"""

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

THEME_LABELS = {
    "auto": "Automático (sistema)",
    "light": "Claro",
    "dark": "Oscuro",
}
THEME_KEYS = list(THEME_LABELS)


class PreferencesDialog(QDialog):
    def __init__(
        self,
        parent=None,
        *,
        theme_key: str = "auto",
        anthropic_api_key: str = "",
    ):
        super().__init__(parent)
        self.setWindowTitle("Preferencias")

        self.theme_combo = QComboBox()
        for key in THEME_KEYS:
            self.theme_combo.addItem(THEME_LABELS[key], userData=key)
        self.theme_combo.setCurrentIndex(THEME_KEYS.index(theme_key))

        self.anthropic_api_key_edit = QLineEdit(anthropic_api_key)
        self.anthropic_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.anthropic_api_key_edit.setPlaceholderText("sk-ant-…")
        self.anthropic_api_key_edit.setToolTip(
            "Clave de la API de Anthropic para el Asistente. Vacía = usa la "
            "variable de entorno ANTHROPIC_API_KEY si existe, o respuestas "
            "de ejemplo (MockAIProvider) si no."
        )

        form = QFormLayout()
        form.addRow("Tema", self.theme_combo)
        form.addRow("Clave API de Anthropic", self.anthropic_api_key_edit)

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

    def anthropic_api_key(self) -> str:
        return self.anthropic_api_key_edit.text().strip()
