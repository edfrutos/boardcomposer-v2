import pytest
from PySide6.QtWidgets import QApplication, QDockWidget

from studio.main_window import MainWindow
from studio.services import StudioServices

BUILT_IN_DOCK_TITLES = {"Explorer", "Inspector", "Timeline", "Comparador", "Asistente"}


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _dock(window, title: str) -> QDockWidget:
    return next(d for d in window.findChildren(QDockWidget) if d.windowTitle() == title)


def test_every_built_in_dock_has_a_toggle_action_in_the_ver_menu(window):
    action_texts = {action.text() for action in window._menus["Ver"].actions()}

    assert BUILT_IN_DOCK_TITLES <= action_texts


def test_ver_menu_action_reopens_a_closed_built_in_dock(window):
    window.show()
    dock = _dock(window, "Inspector")
    dock.close()
    assert dock.isVisible() is False

    toggle = next(
        action
        for action in window._menus["Ver"].actions()
        if action.text() == "Inspector"
    )
    toggle.trigger()

    assert dock.isVisible() is True


def test_theme_defaults_to_automatico(window):
    # IDE-0025: theme moved from a "Ver → Tema" radio-button submenu to the
    # Preferences dialog — see test_preferences_dialog.py for the dialog
    # itself and its wiring through MainWindow._open_preferences().
    assert window._current_theme_key == "auto"


def test_selecting_oscuro_applies_the_dark_stylesheet(window):
    from studio.theme import DARK

    window._set_theme("dark")

    assert DARK.bg in QApplication.instance().styleSheet()
    assert window._current_theme_key == "dark"


def test_selecting_claro_applies_the_light_stylesheet(window):
    from studio.theme import LIGHT

    window._set_theme("dark")
    window._set_theme("light")

    assert LIGHT.bg in QApplication.instance().styleSheet()
    assert window._current_theme_key == "light"


def test_preferences_action_has_the_macos_preferences_menu_role(window):
    from PySide6.QtGui import QAction

    assert window._actions["preferences"].menuRole() == QAction.MenuRole.PreferencesRole


def test_open_preferences_applies_the_chosen_theme(window, monkeypatch):
    from PySide6.QtWidgets import QDialog

    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.exec",
        lambda self: QDialog.DialogCode.Accepted,
    )
    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.theme_key", lambda self: "dark"
    )

    window._open_preferences()

    assert window._current_theme_key == "dark"


def test_open_preferences_cancelled_leaves_the_theme_unchanged(window, monkeypatch):
    from PySide6.QtWidgets import QDialog

    monkeypatch.setattr(
        "studio.main_window.PreferencesDialog.exec",
        lambda self: QDialog.DialogCode.Rejected,
    )

    window._open_preferences()

    assert window._current_theme_key == "auto"


def test_theme_choice_persists_across_a_new_window(window):
    from PySide6.QtCore import QSettings

    from studio.main_window import THEME_SETTINGS_KEY, MainWindow
    from studio.services import StudioServices

    window._set_theme("dark")
    assert QSettings().value(THEME_SETTINGS_KEY) == "dark"

    new_window = MainWindow(services=StudioServices())

    assert new_window._current_theme_key == "dark"
