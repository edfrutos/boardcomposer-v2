"""Panel content builders for BoardComposer Studio."""

from studio.panels.chat_panel import render_chat
from studio.panels.comparator_panel import render_comparison
from studio.panels.inspector_panel import (
    render_board,
    render_empty,
    render_piece,
    render_project,
)
from studio.panels.timeline_panel import render_activity, render_overview

__all__ = [
    "render_activity",
    "render_board",
    "render_chat",
    "render_comparison",
    "render_empty",
    "render_overview",
    "render_piece",
    "render_project",
]
