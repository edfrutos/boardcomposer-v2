import json

import pytest

from boardcomposer.cli import build_demo_project, main


def test_build_demo_project():
    project = build_demo_project()

    assert len(project.boards) == 2
    assert project.total_area_mm2 == 900000


def test_excel_flag_loads_boards_from_an_excel_file(capsys, monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["boardcomposer", "--excel", "data/samples/basic_boards.xlsx", "--json"],
    )

    main()

    output = json.loads(capsys.readouterr().out)

    assert output["input_boards"] == 3


def test_a_malformed_csv_exits_with_a_message_instead_of_a_traceback(
    tmp_path, monkeypatch
):
    path = tmp_path / "malo.csv"
    path.write_text(
        "id,length_mm,width_mm,thickness_mm\nT1,ancho,300,19\n", encoding="utf-8"
    )
    monkeypatch.setattr("sys.argv", ["boardcomposer", "--csv", str(path)])

    with pytest.raises(SystemExit) as exit_info:
        main()

    # SystemExit con texto: argparse/Python lo imprimen en stderr y salen con
    # código 1, en vez de la traza que salía antes.
    assert "Fila 2" in str(exit_info.value)


def test_a_missing_input_file_exits_with_a_message_instead_of_a_traceback(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(
        "sys.argv", ["boardcomposer", "--csv", str(tmp_path / "no-existe.csv")]
    )

    with pytest.raises(SystemExit) as exit_info:
        main()

    assert "No se pudo abrir" in str(exit_info.value)


def test_plugins_subcommand_prints_a_summary_per_group(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["boardcomposer", "plugins"])

    main()

    output = capsys.readouterr().out

    assert "generators:" in output
    assert "strategies:" in output
    assert "importers:" in output
    assert "exporters:" in output


def test_plugins_subcommand_json_output_is_valid_json(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["boardcomposer", "plugins", "--json"])

    main()

    output = json.loads(capsys.readouterr().out)

    assert set(output) == {"generators", "strategies", "importers", "exporters"}


def test_plugins_subcommand_does_not_run_the_default_solve_flow(capsys, monkeypatch):
    monkeypatch.setattr("sys.argv", ["boardcomposer", "plugins"])

    main()

    output = capsys.readouterr().out

    assert "input_boards" not in output
    assert "No hay soluciones" not in output


def test_csv_and_excel_flags_are_mutually_exclusive(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "boardcomposer",
            "--csv",
            "data/samples/basic_boards.csv",
            "--excel",
            "data/samples/basic_boards.xlsx",
        ],
    )

    try:
        main()
    except SystemExit as exit_error:
        assert exit_error.code != 0
    else:
        raise AssertionError("se esperaba SystemExit por argumentos incompatibles")


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
