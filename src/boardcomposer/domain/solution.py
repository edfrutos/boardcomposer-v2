from dataclasses import dataclass, field

from boardcomposer.layout.bounds import bounding_rectangle

from .explanation import SolutionExplanation
from .placement import BoardPlacement
from .score import SolutionScore


@dataclass(frozen=True)
class AssemblySolution:
    placements: list[BoardPlacement]
    score: SolutionScore = field(default_factory=SolutionScore)
    explanation: SolutionExplanation = field(default_factory=SolutionExplanation)

    @property
    def used_area_mm2(self) -> float:
        return sum(p.area_mm2 for p in self.placements)

    @property
    def total_length_mm(self) -> float:
        return bounding_rectangle(self.placements).length_mm

    @property
    def total_width_mm(self) -> float:
        return bounding_rectangle(self.placements).width_mm

    @property
    def bounding_area_mm2(self) -> float:
        return bounding_rectangle(self.placements).area_mm2

    @property
    def waste_area_mm2(self) -> float:
        return self.bounding_area_mm2 - self.used_area_mm2

    @property
    def waste_ratio(self) -> float:
        if self.bounding_area_mm2 == 0:
            return 0
        return self.waste_area_mm2 / self.bounding_area_mm2
