"""Parametric container templates (IDE-0028) — generate Studio pieces for
storage containers (box/drawer/shelf) from a template instead of the user
defining each piece by hand."""

from studio.containers.simple_box import (
    CONTAINER_TEMPLATES,
    ContainerTemplateError,
    build_simple_box_pieces,
)

__all__ = [
    "CONTAINER_TEMPLATES",
    "ContainerTemplateError",
    "build_simple_box_pieces",
]
