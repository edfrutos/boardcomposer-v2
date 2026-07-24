"""Application entry point for BoardComposer Studio."""

import sys

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
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
    services = StudioServices()
    window = MainWindow(services=services)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
