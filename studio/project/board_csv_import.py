"""CSV board import for BoardComposer Studio (IDE-0029).

Pure function, no Qt dependency — same pattern as `csv_import.py`
(pieces), but producing `StudioBoard` objects instead: in Studio a board
is the stock sheet a piece gets placed onto, not something to cut out.
Same use case that motivated `DEC-0019` (retales) — adding several
scrap boards by hand, one dialog at a time, doesn't scale once there are
more than a couple.

Expected columns: `id`, `length_mm`, `width_mm`, `thickness_mm`, plus
two optional columns, in this order: `quantity` (IDE-0037) expands a
row into that many identical boards, with ids derived from the row's id
(`T-101`, `T-101-2`, `T-101-3`, ...) — same suffix scheme as the
"Cantidad" field in BoardDialog, but deterministic rather than
collision-probing: any derived id that collides aborts the whole
import, same as a literal duplicate id. `material` is honored as-is;
absent, StudioBoard's default applies.
"""

import csv
import math
from pathlib import Path

from studio.models import StudioBoard


class BoardCsvImportError(ValueError):
    """The CSV file can't be turned into a valid list of Studio boards."""


REQUIRED_COLUMNS = ("id", "length_mm", "width_mm", "thickness_mm")


def _quantity_from_row(row: dict) -> str:
    """`quantity` accepted case-insensitively, plus its Spanish name
    ("Cantidad", the label BoardDialog itself uses) — reported by the
    user: a CSV column named the way the rest of the app's UI is
    labeled silently defaulted every row to quantity=1, since the
    literal lowercase English column name never matched."""
    for key in row:
        if key and key.strip().lower() in ("quantity", "cantidad"):
            return (row[key] or "").strip()
    return ""


def load_boards_from_csv(
    path: str | Path, existing_ids: frozenset[str] = frozenset()
) -> list[StudioBoard]:
    """Reads `path` and returns one StudioBoard per row (more than one if
    the row's `quantity` column is greater than 1).

    Raises BoardCsvImportError on a missing/empty required column, a
    non-numeric dimension, a non-integer/non-positive `quantity`, or an id
    (literal or quantity-derived) that repeats — within the file or
    against `existing_ids` (the ids already present in the open project):
    importing must never corrupt the project, so any bad row aborts the
    whole import instead of partially applying it. Same all-or-nothing
    contract as `load_pieces_from_csv()`.
    """
    boards: list[StudioBoard] = []
    seen_ids: set[str] = set(existing_ids)

    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in header]
        if missing:
            raise BoardCsvImportError(
                f"Faltan columnas obligatorias en el CSV: {', '.join(missing)}"
            )

        for line_number, row in enumerate(reader, start=2):
            board_id = (row.get("id") or "").strip()
            if not board_id:
                raise BoardCsvImportError(
                    f"Fila {line_number}: falta el id del tablero"
                )
            if board_id in seen_ids:
                raise BoardCsvImportError(
                    f"Fila {line_number}: id repetido '{board_id}' (ya existe en "
                    "el CSV o en el proyecto abierto)"
                )
            seen_ids.add(board_id)

            try:
                length_mm = float(row["length_mm"])
                width_mm = float(row["width_mm"])
                thickness_mm = float(row["thickness_mm"])
            except (ValueError, TypeError) as error:
                raise BoardCsvImportError(
                    f"Fila {line_number}: dimensión no numérica ({error})"
                ) from error

            for column, value in (
                ("length_mm", length_mm),
                ("width_mm", width_mm),
                ("thickness_mm", thickness_mm),
            ):
                if not math.isfinite(value) or value <= 0:
                    raise BoardCsvImportError(
                        f"Fila {line_number}: {column} debe ser un número finito "
                        f"mayor que 0 (se recibió {row[column]!r})"
                    )

            quantity_raw = _quantity_from_row(row)
            if quantity_raw:
                try:
                    quantity = int(quantity_raw)
                except ValueError as error:
                    raise BoardCsvImportError(
                        f"Fila {line_number}: quantity debe ser un número entero "
                        f"(se recibió {quantity_raw!r})"
                    ) from error
                if quantity < 1:
                    raise BoardCsvImportError(
                        f"Fila {line_number}: quantity debe ser 1 o mayor "
                        f"(se recibió {quantity})"
                    )
            else:
                quantity = 1

            # Determinista, no colisión-probing como _generate_ids()
            # (main_window.py): una colisión con cualquier id derivado es un
            # error que aborta todo, igual que un id literal repetido —
            # nunca renombra en silencio.
            unit_ids = [board_id] + [
                f"{board_id}-{suffix}" for suffix in range(2, quantity + 1)
            ]
            for unit_id in unit_ids[1:]:
                if unit_id in seen_ids:
                    raise BoardCsvImportError(
                        f"Fila {line_number}: id repetido '{unit_id}' (derivado de "
                        f"'{board_id}' x quantity={quantity}; ya existe en el CSV o "
                        "en el proyecto abierto)"
                    )
                seen_ids.add(unit_id)

            material = (row.get("material") or "").strip()
            for unit_id in unit_ids:
                try:
                    if material:
                        board = StudioBoard(
                            unit_id, length_mm, width_mm, material, thickness_mm
                        )
                    else:
                        board = StudioBoard(
                            unit_id, length_mm, width_mm, thickness_mm=thickness_mm
                        )
                except ValueError as error:
                    raise BoardCsvImportError(f"Fila {line_number}: {error}") from error
                boards.append(board)

    if not boards:
        raise BoardCsvImportError("El CSV no contiene ningún tablero")

    return boards
