"""Studio panels registered as plugins (IDE-0008 Fase E).

Mirrors boardcomposer.plugins' pattern for the Core (generators,
strategies, importers/exporters, see docs/architecture.md) but lives in
Studio: a panel plugin returns a Qt widget, and Studio is the only
layer allowed to depend on Qt.
"""

from collections.abc import Callable

from PySide6.QtWidgets import QWidget

from boardcomposer.plugins import PluginLoadError, discover_plugins
from studio.services import StudioServices

STUDIO_PANEL_PLUGIN_GROUP = "boardcomposer.studio_panels"

PanelFactory = Callable[[StudioServices], QWidget]


def discover_panel_plugins() -> tuple[dict[str, PanelFactory], list[PluginLoadError]]:
    """Resuelve los plugins de panel instalados (grupo STUDIO_PANEL_PLUGIN_GROUP).

    A diferencia de generators.py/strategies.py/io.registry.py/export.registry.py,
    no hay paneles integrados que fusionar aquí: Explorer/Inspector/Timeline/
    Comparador/Asistente son parte fija de MainWindow, no plugins.
    """
    return discover_plugins(STUDIO_PANEL_PLUGIN_GROUP)
