from dataclasses import dataclass


@dataclass(frozen=True)
class ScoringWeights:
    material_utilization: float = 40.0
    placed_boards: float = 30.0
    compactness: float = 20.0
    rotation_penalty: float = 10.0


def balanced() -> ScoringWeights:
    return ScoringWeights()


def material_first() -> ScoringWeights:
    return ScoringWeights(
        material_utilization=60.0,
        placed_boards=25.0,
        compactness=10.0,
        rotation_penalty=5.0,
    )


def compact_first() -> ScoringWeights:
    return ScoringWeights(
        material_utilization=30.0,
        placed_boards=20.0,
        compactness=45.0,
        rotation_penalty=5.0,
    )
