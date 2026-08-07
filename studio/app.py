"""Application entry point for BoardComposer Studio."""

import os
import sys

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from studio.main_window import (
    AI_PROVIDER_SETTINGS_KEY,
    ANTHROPIC_API_KEY_SETTINGS_KEY,
    GEMINI_API_KEY_SETTINGS_KEY,
    OLLAMA_HOST_SETTINGS_KEY,
    OLLAMA_MODEL_SETTINGS_KEY,
    OPENAI_API_KEY_SETTINGS_KEY,
    MainWindow,
)
from studio.services import StudioServices
from studio.theme import apply_theme

# Maps each Preferences-stored AI setting to the env var boardcomposer.ai
# actually reads for it.
_AI_SETTINGS_TO_ENV_VAR = {
    AI_PROVIDER_SETTINGS_KEY: "BOARDCOMPOSER_AI_PROVIDER",
    ANTHROPIC_API_KEY_SETTINGS_KEY: "ANTHROPIC_API_KEY",
    OPENAI_API_KEY_SETTINGS_KEY: "OPENAI_API_KEY",
    GEMINI_API_KEY_SETTINGS_KEY: "GEMINI_API_KEY",
    OLLAMA_HOST_SETTINGS_KEY: "OLLAMA_HOST",
    OLLAMA_MODEL_SETTINGS_KEY: "OLLAMA_MODEL",
}


def main() -> int:
    """Run BoardComposer Studio."""
    app = QApplication(sys.argv)
    # QSettings() (last-opened-project persistence, main_window.py) needs an
    # organization/application name to know where to store its file.
    app.setOrganizationName("BoardComposer")
    app.setApplicationName("BoardComposer Studio")
    apply_theme(app)

    # Bridges Preferences-stored AI settings (active provider + one
    # credential per provider, IDE-0034/IDE-0036) into the env vars
    # boardcomposer.ai actually reads, before StudioServices() resolves the
    # AI provider — an already-exported env var wins, so this only fills
    # the gap for a double-clicked .app that never inherits one from a
    # shell. See MainWindow._set_ai_preferences() for the interactive
    # (Preferences dialog) half of this.
    settings = QSettings()
    for settings_key, env_var in _AI_SETTINGS_TO_ENV_VAR.items():
        stored_value = settings.value(settings_key, "")
        if stored_value and not os.environ.get(env_var):
            os.environ[env_var] = stored_value

    services = StudioServices()
    window = MainWindow(services=services)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
