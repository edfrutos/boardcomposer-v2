import pytest
from PySide6.QtWidgets import QApplication

from studio.icons import _PATHS, build_icons


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


def test_build_icons_returns_one_icon_per_path(app):
    icons = build_icons("#334155")

    assert set(icons) == set(_PATHS)


def test_build_icons_produces_non_null_pixmaps(app):
    icons = build_icons("#334155")

    for icon in icons.values():
        assert icon.pixmap(32, 32).isNull() is False


def test_build_icons_actually_paints_visible_pixels(app):
    icons = build_icons("#334155")

    for name, icon in icons.items():
        image = icon.pixmap(32, 32).toImage()
        visible_pixels = sum(
            1
            for y in range(32)
            for x in range(32)
            if image.pixelColor(x, y).alpha() > 10
        )
        assert visible_pixels > 5, f"icon '{name}' painted almost nothing"
