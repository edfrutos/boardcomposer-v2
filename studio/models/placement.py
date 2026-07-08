"""Placement model for BoardComposer Studio."""

from dataclasses import dataclass


@dataclass
class StudioPlacement:
    """Placement data for a piece inside a board."""

    piece_id: str
    x_mm: float
    y_mm: float
    rotated: bool = False
    rotation: int = 0
