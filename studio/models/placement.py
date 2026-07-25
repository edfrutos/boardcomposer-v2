"""Placement model for BoardComposer Studio."""

import math
from dataclasses import dataclass


@dataclass
class StudioPlacement:
    """Placement data for a piece inside a board."""

    piece_id: str
    x_mm: float
    y_mm: float
    board_id: str
    rotated: bool = False
    rotation: int = 0

    def __post_init__(self) -> None:
        # Sólo finitud, no signo: una coordenada negativa es un estado
        # transitorio legítimo (una pieza arrastrada fuera del tablero antes
        # de que la validación de encaje la recoloque), mientras que un NaN
        # llegado de un fichero de proyecto se propaga a la escena de Qt y
        # deja la pieza sin posición calculable.
        for name, value in (("x_mm", self.x_mm), ("y_mm", self.y_mm)):
            if not math.isfinite(value):
                raise ValueError(f"{name} debe ser un número finito")
