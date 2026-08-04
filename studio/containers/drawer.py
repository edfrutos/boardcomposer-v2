"""Drawer-without-rails container template (IDE-0031).

Same physical shape as the simple box (`simple_box.py`) — base + 4 walls,
open top — but the outer dimensions aren't given directly. A drawer that
slides wood-on-wood without metal rails needs clearance against the
cabinet opening it sits in, so the caller supplies the opening's width and
height plus a per-side clearance, and this derives the drawer's outer
length/height before delegating to `build_simple_box_pieces()` for the
actual piece list. Depth isn't derived from the opening (the opening is
only width x height) — it's a free parameter set by the cabinet's
interior depth.
"""

import math

from studio.containers.simple_box import ContainerTemplateError, build_simple_box_pieces
from studio.models import StudioPiece


def build_drawer_no_rails_pieces(
    *,
    opening_length_mm: float,
    opening_height_mm: float,
    depth_mm: float,
    clearance_mm: float,
    thickness_mm: float,
    material: str = "Demo",
    id_prefix: str = "cajon",
    joint: str = "a_tope",
    dividers: int = 0,
    existing_ids: frozenset[str] = frozenset(),
) -> list[StudioPiece]:
    """Cajón sin rieles: dimensiones exteriores derivadas del hueco del mueble.

    `opening_length_mm`/`opening_height_mm` son el ancho y alto del hueco
    del mueble donde va a deslizar el cajón; `clearance_mm` es la holgura
    por lado (se resta dos veces de cada dimensión del hueco) para que la
    madera deslice sin rozar al no haber rieles metálicos que absorban el
    ajuste. `depth_mm` es independiente del hueco (el hueco solo define
    ancho y alto) y se corresponde con la profundidad interior del mueble.
    """
    for name, value in (
        ("opening_length_mm", opening_length_mm),
        ("opening_height_mm", opening_height_mm),
        ("depth_mm", depth_mm),
    ):
        if not math.isfinite(value) or value <= 0:
            raise ContainerTemplateError(
                f"{name} debe ser un número finito mayor que 0"
            )
    if not math.isfinite(clearance_mm) or clearance_mm < 0:
        raise ContainerTemplateError(
            "clearance_mm debe ser un número finito mayor o igual que 0"
        )

    outer_length_mm = opening_length_mm - 2 * clearance_mm
    outer_height_mm = opening_height_mm - 2 * clearance_mm
    if outer_length_mm <= 0 or outer_height_mm <= 0:
        raise ContainerTemplateError(
            "La holgura es demasiado grande para el hueco indicado "
            "(el cajón resultante tendría dimensiones nulas o negativas)"
        )

    return build_simple_box_pieces(
        outer_length_mm=outer_length_mm,
        outer_width_mm=depth_mm,
        outer_height_mm=outer_height_mm,
        thickness_mm=thickness_mm,
        material=material,
        id_prefix=id_prefix,
        joint=joint,
        dividers=dividers,
        existing_ids=existing_ids,
    )
