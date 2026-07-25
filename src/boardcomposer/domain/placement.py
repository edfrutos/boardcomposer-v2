import math
from dataclasses import dataclass


@dataclass(frozen=True)
class BoardPlacement:
    board_id: str
    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float
    rotated: bool = False

    def __post_init__(self) -> None:
        # Los comparadores por sí solos dejan pasar NaN (`nan < 0` es False) e
        # Infinity — ambos se parsean sin problema desde JSON. Ver
        # Board.__post_init__.
        if not math.isfinite(self.x_mm) or self.x_mm < 0:
            raise ValueError("x_mm debe ser un número finito no negativo")
        if not math.isfinite(self.y_mm) or self.y_mm < 0:
            raise ValueError("y_mm debe ser un número finito no negativo")
        if not math.isfinite(self.length_mm) or self.length_mm <= 0:
            raise ValueError("length_mm debe ser un número finito mayor que 0")
        if not math.isfinite(self.width_mm) or self.width_mm <= 0:
            raise ValueError("width_mm debe ser un número finito mayor que 0")

    @property
    def area_mm2(self) -> float:
        return self.length_mm * self.width_mm

    @property
    def right_mm(self) -> float:
        return self.x_mm + self.length_mm

    @property
    def top_mm(self) -> float:
        return self.y_mm + self.width_mm
