from dataclasses import dataclass, field

from .free_space import FreeSpace
from .rectangle import Rectangle


@dataclass
class FreeSpaceManager:
    spaces: list[FreeSpace] = field(default_factory=list)

    @classmethod
    def from_bounds(cls, length_mm: float, width_mm: float) -> "FreeSpaceManager":
        return cls(spaces=[FreeSpace(Rectangle(0, 0, length_mm, width_mm))])

    def find_space_for(self, rectangle: Rectangle) -> FreeSpace | None:
        for space in self.spaces:
            if space.fits(rectangle):
                return space
        return None

    def place(self, rectangle: Rectangle) -> bool:
        space = self.find_space_for(rectangle)

        if space is None:
            return False

        self.spaces.remove(space)
        self.spaces.extend(space.split(rectangle))
        return True

    @property
    def free_area_mm2(self) -> float:
        return sum(space.area_mm2 for space in self.spaces)
