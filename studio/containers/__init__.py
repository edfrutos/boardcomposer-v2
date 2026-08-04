"""Parametric container templates (IDE-0028/IDE-0031) — generate Studio
pieces for storage containers (box/drawer/shelf) from a template instead of
the user defining each piece by hand.

`CONTAINER_TEMPLATES` is the registry driving `ContainerGeneratorDialog`'s
"Tipo de contenedor" combo — a new template is a new function plus a new
entry here, not a new call site in Studio.
"""

from studio.containers.drawer import build_drawer_no_rails_pieces
from studio.containers.simple_box import (
    ContainerTemplateError,
    build_simple_box_pieces,
)

CONTAINER_TEMPLATES = {
    "caja_simple": build_simple_box_pieces,
    "cajon_sin_rieles": build_drawer_no_rails_pieces,
}

__all__ = [
    "CONTAINER_TEMPLATES",
    "ContainerTemplateError",
    "build_drawer_no_rails_pieces",
    "build_simple_box_pieces",
]
