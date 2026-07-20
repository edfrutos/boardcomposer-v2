"""CSV piece import for BoardComposer Studio.

Pure function, no Qt dependency, so it's unit-testable — same pattern as
the Core's csv_loader.py, but producing StudioPiece objects: in the Core a
CSV row is a `Board` (the item to cut); in Studio that same item is a
piece placed onto a stock board, so the columns map to StudioPiece.

Expected columns (same as the Core/CLI CSV format): `id`, `length_mm`,
`width_mm`, `thickness_mm`. An optional `material` column is honored;
absent, StudioPiece's default applies.
"""

import csv
from pathlib import Path

from studio.models import StudioPiece


class CsvImportError(ValueError):
    """The CSV file can't be turned into a valid list of Studio pieces."""


REQUIRED_COLUMNS = ("id", "length_mm", "width_mm", "thickness_mm")


def load_pieces_from_csv(
    path: str | Path, existing_ids: frozenset[str] = frozenset()
) -> list[StudioPiece]:
    """Reads `path` and returns one StudioPiece per row.

    Raises CsvImportError on a missing/empty required column, a non-numeric
    dimension, or an id that repeats — within the file or against
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

            material = (row.get("material") or "").strip()
            if material:
                piece = StudioPiece(
                    piece_id, length_mm, width_mm, material, thickness_mm
                )
            else:
                piece = StudioPiece(
                    piece_id, length_mm, width_mm, thickness_mm=thickness_mm
                )
            pieces.append(piece)

    if not pieces:
        raise CsvImportError("El CSV no contiene ninguna pieza")

    return pieces
