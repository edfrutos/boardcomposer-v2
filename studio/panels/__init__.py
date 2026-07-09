"""Panel content builders for BoardComposer Studio."""

from studio.panels.comparator_panel import render_comparison
from studio.panels.inspector_panel import (
    render_board,
    render_empty,
    render_piece,
    render_project,
)

__all__ = [
    "render_board",
    "render_comparison",
    "render_empty",
    "render_piece",
    "render_project",
]
