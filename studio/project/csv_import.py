"""CSV piece import for BoardComposer Studio.

Pure function, no Qt dependency, so it's unit-testable — same pattern as
the Core's csv_loader.py, but producing StudioPiece objects: in the Core a
CSV row is a `Board` (the item to cut); in Studio that same item is a
piece placed onto a stock board, so the columns map to StudioPiece.

Expected columns (same as the Core/CLI CSV format): `id`, `length_mm`,
`width_mm`, `thickness_mm`, plus two optional columns, in this order:
`quantity` (IDE-0037) expands a row into that many identical pieces,
with ids derived from the row's id (`P-101`, `P-101-2`, `P-101-3`, ...)
— same suffix scheme as the "Cantidad" field in PieceDialog, but
deterministic rather than collision-probing: any derived id that
collides aborts the whole import, same as a literal duplicate id.
`material` is honored as-is; absent, StudioPiece's default applies.
"""

import csv
import math
from pathlib import Path

from studio.models import StudioPiece


class CsvImportError(ValueError):
    """The CSV file can't be turned into a valid list of Studio pieces."""


REQUIRED_COLUMNS = ("id", "length_mm", "width_mm", "thickness_mm")


def _quantity_from_row(row: dict) -> str:
    """`quantity` accepted case-insensitively, plus its Spanish name
    ("Cantidad", the label PieceDialog itself uses) — reported by the
    user: a CSV column named the way the rest of the app's UI is
    labeled silently defaulted every row to quantity=1, since the
    literal lowercase English column name never matched."""
    for key in row:
        if key and key.strip().lower() in ("quantity", "cantidad"):
            return (row[key] or "").strip()
    return ""


def load_pieces_from_csv(
    path: str | Path, existing_ids: frozenset[str] = frozenset()
) -> list[StudioPiece]:
    """Reads `path` and returns one StudioPiece per row (more than one if
    the row's `quantity` column is greater than 1).

    Raises CsvImportError on a missing/empty required column, a non-numeric
    dimension, a non-integer/non-positive `quantity`, or an id (literal or
    quantity-derived) that repeats — within the file or against
    `existing_ids` (the ids already present in the open project): importing
    must never corrupt the project, so any bad row aborts the whole import
    instead of partially applying it.
    """
    pieces: list[StudioPiece] = []
    seen_ids: set[str] = set(existing_ids)

    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in header]
        if missing:
            raise CsvImportError(
                f"Faltan columnas obligatorias en el CSV: {', '.join(missing)}"
            )

        for line_number, row in enumerate(reader, start=2):
            piece_id = (row.get("id") or "").strip()
            if not piece_id:
                raise CsvImportError(f"Fila {line_number}: falta el id de la pieza")
            if piece_id in seen_ids:
                raise CsvImportError(
                    f"Fila {line_number}: id repetido '{piece_id}' (ya existe en "
                    "el CSV o en el proyecto abierto)"
                )
            seen_ids.add(piece_id)

            try:
                length_mm = float(row["length_mm"])
                width_mm = float(row["width_mm"])
                thickness_mm = float(row["thickness_mm"])
            except (ValueError, TypeError) as error:
                raise CsvImportError(
                    f"Fila {line_number}: dimensión no numérica ({error})"
                ) from error

            # float() acepta "nan", "inf" y "1e400" (que desborda a inf), y una
            # dimensión negativa o cero es igual de inservible: una pieza así
            # entra al proyecto y revienta después, al colocarla o exportarla.
            for column, value in (
                ("length_mm", length_mm),
                ("width_mm", width_mm),
                ("thickness_mm", thickness_mm),
            ):
                if not math.isfinite(value) or value <= 0:
                    raise CsvImportError(
                        f"Fila {line_number}: {column} debe ser un número finito "
                        f"mayor que 0 (se recibió {row[column]!r})"
                    )

            quantity_raw = _quantity_from_row(row)
            if quantity_raw:
                try:
                    quantity = int(quantity_raw)
                except ValueError as error:
                    raise CsvImportError(
                        f"Fila {line_number}: quantity debe ser un número entero "
                        f"(se recibió {quantity_raw!r})"
                    ) from error
                if quantity < 1:
                    raise CsvImportError(
                        f"Fila {line_number}: quantity debe ser 1 o mayor "
                        f"(se recibió {quantity})"
                    )
            else:
                quantity = 1

            # Determinista, no colisión-probing como _generate_ids()
            # (main_window.py): una colisión con cualquier id derivado es un
            # error que aborta todo, igual que un id literal repetido —
            # nunca renombra en silencio.
            unit_ids = [piece_id] + [
                f"{piece_id}-{suffix}" for suffix in range(2, quantity + 1)
            ]
            for unit_id in unit_ids[1:]:
                if unit_id in seen_ids:
                    raise CsvImportError(
                        f"Fila {line_number}: id repetido '{unit_id}' (derivado de "
                        f"'{piece_id}' x quantity={quantity}; ya existe en el CSV o "
                        "en el proyecto abierto)"
                    )
                seen_ids.add(unit_id)

            material = (row.get("material") or "").strip()
            # StudioPiece valida también por su cuenta; traducir su ValueError
            # mantiene la promesa del docstring (todo fallo sale como
            # CsvImportError) y evita que un invariante añadido ahí en el
            # futuro se escape hasta _import_pieces_csv, que no lo captura.
            for unit_id in unit_ids:
                try:
                    if material:
                        piece = StudioPiece(
                            unit_id, length_mm, width_mm, material, thickness_mm
                        )
                    else:
                        piece = StudioPiece(
                            unit_id, length_mm, width_mm, thickness_mm=thickness_mm
                        )
                except ValueError as error:
                    raise CsvImportError(f"Fila {line_number}: {error}") from error
                pieces.append(piece)

    if not pieces:
        raise CsvImportError("El CSV no contiene ninguna pieza")

    return pieces
