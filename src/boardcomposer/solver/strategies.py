from collections.abc import Callable
from dataclasses import dataclass

from boardcomposer.plugins import PluginLoadError, discover_plugins
from boardcomposer.solver.scoring_weights import (
    ScoringWeights,
    balanced,
    compact_first,
    material_first,
)

STRATEGY_PLUGIN_GROUP = "boardcomposer.strategies"


@dataclass(frozen=True)
class OptimizationStrategy:
    name: str
    weights: ScoringWeights
    generator_names: tuple[str, ...]


def balanced_strategy() -> OptimizationStrategy:
    return OptimizationStrategy(
        name="balanced",
        weights=balanced(),
        generator_names=("horizontal", "vertical", "free_space"),
    )


def material_first_strategy() -> OptimizationStrategy:
    return OptimizationStrategy(
        name="material",
        weights=material_first(),
        generator_names=("horizontal", "vertical", "free_space", "skyline", "maxrects"),
    )


def compact_first_strategy() -> OptimizationStrategy:
    return OptimizationStrategy(
        name="compact",
        weights=compact_first(),
        generator_names=("vertical", "free_space"),
    )


STRATEGY_FACTORIES: dict[str, Callable[[], OptimizationStrategy]] = {
    "balanced": balanced_strategy,
    "material": material_first_strategy,
    "compact": compact_first_strategy,
}


def available_strategies() -> dict[str, Callable[[], OptimizationStrategy]]:
    """STRATEGY_FACTORIES más las estrategias registradas por plugins
    instalados (grupo STRATEGY_PLUGIN_GROUP). Las integradas siempre
    ganan: un plugin no puede sustituir una estrategia existente."""
    plugins, _errors = discover_plugins(STRATEGY_PLUGIN_GROUP)
    return {**plugins, **STRATEGY_FACTORIES}


def strategy_plugin_errors() -> list[PluginLoadError]:
    """Plugins de estrategias instalados que fallaron al cargarse."""
    _plugins, errors = discover_plugins(STRATEGY_PLUGIN_GROUP)
    return errors


def strategy_by_name(name: str) -> OptimizationStrategy:
    strategies = available_strategies()

    try:
        return strategies[name]()
    except KeyError as exc:
        valid = ", ".join(sorted(strategies))
        raise ValueError(f"Estrategia desconocida: {name}. Válidas: {valid}") from exc
