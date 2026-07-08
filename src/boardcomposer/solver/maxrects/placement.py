from dataclasses import dataclass


@dataclass(frozen=True)
class MaxRectsPlacement:
    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float
    rotated: bool = False
