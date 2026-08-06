import pytest
from PySide6.QtWidgets import QApplication, QDockWidget, QToolButton

from studio.main_window import MainWindow
from studio.services import StudioServices

BUILT_IN_DOCK_TITLES = {"Explorer", "Inspector", "Timeline", "Comparador", "Asistente"}


@pytest.fixture
def window():
    QApplication.instance() or QApplication([])
    return MainWindow(services=StudioServices())


def _dock(window, title: str) -> QDockWidget:
    return next(d for d in window.findChildren(QDockWidget) if d.windowTitle() == title)


def _title_buttons(dock: QDockWidget) -> list[QToolButton]:
    bar = dock.titleBarWidget()
    return bar.findChildren(QToolButton)


@pytest.mark.parametrize("title", sorted(BUILT_IN_DOCK_TITLES))
def test_every_built_in_dock_has_its_own_titlebar_widget(window, title):
    # Regression: Qt's native dock title bar buttons (float/close) ignore
    # this app's palette entirely — MainWindow must replace the title bar
    # rather than leave the native one in place.
    dock = _dock(window, title)

    assert dock.titleBarWidget() is not None


@pytest.mark.parametrize("title", sorted(BUILT_IN_DOCK_TITLES))
def test_titlebar_float_and_close_buttons_paint_visible_pixels_in_dark_mode(
    window, title
):
    # Regression: the native close/float icons came out near-invisible
    # (dark gray on dark navy) in dark mode — confirmed with a real render,
    # not just forcing QPalette roles. Guard against it coming back.
    window._set_theme("dark")
    dock = _dock(window, title)

    buttons = _title_buttons(dock)
    assert len(buttons) == 2

    for button in buttons:
        image = button.icon().pixmap(12, 12).toImage()
        visible_pixels = sum(
            1
            for y in range(image.height())
            for x in range(image.width())
            if image.pixelColor(x, y).alpha() > 10
        )
        assert visible_pixels > 3, f"'{title}' title bar button painted almost nothing"


def test_titlebar_close_button_closes_the_dock(window):
    window.show()
    dock = _dock(window, "Inspector")
    button = _title_buttons(dock)[1]  # [float, close]

    button.click()

    assert dock.isVisible() is False


def test_titlebar_float_button_toggles_floating(window):
    window.show()
    dock = _dock(window, "Explorer")
    button = _title_buttons(dock)[0]  # [float, close]
    assert dock.isFloating() is False

    button.click()

    assert dock.isFloating() is True
