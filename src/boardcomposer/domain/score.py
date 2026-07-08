from dataclasses import dataclass


@dataclass(frozen=True)
class SolutionScore:
    waste_score: float = 0.0
    material_usage_score: float = 0.0
    cuts_score: float = 0.0
    regularity_score: float = 0.0
    grain_score: float = 0.0

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if value < 0:
                raise ValueError(f"{name} no puede ser negativo")

    @property
    def total(self) -> float:
        return (
            self.waste_score
            + self.material_usage_score
            + self.cuts_score
            + self.regularity_score
            + self.grain_score
        )
