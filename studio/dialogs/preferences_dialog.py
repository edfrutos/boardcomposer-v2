"""Preferences dialog (IDE-0025) — theme plus the AI provider settings
(IDE-0032 follow-up, extended by IDE-0036). Idioma/unidades aren't here:
neither has real infrastructure behind it yet (no i18n, the domain works
in mm end to end), so a control for either would do nothing — see
IDE-0025 in docs/masterplan/DOC-004-Backlog.md. The AI provider fields are
different: real infrastructure (boardcomposer.ai.default_provider()/
provider_by_name()) already exists and already reads these exact env
vars — a double-clicked .app just never inherits a Terminal's exported
env vars, so without fields here the Asistente silently falls back to
MockAIProvider with no way to fix it short of relaunching from a shell.

IDE-0036 adds OpenAI/Gemini/Ollama alongside Anthropic: one field row per
provider (its API key, or host+model for Ollama, which has no key at
all), visible only while that provider is the one selected in "Proveedor
de IA activo" — same QFormLayout.setRowVisible() pattern already used by
ContainerGeneratorDialog (IDE-0028/IDE-0031) to switch a form between
template shapes.
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

AI_PROVIDER_LABELS = {
    "anthropic": "Anthropic (Claude)",
    "openai": "OpenAI (GPT)",
    "gemini": "Google Gemini",
    "ollama": "Ollama (local)",
}
AI_PROVIDER_KEYS = list(AI_PROVIDER_LABELS)


class PreferencesDialog(QDialog):
    def __init__(
        self,
        parent=None,
        *,
        theme_key: str = "auto",
        ai_provider: str = "anthropic",
        anthropic_api_key: str = "",
        openai_api_key: str = "",
        gemini_api_key: str = "",
        ollama_host: str = "",
        ollama_model: str = "",
    ):
        super().__init__(parent)
        self.setWindowTitle("Preferencias")

        self.theme_combo = QComboBox()
        for key in THEME_KEYS:
            self.theme_combo.addItem(THEME_LABELS[key], userData=key)
        self.theme_combo.setCurrentIndex(THEME_KEYS.index(theme_key))

        self.ai_provider_combo = QComboBox()
        for key in AI_PROVIDER_KEYS:
            self.ai_provider_combo.addItem(AI_PROVIDER_LABELS[key], userData=key)
        self.ai_provider_combo.setCurrentIndex(AI_PROVIDER_KEYS.index(ai_provider))
        self.ai_provider_combo.currentIndexChanged.connect(
            self._update_provider_field_visibility
        )

        self.anthropic_api_key_edit = QLineEdit(anthropic_api_key)
        self.anthropic_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.anthropic_api_key_edit.setPlaceholderText("sk-ant-…")

        self.openai_api_key_edit = QLineEdit(openai_api_key)
        self.openai_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_api_key_edit.setPlaceholderText("sk-…")

        self.gemini_api_key_edit = QLineEdit(gemini_api_key)
        self.gemini_api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.gemini_api_key_edit.setPlaceholderText("AIza…")

        self.ollama_host_edit = QLineEdit(ollama_host)
        self.ollama_host_edit.setPlaceholderText("http://localhost:11434")

        self.ollama_model_edit = QLineEdit(ollama_model)
        self.ollama_model_edit.setPlaceholderText("llama3.1")

        self.form = QFormLayout()
        self.form.addRow("Tema", self.theme_combo)
        self.form.addRow("Proveedor de IA activo", self.ai_provider_combo)
        self.form.addRow("Clave API de Anthropic", self.anthropic_api_key_edit)
        self.form.addRow("Clave API de OpenAI", self.openai_api_key_edit)
        self.form.addRow("Clave API de Google Gemini", self.gemini_api_key_edit)
        self.form.addRow("Host de Ollama", self.ollama_host_edit)
        self.form.addRow("Modelo de Ollama", self.ollama_model_edit)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(self.form)
        layout.addWidget(buttons)

        self._update_provider_field_visibility()

    def _update_provider_field_visibility(self) -> None:
        provider = self.ai_provider()
        self.form.setRowVisible(self.anthropic_api_key_edit, provider == "anthropic")
        self.form.setRowVisible(self.openai_api_key_edit, provider == "openai")
        self.form.setRowVisible(self.gemini_api_key_edit, provider == "gemini")
        self.form.setRowVisible(self.ollama_host_edit, provider == "ollama")
        self.form.setRowVisible(self.ollama_model_edit, provider == "ollama")

    def theme_key(self) -> str:
        return self.theme_combo.currentData()

    def ai_provider(self) -> str:
        return self.ai_provider_combo.currentData()

    def anthropic_api_key(self) -> str:
        return self.anthropic_api_key_edit.text().strip()

    def openai_api_key(self) -> str:
        return self.openai_api_key_edit.text().strip()

    def gemini_api_key(self) -> str:
        return self.gemini_api_key_edit.text().strip()

    def ollama_host(self) -> str:
        return self.ollama_host_edit.text().strip()

    def ollama_model(self) -> str:
        return self.ollama_model_edit.text().strip()
