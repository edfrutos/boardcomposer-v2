"""PDF export for the current Studio workspace state (IDE-0005).

Draws the same rectangles + board_id labels as
boardcomposer.export.solution_to_svg(), but rendered via QPainter onto a
QPdfWriter page instead of building an SVG string — PDF generation needs
Qt, which the Core deliberately never depends on (see docs/architecture.md).
"""

from pathlib import Path

from PySide6.QtCore import QMarginsF, QRectF, QSizeF
from PySide6.QtGui import QPageSize, QPainter, QPdfWriter

from studio.export.solution_bridge import studio_project_to_solution
from studio.models import StudioProject

_DPI = 96


def export_project_to_pdf(project: StudioProject, path: str | Path) -> bool:
    solution = studio_project_to_solution(project)
    if not solution.placements:
        return False

    writer = QPdfWriter(str(path))
    writer.setResolution(_DPI)
    writer.setPageSize(
        QPageSize(
            QSizeF(solution.total_length_mm, solution.total_width_mm),
            QPageSize.Unit.Millimeter,
        )
    )
    writer.setPageMargins(QMarginsF(0, 0, 0, 0))

    painter = QPainter(writer)
    px_per_mm = _DPI / 25.4
    painter.scale(px_per_mm, px_per_mm)

    for placement in solution.placements:
        rect = QRectF(
            placement.x_mm, placement.y_mm, placement.length_mm, placement.width_mm
        )
        painter.drawRect(rect)
        painter.drawText(rect.adjusted(2, 2, 0, 0), placement.board_id)

    painter.end()
    return True
