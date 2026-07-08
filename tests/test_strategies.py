import pytest

from boardcomposer.solver.strategies import (
    balanced_strategy,
    compact_first_strategy,
    material_first_strategy,
    strategy_by_name,
)


def test_balanced_strategy():
    strategy = balanced_strategy()

    assert strategy.name == "balanced"
    assert strategy.weights.material_utilization == 40.0


def test_material_first_strategy():
    strategy = material_first_strategy()

    assert strategy.name == "material"
    assert strategy.weights.material_utilization == 60.0


def test_compact_first_strategy():
    strategy = compact_first_strategy()

    assert strategy.name == "compact"
    assert strategy.weights.compactness == 45.0


def test_strategy_by_name_rejects_unknown_strategy():
    with pytest.raises(ValueError):
        strategy_by_name("unknown")


def test_strategy_defines_generators():
    assert "horizontal" in balanced_strategy().generator_names
    assert "vertical" in compact_first_strategy().generator_names
    assert "horizontal" not in compact_first_strategy().generator_names


def test_material_strategy_uses_skyline():
    assert "skyline" in material_first_strategy().generator_names


def test_material_strategy_uses_maxrects():
    assert "maxrects" in material_first_strategy().generator_names
