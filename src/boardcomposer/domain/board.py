from dataclasses import dataclass


@dataclass(frozen=True)
class Board:
    length_mm: float
    width_mm: float
    thickness_mm: float
    id: str | None = None

    def __post_init__(self) -> None:
        if self.length_mm <= 0:
            raise ValueError("length_mm debe ser mayor que 0")
        if self.width_mm <= 0:
            raise ValueError("width_mm debe ser mayor que 0")
        if self.thickness_mm <= 0:
            raise ValueError("thickness_mm debe ser mayor que 0")

    @property
    def area_mm2(self) -> float:
        return self.length_mm * self.width_mm
