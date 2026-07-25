import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Board:
    length_mm: float
    width_mm: float
    thickness_mm: float
    id: str | None = None

    def __post_init__(self) -> None:
        # `<= 0` alone lets NaN through (`nan <= 0` is False) and Infinity
        # (`inf <= 0` is False) — both parse fine from JSON via Python's
        # permissive json.loads and would otherwise reach the solver/export.
        if not math.isfinite(self.length_mm) or self.length_mm <= 0:
            raise ValueError("length_mm debe ser mayor que 0")
        if not math.isfinite(self.width_mm) or self.width_mm <= 0:
            raise ValueError("width_mm debe ser mayor que 0")
        if not math.isfinite(self.thickness_mm) or self.thickness_mm <= 0:
            raise ValueError("thickness_mm debe ser mayor que 0")

    @property
    def area_mm2(self) -> float:
        return self.length_mm * self.width_mm
