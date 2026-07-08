from dataclasses import dataclass


@dataclass(frozen=True)
class SkylineNode:
    x_mm: float
    y_mm: float
    width_mm: float
