from dataclasses import dataclass

from .rectangle import Rectangle


@dataclass(frozen=True)
class FreeSpace:
    rectangle: Rectangle

    @property
    def area_mm2(self) -> float:
        return self.rectangle.area_mm2

    @property
    def is_empty(self) -> bool:
        return self.rectangle.length_mm <= 0 or self.rectangle.width_mm <= 0

    def fits(self, rectangle: Rectangle) -> bool:
        return (
            rectangle.length_mm <= self.rectangle.length_mm
            and rectangle.width_mm <= self.rectangle.width_mm
        )

    def split(self, used: Rectangle) -> list["FreeSpace"]:
        if not self.fits(used):
            return [self]

        right_space = FreeSpace(
            Rectangle(
                x_mm=self.rectangle.x_mm + used.length_mm,
                y_mm=self.rectangle.y_mm,
                length_mm=self.rectangle.length_mm - used.length_mm,
                width_mm=used.width_mm,
            )
        )

        bottom_space = FreeSpace(
            Rectangle(
                x_mm=self.rectangle.x_mm,
                y_mm=self.rectangle.y_mm + used.width_mm,
                length_mm=self.rectangle.length_mm,
                width_mm=self.rectangle.width_mm - used.width_mm,
            )
        )

        return [space for space in [right_space, bottom_space] if not space.is_empty]
