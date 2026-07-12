from collections.abc import Callable
from pathlib import Path

from boardcomposer.domain import Project
from boardcomposer.io.csv_loader import load_project_from_csv
from boardcomposer.plugins import PluginLoadError, discover_plugins

IMPORTER_PLUGIN_GROUP = "boardcomposer.importers"

Importer = Callable[[str | Path], Project]

IMPORTER_REGISTRY: dict[str, Importer] = {
    "csv": load_project_from_csv,
}


def available_importers() -> dict[str, Importer]:
    """IMPORTER_REGISTRY más los importadores registrados por plugins
    instalados (grupo IMPORTER_PLUGIN_GROUP). Los integrados siempre
    ganan: un plugin no puede sustituir un importador existente."""
    plugins, _errors = discover_plugins(IMPORTER_PLUGIN_GROUP)
    return {**plugins, **IMPORTER_REGISTRY}


def importer_plugin_errors() -> list[PluginLoadError]:
    """Plugins de importadores instalados que fallaron al cargarse."""
    _plugins, errors = discover_plugins(IMPORTER_PLUGIN_GROUP)
    return errors


def importer_by_name(name: str) -> Importer:
    importers = available_importers()

    try:
        return importers[name]
    except KeyError as exc:
        valid = ", ".join(sorted(importers))
        raise ValueError(f"Importador desconocido: {name}. Válidos: {valid}") from exc
