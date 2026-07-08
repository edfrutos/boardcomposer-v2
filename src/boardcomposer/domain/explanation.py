from dataclasses import dataclass, field


@dataclass(frozen=True)
class SolutionExplanation:
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
