from boardcomposer import AssemblySolution, BoardPlacement
from boardcomposer.solver.objectives import (
    compactness,
    material_utilization,
    placed_board_ratio,
    rotation_ratio,
)


def test_material_utilization():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 0, 50, 100, 50),
        ]
    )

    assert material_utilization(solution) == 1.0


def test_compactness():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    assert compactness(solution) == 0.5


def test_rotation_ratio():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50, rotated=True),
            BoardPlacement("B", 0, 50, 100, 50, rotated=False),
        ]
    )

    assert rotation_ratio(solution) == 0.5


def test_placed_board_ratio():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    assert placed_board_ratio(solution, total_boards=2) == 0.5
