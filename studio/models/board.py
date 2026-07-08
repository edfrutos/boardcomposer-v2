"""Board model for BoardComposer Studio."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StudioBoard:
    """Board data used by the Studio workspace."""

    board_id: str
    length_mm: float
    width_mm: float
    material: str = "Demo"
