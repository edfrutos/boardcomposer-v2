"""Line-art icon set for BoardComposer Studio's menu/toolbar actions.

Rendered at runtime from inline SVG paths (parametrized by the current
theme's icon color) via QSvgRenderer -> QPixmap -> QIcon — no binary asset
pipeline, and icons automatically match light/dark mode (studio/theme.py).
"""

from PySide6.QtCore import QByteArray, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

_RENDER_SIZE = 32

_PATHS = {
    "new_project": '<path d="M4 4h9l4 4v12H4z"/><path d="M13 4v4h4"/>',
    "open": '<path d="M4 7h5l2 2h9v9a1 1 0 0 1-1 1H4z"/>'
    '<path d="M4 7V5a1 1 0 0 1 1-1h4l2 2"/>',
    "save": '<path d="M5 4h11l3 3v13H5z"/><path d="M8 4v5h7V4"/>'
    '<rect x="8" y="14" width="7" height="6"/>',
    "add_board": '<rect x="4" y="6" width="16" height="12" rx="1"/>'
    '<path d="M12 10v6M9 13h6"/>',
    "edit_board": '<rect x="4" y="6" width="16" height="12" rx="1"/>'
    '<path d="M14 9l3 3-6 6H8v-3z"/>',
    "add_piece": '<rect x="6" y="8" width="12" height="8" rx="1"/>'
    '<path d="M12 11v2M11 12h2"/>',
    "edit_piece": '<rect x="6" y="8" width="12" height="8" rx="1"/>'
    '<path d="M15 6l3 3-8 8H7v-3z"/>',
    "move_to_board": '<rect x="3" y="10" width="7" height="7" rx="1"/>'
    '<rect x="14" y="6" width="7" height="7" rx="1"/>'
    '<path d="M11 13h6m0 0-3-3m3 3-3 3"/>',
    "kerf": '<path d="M4 12h16"/><path d="M4 8h16"/><path d="M4 16h16"/>',
    "solve": '<path d="M4 20V10l8-6 8 6v10"/><path d="M9 20v-6h6v6"/>',
    "apply": '<path d="M20 6 9 17l-5-5"/>',
    "compare": '<rect x="3" y="4" width="8" height="16" rx="1"/>'
    '<rect x="13" y="4" width="8" height="16" rx="1"/>',
    "export_svg": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/>'
    '<path d="M9 12v5M12 12v5M15 12l-1.5 5L12 15"/>',
    "export_pdf": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4"/>'
    '<path d="M9 17v-4h1.5a1.5 1.5 0 0 1 0 3H9M13 17v-4h2M13 15h1.5M17 17v-4h2"/>',
    "undo": '<path d="M9 7 4 12l5 5"/><path d="M4 12h11a5 5 0 0 1 0 10h-1"/>',
    "redo": '<path d="M15 7l5 5-5 5"/><path d="M20 12H9a5 5 0 0 0 0 10h1"/>',
    "delete": '<path d="M5 7h14"/><path d="M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>'
    '<path d="M7 7l1 13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1l1-13"/>',
    "rotate": '<path d="M4 12a8 8 0 1 1 3 6.2"/><path d="M4 18v-5h5"/>',
    "attach": '<path d="M20.4 11.05 12 19.45a5.5 5.5 0 0 1-7.78-7.78l8.4-8.4a'
    '3.67 3.67 0 0 1 5.19 5.19l-8.41 8.4a1.83 1.83 0 0 1-2.6-2.6l7.78-7.77"/>',
    "send": '<path d="M4 12h14"/><path d="M13 6l6 6-6 6"/>',
    # Explorer tree rows: a full board is one wide flat rectangle; a piece
    # is two smaller offset rectangles, evoking cut-out material rather
    # than a single sheet — silhouette does the distinguishing, not just
    # the label text next to it.
    "board_row": '<rect x="3" y="8" width="18" height="8" rx="1.5"/>',
    "piece_row": '<rect x="4" y="5" width="8" height="8" rx="1"/>'
    '<rect x="13" y="10" width="7" height="7" rx="1"/>',
}


def _build_icon(name: str, color: str) -> QIcon:
    body = _PATHS[name]
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
    )

    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    pixmap = QPixmap(_RENDER_SIZE, _RENDER_SIZE)
    pixmap.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()

    return QIcon(pixmap)


def build_icons(color: str) -> dict[str, QIcon]:
    """One QIcon per action name in _PATHS, all rendered in `color`."""
    return {name: _build_icon(name, color) for name in _PATHS}
