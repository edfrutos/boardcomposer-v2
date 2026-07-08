from boardcomposer.cli import build_demo_project


def test_build_demo_project():
    project = build_demo_project()

    assert len(project.boards) == 2
    assert project.total_area_mm2 == 900000


def test_cli_project_constraints_from_cli_options():
    from boardcomposer import ProjectConstraints

    constraints = ProjectConstraints(
        max_length_mm=2500,
        max_width_mm=600,
        **{"allow_rotation": True},
    )

    assert constraints.max_length_mm == 2500
    assert constraints.max_width_mm == 600
    assert constraints.allow_rotation is True


def test_strategy_argument_is_supported():
    from boardcomposer.solver.strategies import strategy_by_name

    strategy = strategy_by_name("material")

    assert strategy.name == "material"
    assert strategy.weights.material_utilization == 60.0


def test_cli_json_fields_are_stable():
    from boardcomposer.solver.strategies import strategy_by_name

    strategy = strategy_by_name("compact")

    assert strategy.name == "compact"
    assert strategy.generator_names == ("vertical", "free_space")
