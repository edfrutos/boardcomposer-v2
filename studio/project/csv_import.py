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
import math
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

            material = (row.get("material") or "").strip()
            # StudioPiece valida también por su cuenta; traducir su ValueError
            # mantiene la promesa del docstring (todo fallo sale como
            # CsvImportError) y evita que un invariante añadido ahí en el
            # futuro se escape hasta _import_pieces_csv, que no lo captura.
            try:
                if material:
                    piece = StudioPiece(
                        piece_id, length_mm, width_mm, material, thickness_mm
                    )
                else:
                    piece = StudioPiece(
                        piece_id, length_mm, width_mm, thickness_mm=thickness_mm
                    )
            except ValueError as error:
                raise CsvImportError(f"Fila {line_number}: {error}") from error
            pieces.append(piece)

    if not pieces:
        raise CsvImportError("El CSV no contiene ninguna pieza")

    return pieces
