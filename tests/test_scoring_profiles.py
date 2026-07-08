from boardcomposer.solver.scoring_weights import (
    balanced,
    compact_first,
    material_first,
)


def test_balanced_profile():
    weights = balanced()

    assert weights.material_utilization == 40.0


def test_material_first_profile():
    weights = material_first()

    assert weights.material_utilization == 60.0


def test_compact_first_profile():
    weights = compact_first()

    assert weights.compactness == 45.0
