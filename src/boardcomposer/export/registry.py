from collections.abc import Callable

from boardcomposer.domain import AssemblySolution
from boardcomposer.export.dxf_exporter import solution_to_dxf
from boardcomposer.export.svg_exporter import solution_to_svg
from boardcomposer.plugins import PluginLoadError, discover_plugins

EXPORTER_PLUGIN_GROUP = "boardcomposer.exporters"

Exporter = Callable[[AssemblySolution], str]

EXPORTER_REGISTRY: dict[str, Exporter] = {
    "svg": solution_to_svg,
    "dxf": solution_to_dxf,
}


def available_exporters() -> dict[str, Exporter]:
    """EXPORTER_REGISTRY más los exportadores registrados por plugins
    instalados (grupo EXPORTER_PLUGIN_GROUP). Los integrados siempre
    ganan: un plugin no puede sustituir un exportador existente."""
    plugins, _errors = discover_plugins(EXPORTER_PLUGIN_GROUP)
    return {**plugins, **EXPORTER_REGISTRY}


def exporter_plugin_errors() -> list[PluginLoadError]:
    """Plugins de exportadores instalados que fallaron al cargarse."""
    _plugins, errors = discover_plugins(EXPORTER_PLUGIN_GROUP)
    return errors


def exporter_by_name(name: str) -> Exporter:
    exporters = available_exporters()

    try:
        return exporters[name]
    except KeyError as exc:
        valid = ", ".join(sorted(exporters))
        raise ValueError(f"Exportador desconocido: {name}. Válidos: {valid}") from exc
