"""Small QPainter-rendered thumbnail of an AssemblySolution, for the
Comparador panel (IDE-0023). Same direct-rectangle drawing as
pdf_export.py, scaled to fit a fixed small canvas and returned as a
base64 PNG data URI, so comparator_panel.py can stay Qt-free (it embeds
the string straight into the HTML table it already builds — no Qt
dependency needed there) while the actual rendering, which does need Qt,
lives here instead.
"""

import base64

from PySide6.QtCore import QBuffer, QIODevice, QRectF
from PySide6.QtGui import QColor, QPainter, QPixmap

from boardcomposer.domain import AssemblySolution
from boardcomposer.layout.bounds import bounding_rectangle

_WIDTH = 120
_HEIGHT = 90
_MARGIN = 4


def render_solution_thumbnail(solution: AssemblySolution) -> str:
    """Returns a `data:image/png;base64,...` URI, or "" if there's
    nothing to draw — same "no placements" guard as the other export
    functions."""
    if not solution.placements:
        return ""

    bounds = bounding_rectangle(solution.placements)
    if bounds.length_mm <= 0 or bounds.width_mm <= 0:
        return ""

    available_w = _WIDTH - 2 * _MARGIN
    available_h = _HEIGHT - 2 * _MARGIN
    scale = min(available_w / bounds.length_mm, available_h / bounds.width_mm)

    pixmap = QPixmap(_WIDTH, _HEIGHT)
    pixmap.fill(QColor("white"))

    painter = QPainter(pixmap)
    painter.translate(_MARGIN, _MARGIN)
    painter.scale(scale, scale)
    painter.setPen(QColor("#333333"))
    painter.setBrush(QColor("#cbd8e8"))

    for placement in solution.placements:
        rect = QRectF(
            placement.x_mm - bounds.x_mm,
            placement.y_mm - bounds.y_mm,
            placement.length_mm,
            placement.width_mm,
        )
        painter.drawRect(rect)
    painter.end()

    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    pixmap.save(buffer, "PNG")
    encoded = base64.b64encode(buffer.data().data()).decode("ascii")
    return f"data:image/png;base64,{encoded}"
