from dataclasses import dataclass


@dataclass(frozen=True)
class Rectangle:
    x_mm: float
    y_mm: float
    length_mm: float
    width_mm: float

    @property
    def right_mm(self) -> float:
        return self.x_mm + self.length_mm

    @property
    def top_mm(self) -> float:
        return self.y_mm + self.width_mm

    @property
    def area_mm2(self) -> float:
        return self.length_mm * self.width_mm

    def overlaps(self, other: "Rectangle") -> bool:
        return not (
            self.right_mm <= other.x_mm
            or other.right_mm <= self.x_mm
            or self.top_mm <= other.y_mm
            or other.top_mm <= self.y_mm
        )
