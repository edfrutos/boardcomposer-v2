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


def test_theme_menu_defaults_to_automatico_checked(window):
    assert window._theme_actions["auto"].isChecked() is True
    assert window._theme_actions["light"].isChecked() is False
    assert window._theme_actions["dark"].isChecked() is False


def test_selecting_oscuro_applies_the_dark_stylesheet(window):
    from studio.theme import DARK

    window._theme_actions["dark"].trigger()

    assert DARK.bg in QApplication.instance().styleSheet()
    assert window._theme_actions["dark"].isChecked() is True


def test_selecting_claro_applies_the_light_stylesheet(window):
    from studio.theme import LIGHT

    window._theme_actions["dark"].trigger()
    window._theme_actions["light"].trigger()

    assert LIGHT.bg in QApplication.instance().styleSheet()
    assert window._theme_actions["light"].isChecked() is True


def test_theme_actions_are_mutually_exclusive(window):
    window._theme_actions["dark"].trigger()

    assert window._theme_actions["dark"].isChecked() is True
    assert window._theme_actions["auto"].isChecked() is False
