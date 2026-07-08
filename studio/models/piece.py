"""Piece model for BoardComposer Studio."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StudioPiece:
    """Piece data used by the Studio workspace."""

    piece_id: str
    length_mm: float
    width_mm: float
    material: str = "Demo"
