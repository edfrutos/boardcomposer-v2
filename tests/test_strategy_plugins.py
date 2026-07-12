from boardcomposer.plugins import PluginLoadError
from boardcomposer.solver.scoring_weights import ScoringWeights
from boardcomposer.solver.strategies import (
    OptimizationStrategy,
    available_strategies,
    balanced_strategy,
    strategy_by_name,
    strategy_plugin_errors,
)


def _fake_strategy() -> OptimizationStrategy:
    return OptimizationStrategy(
        name="custom",
        weights=ScoringWeights(),
        generator_names=("horizontal",),
    )


def test_available_strategies_without_plugins_matches_built_ins(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.solver.strategies.discover_plugins",
        lambda group: ({}, []),
    )

    strategies = available_strategies()

    assert set(strategies) == {"balanced", "material", "compact"}


def test_available_strategies_includes_a_plugin_strategy(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.solver.strategies.discover_plugins",
        lambda group: ({"custom": _fake_strategy}, []),
    )

    strategies = available_strategies()

    assert strategies["custom"] is _fake_strategy
    assert "balanced" in strategies


def test_built_in_strategy_wins_over_a_plugin_with_the_same_name(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.solver.strategies.discover_plugins",
        lambda group: ({"balanced": _fake_strategy}, []),
    )

    strategies = available_strategies()

    assert strategies["balanced"] is balanced_strategy


def test_strategy_by_name_resolves_a_plugin_strategy(monkeypatch):
    monkeypatch.setattr(
        "boardcomposer.solver.strategies.discover_plugins",
        lambda group: ({"custom": _fake_strategy}, []),
    )

    strategy = strategy_by_name("custom")

    assert strategy.name == "custom"
    assert strategy.generator_names == ("horizontal",)


def test_strategy_plugin_errors_surfaces_broken_plugins(monkeypatch):
    error = PluginLoadError(name="broken", error="boom")
    monkeypatch.setattr(
        "boardcomposer.solver.strategies.discover_plugins",
        lambda group: ({}, [error]),
    )

    errors = strategy_plugin_errors()

    assert errors == [error]
