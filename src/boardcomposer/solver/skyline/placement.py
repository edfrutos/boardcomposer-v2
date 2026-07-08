from dataclasses import dataclass


@dataclass(frozen=True)
class SkylinePlacement:
    x_mm: float
    y_mm: float
    rotated: bool = False
