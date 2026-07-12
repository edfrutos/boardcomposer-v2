from dataclasses import dataclass
from importlib.metadata import entry_points
from typing import Any


@dataclass(frozen=True)
class PluginLoadError:
    name: str
    error: str


def discover_plugins(group: str) -> tuple[dict[str, Any], list[PluginLoadError]]:
    """Resuelve los entry points instalados para `group`.

    Un plugin de terceros puede fallar al cargarse por cualquier motivo
    (paquete desinstalado a medias, error de sintaxis, dependencia que
    falta...); un plugin roto no debe impedir que el resto de plugins,
    ni la aplicación, arranquen.
    """
    plugins: dict[str, Any] = {}
    errors: list[PluginLoadError] = []

    for entry_point in entry_points(group=group):
        try:
            plugins[entry_point.name] = entry_point.load()
        except Exception as error:  # noqa: BLE001 - código de terceros, cualquier fallo es posible
            errors.append(PluginLoadError(name=entry_point.name, error=str(error)))

    return plugins, errors
