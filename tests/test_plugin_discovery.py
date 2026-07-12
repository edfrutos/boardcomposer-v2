from importlib.metadata import EntryPoint

from boardcomposer.plugins import discover_plugins
from boardcomposer.solver.strategies import balanced_strategy


def _entry_point(name: str, value: str, group: str) -> EntryPoint:
    return EntryPoint(name=name, value=value, group=group)


def test_discover_plugins_resolves_valid_entry_points(monkeypatch):
    entry_point = _entry_point(
        "demo",
        "boardcomposer.solver.strategies:balanced_strategy",
        "boardcomposer.test_group",
    )
    monkeypatch.setattr(
        "boardcomposer.plugins.discovery.entry_points",
        lambda group: [entry_point] if group == "boardcomposer.test_group" else [],
    )

    plugins, errors = discover_plugins("boardcomposer.test_group")

    assert errors == []
    assert plugins["demo"] is balanced_strategy


def test_discover_plugins_returns_empty_for_unknown_group(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.plugins.discovery.entry_points", lambda group: []
    )

    plugins, errors = discover_plugins("boardcomposer.nothing_here")

    assert plugins == {}
    assert errors == []


def test_discover_plugins_captures_broken_entry_point_without_raising(monkeypatch):
    entry_point = _entry_point(
        "broken", "nonexistent_module_xyz:whatever", "boardcomposer.test_group"
    )
    monkeypatch.setattr(
        "boardcomposer.plugins.discovery.entry_points",
        lambda group: [entry_point],
    )

    plugins, errors = discover_plugins("boardcomposer.test_group")

    assert plugins == {}
    assert len(errors) == 1
    assert errors[0].name == "broken"


def test_discover_plugins_one_broken_does_not_block_others(monkeypatch):
    good = _entry_point(
        "good", "boardcomposer.solver.strategies:balanced_strategy", "g"
    )
    bad = _entry_point("bad", "nonexistent_module_xyz:whatever", "g")
    monkeypatch.setattr(
        "boardcomposer.plugins.discovery.entry_points",
        lambda group: [good, bad],
    )

    plugins, errors = discover_plugins("g")

    assert plugins["good"] is balanced_strategy
    assert [error.name for error in errors] == ["bad"]
