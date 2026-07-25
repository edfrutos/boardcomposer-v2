"""Piece model for BoardComposer Studio."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class StudioPiece:
    """Piece data used by the Studio workspace."""

    piece_id: str
    length_mm: float
    width_mm: float
    material: str = "Demo"
    thickness_mm: float = 19.0

    def __post_init__(self) -> None:
        # Ver StudioBoard.__post_init__: mismas rutas de entrada (proyecto
        # JSON, CSV) y mismas consecuencias silenciosas.
        for name, value in (
            ("length_mm", self.length_mm),
            ("width_mm", self.width_mm),
            ("thickness_mm", self.thickness_mm),
        ):
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} debe ser un número finito mayor que 0")
