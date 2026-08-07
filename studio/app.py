"""Application entry point for BoardComposer Studio."""

import os
import sys

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from studio.main_window import ANTHROPIC_API_KEY_SETTINGS_KEY, MainWindow
from studio.services import StudioServices
from studio.theme import apply_theme


def main() -> int:
    """Run BoardComposer Studio."""
    app = QApplication(sys.argv)
    # QSettings() (last-opened-project persistence, main_window.py) needs an
    # organization/application name to know where to store its file.
    app.setOrganizationName("BoardComposer")
    app.setApplicationName("BoardComposer Studio")
    apply_theme(app)

    # Bridges a Preferences-stored Anthropic key into the env var
    # boardcomposer.ai actually reads, before StudioServices() resolves the
    # AI provider — an already-exported env var wins, so this only fills
    # the gap for a double-clicked .app that never inherits one from a
    # shell. See MainWindow._set_anthropic_api_key() for the interactive
    # (Preferences dialog) half of this.
    stored_api_key = QSettings().value(ANTHROPIC_API_KEY_SETTINGS_KEY, "")
    if stored_api_key and not os.environ.get("ANTHROPIC_API_KEY"):
        os.environ["ANTHROPIC_API_KEY"] = stored_api_key

    services = StudioServices()
    window = MainWindow(services=services)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
