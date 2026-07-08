"""Application entry point for BoardComposer Studio."""

import sys

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.services import StudioServices


def main() -> int:
    """Run BoardComposer Studio."""
    app = QApplication(sys.argv)
    services = StudioServices()
    window = MainWindow(services=services)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
