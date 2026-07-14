import pytest

from boardcomposer import Project
from boardcomposer.io import (
    available_importers,
    importer_by_name,
    importer_plugin_errors,
    load_project_from_csv,
    load_project_from_excel,
)
from boardcomposer.plugins import PluginLoadError


def _fake_importer(path):
    return Project()


def test_available_importers_without_plugins_matches_built_ins(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.io.registry.discover_plugins",
        lambda group: ({}, []),
    )

    importers = available_importers()

    assert importers["csv"] is load_project_from_csv
    assert importers["xlsx"] is load_project_from_excel


def test_available_importers_includes_a_plugin_importer(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.io.registry.discover_plugins",
        lambda group: ({"custom": _fake_importer}, []),
    )

    importers = available_importers()

    assert importers["custom"] is _fake_importer
    assert "csv" in importers


def test_built_in_importer_wins_over_a_plugin_with_the_same_name(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.io.registry.discover_plugins",
        lambda group: ({"csv": _fake_importer}, []),
    )

    importers = available_importers()

    assert importers["csv"] is load_project_from_csv


def test_importer_by_name_resolves_a_plugin_importer(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.io.registry.discover_plugins",
        lambda group: ({"custom": _fake_importer}, []),
    )

    importer = importer_by_name("custom")

    assert isinstance(importer("anything"), Project)


def test_importer_by_name_rejects_unknown_importer():
    with pytest.raises(ValueError):
        importer_by_name("not_a_real_importer")


def test_importer_plugin_errors_surfaces_broken_plugins(monkeypatch):
    error = PluginLoadError(name="broken", error="boom")
    monkeypatch.setattr(
        "boardcomposer.io.registry.discover_plugins",
        lambda group: ({}, [error]),
    )

    errors = importer_plugin_errors()

    assert errors == [error]
