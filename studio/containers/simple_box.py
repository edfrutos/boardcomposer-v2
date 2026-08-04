"""Parametric container templates for BoardComposer Studio (IDE-0028).

Pure functions, no Qt dependency — same pattern as `csv_import.py`. Each
template takes the container's outer dimensions plus the sheet thickness
and returns a flat list of `StudioPiece` (walls, base, ...) ready to add to
the open project with `AddPieceCommand`, one per piece, same as CSV import.
The solver doesn't need to know these pieces came from a template instead
of a CSV row or a hand-typed dialog — a piece is a piece.

`CONTAINER_TEMPLATES` (`studio/containers/__init__.py`) is the extension
point for future container types (drawer, N-drawer unit, shelving) and
`joint`/`dividers` are already part of the signature so adding a rebated
joint or internal dividers later is a new branch in this function, not a
new call site in Studio (DEC-0019 scope discussion,
`docs/masterplan/DOC-999-Ideas.md`).
"""

import math

from studio.models import StudioPiece

SUPPORTED_JOINTS = ("a_tope",)
SUPPORTED_DIVIDERS = (0,)


class ContainerTemplateError(ValueError):
    """The requested container can't be generated as a valid piece list."""


def build_simple_box_pieces(
    *,
    outer_length_mm: float,
    outer_width_mm: float,
    outer_height_mm: float,
    thickness_mm: float,
    material: str = "Demo",
    id_prefix: str = "caja",
    joint: str = "a_tope",
    dividers: int = 0,
    existing_ids: frozenset[str] = frozenset(),
) -> list[StudioPiece]:
    """Caja simple, abierta por arriba: base + 4 paredes a tope.

    La base ocupa toda la huella exterior (`outer_length_mm` x
    `outer_width_mm`); las paredes frontal/trasera abarcan todo el largo
    exterior, y las laterales encajan *entre* frontal y trasera (se les
    resta dos veces el grosor) — unión a tope clásica, sin rebaje.
    """
    if joint not in SUPPORTED_JOINTS:
        raise ContainerTemplateError(
            f"Unión '{joint}' no soportada todavía (solo: {', '.join(SUPPORTED_JOINTS)})"
        )
    if dividers not in SUPPORTED_DIVIDERS:
        raise ContainerTemplateError(
            "Divisores no soportados todavía (solo 0 en esta versión)"
        )

    for name, value in (
        ("outer_length_mm", outer_length_mm),
        ("outer_width_mm", outer_width_mm),
        ("outer_height_mm", outer_height_mm),
        ("thickness_mm", thickness_mm),
    ):
        if not math.isfinite(value) or value <= 0:
            raise ContainerTemplateError(
                f"{name} debe ser un número finito mayor que 0"
            )

    lateral_length_mm = outer_width_mm - 2 * thickness_mm
    if lateral_length_mm <= 0:
        raise ContainerTemplateError(
            "outer_width_mm es insuficiente para el grosor de pared indicado "
            "(las paredes laterales no caben entre frontal y trasera)"
        )

    pieces_spec = (
        ("base", outer_length_mm, outer_width_mm),
        ("pared-frontal", outer_length_mm, outer_height_mm),
        ("pared-trasera", outer_length_mm, outer_height_mm),
        ("lateral-izquierdo", lateral_length_mm, outer_height_mm),
        ("lateral-derecho", lateral_length_mm, outer_height_mm),
    )

    ids = [f"{id_prefix}-{suffix}" for suffix, _, _ in pieces_spec]
    repeated = [piece_id for piece_id in ids if piece_id in existing_ids]
    if repeated:
        raise ContainerTemplateError(
            f"Ya existe una pieza con id {', '.join(repeated)} — cambia el prefijo"
        )

    return [
        StudioPiece(piece_id, length_mm, width_mm, material, thickness_mm)
        for piece_id, (_, length_mm, width_mm) in zip(ids, pieces_spec, strict=True)
    ]
