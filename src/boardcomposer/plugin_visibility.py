"""Cross-cutting visibility into installed plugins (DOC-999-Ideas.md candidate,
promoted as the first concrete step of Marketplace/Comunidad — DEC-0011-adjacent).

`discover_plugins()` and the per-group `*_plugin_errors()` functions already
exist; nothing outside Studio's status bar consumed them. This module answers
"what plugins are installed, and which of them failed to load" for the CLI
(`boardcomposer plugins`) and the API (`GET /plugins`), across the four
Core-side entry point groups. Studio's panel plugins are out of scope here —
that group only matters within the desktop app itself, not a CLI/API context.
"""

from boardcomposer.export.registry import (
    EXPORTER_REGISTRY,
    available_exporters,
    exporter_plugin_errors,
)
from boardcomposer.io.registry import (
    IMPORTER_REGISTRY,
    available_importers,
    importer_plugin_errors,
)
from boardcomposer.plugins import PluginLoadError
from boardcomposer.solver.generators import (
    GENERATOR_REGISTRY,
    available_generators,
    generator_plugin_errors,
)
from boardcomposer.solver.strategies import (
    STRATEGY_FACTORIES,
    available_strategies,
    strategy_plugin_errors,
)


def plugin_summary() -> dict:
    """Installed third-party plugins and load errors, per entry point group."""
    return {
        "generators": _group_summary(
            available_generators(), GENERATOR_REGISTRY, generator_plugin_errors()
        ),
        "strategies": _group_summary(
            available_strategies(), STRATEGY_FACTORIES, strategy_plugin_errors()
        ),
        "importers": _group_summary(
            available_importers(), IMPORTER_REGISTRY, importer_plugin_errors()
        ),
        "exporters": _group_summary(
            available_exporters(), EXPORTER_REGISTRY, exporter_plugin_errors()
        ),
    }


def _group_summary(
    available: dict, built_in: dict, errors: list[PluginLoadError]
) -> dict:
    installed = sorted(set(available) - set(built_in))
    return {
        "installed": installed,
        "errors": [{"name": error.name, "error": error.error} for error in errors],
    }
