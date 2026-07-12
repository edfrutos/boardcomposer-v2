import pytest

from boardcomposer.domain import AssemblySolution
from boardcomposer.export import (
    available_exporters,
    exporter_by_name,
    exporter_plugin_errors,
    solution_to_svg,
)
from boardcomposer.plugins import PluginLoadError


def _fake_exporter(solution: AssemblySolution) -> str:
    return "custom-format"


def test_available_exporters_without_plugins_matches_built_ins(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.export.registry.discover_plugins",
        lambda group: ({}, []),
    )

    exporters = available_exporters()

    assert exporters["svg"] is solution_to_svg


def test_available_exporters_includes_a_plugin_exporter(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.export.registry.discover_plugins",
        lambda group: ({"custom": _fake_exporter}, []),
    )

    exporters = available_exporters()

    assert exporters["custom"] is _fake_exporter
    assert "svg" in exporters


def test_built_in_exporter_wins_over_a_plugin_with_the_same_name(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.export.registry.discover_plugins",
        lambda group: ({"svg": _fake_exporter}, []),
    )

    exporters = available_exporters()

    assert exporters["svg"] is solution_to_svg


def test_exporter_by_name_resolves_a_plugin_exporter(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.export.registry.discover_plugins",
        lambda group: ({"custom": _fake_exporter}, []),
    )

    exporter = exporter_by_name("custom")

    assert exporter(AssemblySolution(placements=[])) == "custom-format"


def test_exporter_by_name_rejects_unknown_exporter():
    with pytest.raises(ValueError):
        exporter_by_name("not_a_real_exporter")


def test_exporter_plugin_errors_surfaces_broken_plugins(monkeypatch):
    error = PluginLoadError(name="broken", error="boom")
    monkeypatch.setattr(
        "boardcomposer.export.registry.discover_plugins",
        lambda group: ({}, [error]),
    )

    errors = exporter_plugin_errors()

    assert errors == [error]
