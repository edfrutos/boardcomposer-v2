"""Visual theme for BoardComposer Studio — palette, typography, and QSS.

Bold, high-contrast direction: near-black navy surfaces, a blue→teal→amber
accent range on the toolbar/primary buttons/dock title accent stripe, and
larger corner radii — chosen to read as a "designed" product rather than
default OS chrome, while keeping the workspace canvas's existing
Tailwind-derived colors (board_item.py, board_piece_item.py, grid.py) as the
one accent family the whole app shares.

The amber `accent2` is blue's complementary color on the wheel: it marks the
two most "active" docked panels (Asistente, Comparador) with a warm stripe so
the eye can tell them apart from the structural ones (Explorer, Inspector,
Timeline), which stay on the cool blue accent.
"""

from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QGraphicsDropShadowEffect, QWidget


@dataclass(frozen=True)
class Palette:
    bg: str
    surface: str
    surface_alt: str
    border: str
    text: str
    text_muted: str
    accent: str
    accent_hover: str
    accent_text: str
    accent2: str
    accent2_hover: str
    accent2_text: str
    gradient_start: str
    gradient_end: str


LIGHT = Palette(
    bg="#f8fafc",
    surface="#ffffff",
    surface_alt="#eef2f7",
    border="#dbe3ee",
    text="#0f172a",
    text_muted="#64748b",
    accent="#2563eb",
    accent_hover="#1d4ed8",
    accent_text="#ffffff",
    accent2="#f59e0b",
    accent2_hover="#d97706",
    accent2_text="#1c1206",
    gradient_start="#2563eb",
    gradient_end="#0ea5e9",
)

DARK = Palette(
    bg="#0a0e17",
    surface="#131a26",
    surface_alt="#1b2436",
    border="#2a3548",
    text="#f1f5f9",
    text_muted="#94a3b8",
    accent="#3b82f6",
    accent_hover="#60a5fa",
    accent_text="#ffffff",
    accent2="#fbbf24",
    accent2_hover="#fcd34d",
    accent2_text="#1c1206",
    gradient_start="#3b82f6",
    gradient_end="#22d3ee",
)

# Docks that get the warm (amber) title stripe instead of the default cool
# (blue) one — the two panels the user actively drives (typing, comparing)
# rather than reads passively.
WARM_DOCK_NAMES = ("Asistente", "Comparador")

# Icons sit on the toolbar's colored gradient in both themes, and on a dark
# navy dock/menu surface in dark mode — white reads well in both. The one
# soft spot is light mode's dropdown menus (white icon, near-white surface),
# accepted as a minor trade-off rather than maintaining two icon sets per
# QAction (toolbar and menu currently share the same QAction/QIcon).
ICON_COLOR = "#ffffff"


def detect_color_scheme() -> str:
    """Reads the OS appearance via Qt's own style hints — no heuristics."""
    app = QApplication.instance()
    if app is None:
        return "light"

    return "dark" if app.styleHints().colorScheme() == Qt.ColorScheme.Dark else "light"


def palette_for(scheme: str) -> Palette:
    return DARK if scheme == "dark" else LIGHT


def _rgba(hex_color: str, alpha: int) -> str:
    """`#rrggbb` -> `rgba(r, g, b, alpha)`, for tinted QSS backgrounds that a
    plain hex color can't express."""
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r}, {g}, {b}, {alpha})"


def _gradient(start: str, end: str, angle: str = "x1:0, y1:0, x2:1, y2:0") -> str:
    return f"qlineargradient({angle}, stop:0 {start}, stop:1 {end})"


def _accent_gradient(p: Palette, angle: str = "x1:0, y1:0, x2:1, y2:0") -> str:
    """The toolbar/primary-button gradient: blue into teal into a hint of
    amber, so primary chrome carries both the cool and warm accents rather
    than reading as a single flat hue."""
    return (
        f"qlineargradient({angle}, stop:0 {p.gradient_start}, "
        f"stop:0.65 {p.gradient_end}, stop:1 {p.accent2})"
    )


def apply_elevation(
    widget: QWidget, blur_radius: int = 28, y_offset: int = 6, alpha: int = 90
) -> QGraphicsDropShadowEffect:
    """Gives `widget` a soft drop shadow so it reads as a raised layer with
    real thickness against the flat background, instead of a flush panel
    with just a 1px border. Used on the toolbar and the docked panels —
    docked widgets clip most of the shadow to their allocated rect, but the
    exposed edges (and the full shadow once a panel is floated as its own
    window) still pick it up."""
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(blur_radius)
    effect.setOffset(0, y_offset)
    effect.setColor(QColor(0, 0, 0, alpha))
    widget.setGraphicsEffect(effect)
    return effect


def build_stylesheet(scheme: str) -> str:
    p = palette_for(scheme)
    gradient = _accent_gradient(p)
    gradient_vertical = _accent_gradient(p, "x1:0, y1:0, x2:0, y2:1")
    accent2_gradient = _gradient(p.accent2, p.accent2_hover)

    warm_dock_rules = "".join(
        f"""
    QDockWidget#{name}::title {{
        border-left: 3px solid {p.accent2};
    }}
    """
        for name in WARM_DOCK_NAMES
    )

    return f"""
    QMainWindow, QDialog {{
        background: {p.bg};
        color: {p.text};
    }}

    QLabel {{
        color: {p.text};
    }}

    QMenuBar {{
        background: {p.surface};
        color: {p.text};
        border-bottom: 1px solid {p.border};
        padding: 2px;
    }}
    QMenuBar::item {{
        background: transparent;
        padding: 6px 10px;
        border-radius: 6px;
    }}
    QMenuBar::item:selected {{
        background: {gradient};
        color: {p.accent_text};
    }}

    QMenu {{
        background: {p.surface};
        color: {p.text};
        border: 1px solid {p.border};
        border-radius: 10px;
        padding: 6px;
    }}
    QMenu::item {{
        padding: 7px 24px 7px 14px;
        border-radius: 8px;
    }}
    QMenu::item:selected {{
        background: {gradient};
        color: {p.accent_text};
    }}
    QMenu::separator {{
        height: 1px;
        background: {p.border};
        margin: 6px 10px;
    }}

    QDockWidget {{
        color: {p.text};
        font-weight: 600;
    }}
    QDockWidget::title {{
        background: {p.surface_alt};
        padding: 8px 8px 8px 12px;
        border-bottom: 1px solid {p.border};
        border-left: 3px solid {p.accent};
    }}
    {warm_dock_rules}

    QTreeWidget, QTextEdit, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        background: {p.surface};
        color: {p.text};
        border: 1px solid {p.border};
        border-radius: 10px;
        selection-background-color: {p.accent};
        selection-color: {p.accent_text};
    }}
    QTreeWidget {{
        padding: 4px;
        outline: none;
    }}
    QTreeWidget::item {{
        padding: 5px;
        border-radius: 6px;
    }}
    QTreeWidget::item:selected {{
        background: {gradient};
        color: {p.accent_text};
    }}
    QTextEdit {{
        padding: 10px;
        selection-color: {p.accent_text};
    }}
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        padding: 5px 8px;
    }}
    QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 1px solid {p.accent};
    }}

    QTextEdit#assistantInput {{
        border: 1px solid {p.border};
    }}
    QTextEdit#assistantInput:focus {{
        border: 1px solid {p.accent2};
    }}

    QLabel#assistantAttachmentChip {{
        background: {_rgba(p.accent2, 35)};
        color: {p.text};
        border: 1px solid {p.accent2};
        border-radius: 8px;
        padding: 3px 10px;
    }}

    QPushButton {{
        background: {p.surface_alt};
        color: {p.text};
        border: 1px solid {p.border};
        border-radius: 10px;
        padding: 7px 18px;
    }}
    QPushButton:hover {{
        border-color: {p.accent};
    }}
    QPushButton:default {{
        background: {gradient};
        color: {p.accent_text};
        border: none;
        font-weight: 600;
    }}
    QPushButton:default:hover {{
        background: {gradient_vertical};
    }}

    QToolButton#assistantAttachButton, QToolButton#assistantSendButton {{
        background: {p.surface_alt};
        border: 1px solid {p.border};
        border-radius: 8px;
        padding: 6px;
    }}
    QToolButton#assistantAttachButton:hover {{
        border-color: {p.accent2};
    }}
    QToolButton#assistantSendButton {{
        background: {accent2_gradient};
        border: none;
    }}
    QToolButton#assistantSendButton:hover {{
        background: {p.accent2_hover};
    }}

    QStatusBar {{
        background: {p.surface};
        color: {p.text_muted};
        border-top: 1px solid {p.border};
    }}

    QToolBar {{
        background: {gradient};
        border: none;
        spacing: 2px;
        padding: 6px;
    }}
    QToolButton {{
        border-radius: 8px;
        padding: 7px;
    }}
    QToolButton:hover {{
        background: rgba(255, 255, 255, 60);
    }}
    QToolButton:pressed {{
        background: rgba(255, 255, 255, 100);
    }}
    """


def apply_theme(app: QApplication, scheme: str | None = None) -> str:
    """Applies the light/dark stylesheet; returns the scheme actually used."""
    resolved = scheme or detect_color_scheme()
    app.setStyleSheet(build_stylesheet(resolved))
    return resolved
