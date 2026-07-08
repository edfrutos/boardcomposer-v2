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
        if self.x_mm < 0:
            raise ValueError("x_mm no puede ser negativo")
        if self.y_mm < 0:
            raise ValueError("y_mm no puede ser negativo")
        if self.length_mm <= 0:
            raise ValueError("length_mm debe ser mayor que 0")
        if self.width_mm <= 0:
            raise ValueError("width_mm debe ser mayor que 0")

    @property
    def area_mm2(self) -> float:
        return self.length_mm * self.width_mm

    @property
    def right_mm(self) -> float:
        return self.x_mm + self.length_mm

    @property
    def top_mm(self) -> float:
        return self.y_mm + self.width_mm
