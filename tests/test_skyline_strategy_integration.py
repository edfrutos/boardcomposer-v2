from boardcomposer.solver.strategies import material_first_strategy


def test_material_strategy_enables_skyline_generator():
    assert "skyline" in material_first_strategy().generator_names
