from boardcomposer import Board, Project
from boardcomposer.plugins import PluginLoadError
from boardcomposer.solver.generators import (
    available_generators,
    generator_plugin_errors,
    generators_by_name,
    skyline_generator,
)


def _fake_generator(project: Project):
    return []


def test_available_generators_without_plugins_matches_built_ins(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.solver.generators.discover_plugins",
        lambda group: ({}, []),
    )

    generators = available_generators()

    assert "horizontal" in generators
    assert "skyline" in generators


def test_available_generators_includes_a_plugin_generator(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.solver.generators.discover_plugins",
        lambda group: ({"custom": _fake_generator}, []),
    )

    generators = available_generators()

    assert generators["custom"] is _fake_generator
    assert "horizontal" in generators


def test_built_in_generator_wins_over_a_plugin_with_the_same_name(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.solver.generators.discover_plugins",
        lambda group: ({"skyline": _fake_generator}, []),
    )

    generators = available_generators()

    assert generators["skyline"] is skyline_generator


def test_generators_by_name_resolves_a_plugin_generator(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.solver.generators.discover_plugins",
        lambda group: ({"custom": _fake_generator}, []),
    )

    generator = generators_by_name(["custom"])[0]
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    assert generator(project) == []


def test_generator_plugin_errors_surfaces_broken_plugins(monkeypatch):
    error = PluginLoadError(name="broken", error="boom")
    monkeypatch.setattr(
        "boardcomposer.solver.generators.discover_plugins",
        lambda group: ({}, [error]),
    )

    errors = generator_plugin_errors()

    assert errors == [error]
