import pytest
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QMessageBox

from studio._version import __version__ as STUDIO_VERSION
from studio.main_window import MainWindow
from studio.services import StudioServices


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def test_ayuda_menu_has_an_about_action(window):
    action_texts = {action.text() for action in window._menus["Ayuda"].actions()}

    assert "Acerca de BoardComposer Studio…" in action_texts


def test_about_action_has_the_macos_about_menu_role(window):
    assert window._actions["about"].menuRole() == QAction.MenuRole.AboutRole


def test_about_shows_version_and_developer(window, monkeypatch):
    calls = []
    monkeypatch.setattr(
        QMessageBox,
        "about",
        lambda *args, **kwargs: calls.append((args, kwargs)) or None,
    )

    window._show_about()

    assert len(calls) == 1
    text = calls[0][0][2]
    assert STUDIO_VERSION in text
    assert "EDF Developer" in text
    assert "BoardComposer Studio" in text
