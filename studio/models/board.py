"""Board model for BoardComposer Studio."""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class StudioBoard:
    """Board data used by the Studio workspace."""

    board_id: str
    length_mm: float
    width_mm: float
    material: str = "Demo"
    thickness_mm: float = 19.0

    def __post_init__(self) -> None:
        # Mismo invariante que el Board del Core: las dimensiones llegan de
        # ficheros de proyecto y de CSV, donde float() acepta "nan"/"inf" y
        # nadie garantiza el signo. Sin esto un tablero de -500 mm se dibuja
        # invertido y rompe la colocación en silencio.
        for name, value in (
            ("length_mm", self.length_mm),
            ("width_mm", self.width_mm),
            ("thickness_mm", self.thickness_mm),
        ):
            if not math.isfinite(value) or value <= 0:
                raise ValueError(f"{name} debe ser un número finito mayor que 0")
