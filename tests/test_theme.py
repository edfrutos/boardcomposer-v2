import pytest
from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect, QLabel

from studio.theme import (
    DARK,
    LIGHT,
    WARM_DOCK_NAMES,
    apply_elevation,
    apply_theme,
    build_stylesheet,
    detect_color_scheme,
)


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


def test_detect_color_scheme_returns_light_or_dark(app):
    assert detect_color_scheme() in {"light", "dark"}


def test_build_stylesheet_light_uses_the_light_palette():
    stylesheet = build_stylesheet("light")

    assert LIGHT.bg in stylesheet
    assert LIGHT.accent in stylesheet
    # LIGHT.text ("#0f172a") happens to equal DARK.bg, so compare against a
    # dark-only value instead (LIGHT never uses this shade of surface).
    assert DARK.surface not in stylesheet


def test_build_stylesheet_dark_uses_the_dark_palette():
    stylesheet = build_stylesheet("dark")

    assert DARK.bg in stylesheet
    assert DARK.accent in stylesheet
    # LIGHT.bg ("#f8fafc") is unique to the light palette — several other
    # hex values are intentionally shared between the two (e.g. both themes'
    # accent_text is now white).
    assert LIGHT.bg not in stylesheet


def test_build_stylesheet_defaults_to_light_for_unknown_scheme():
    assert build_stylesheet("something-else") == build_stylesheet("light")


def test_apply_theme_sets_the_app_stylesheet_and_returns_the_scheme(app):
    scheme = apply_theme(app, "dark")

    assert scheme == "dark"
    assert DARK.bg in app.styleSheet()


def test_apply_theme_without_a_scheme_detects_one(app):
    scheme = apply_theme(app)

    assert scheme in {"light", "dark"}
    assert app.styleSheet() != ""


def test_build_stylesheet_uses_the_complementary_accent2_in_both_themes():
    assert LIGHT.accent2 in build_stylesheet("light")
    assert DARK.accent2 in build_stylesheet("dark")


def test_build_stylesheet_gives_warm_docks_an_accent2_title_stripe():
    light = build_stylesheet("light")

    for name in WARM_DOCK_NAMES:
        assert f"QDockWidget#{name}::title" in light


def test_build_stylesheet_themes_the_tab_bar_for_tabified_docks():
    # Regression: unstyled QTabBar fell back to native macOS rendering,
    # which doesn't pick up this palette — unselected tab text went
    # near-invisible against the dark surfaces (Timeline/Inspector tabs).
    dark = build_stylesheet("dark")

    assert "QTabBar::tab" in dark
    assert "QTabBar::tab:selected" in dark
    assert DARK.text_muted in dark


def test_build_stylesheet_explorer_selection_is_a_plain_accent_not_a_gradient():
    # Regression: QTreeWidget::item:selected reused the toolbar's 3-stop
    # accent gradient (blue/teal/amber) as its background — painted into
    # the narrow branch/icon column of a selected board or piece row in
    # the Explorer, it read as a stray patch of rainbow color rather than
    # a normal selection highlight.
    for scheme, palette in (("light", LIGHT), ("dark", DARK)):
        stylesheet = build_stylesheet(scheme)
        start = stylesheet.index("QTreeWidget::item:selected {")
        end = stylesheet.index("}", start)
        rule = stylesheet[start:end]

        assert "qlineargradient" not in rule
        assert palette.accent in rule


def test_apply_elevation_attaches_a_drop_shadow(app):
    widget = QLabel()

    effect = apply_elevation(widget, blur_radius=12, y_offset=3, alpha=50)

    assert isinstance(effect, QGraphicsDropShadowEffect)
    assert widget.graphicsEffect() is effect
    assert effect.blurRadius() == 12
    assert effect.color().alpha() == 50
