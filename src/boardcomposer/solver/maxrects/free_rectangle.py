from dataclasses import dataclass


@dataclass(frozen=True)
class FreeRectangle:
    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float

    @property
    def area_mm2(self) -> float:
        return self.length_mm * self.width_mm

    def fits(self, length_mm: float, width_mm: float) -> bool:
        return length_mm <= self.length_mm and width_mm <= self.width_mm
