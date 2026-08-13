"""CSV import/export for the materials catalog (IDE-0041).

Pure function, no Qt dependency, same pattern as csv_import.py. Unlike the
piece/board CSV importers — which read files the user authors by hand
from whatever a supplier or a spreadsheet gives them — this format is
primarily BoardComposer's own round-trip: export a catalog, hand the file
to someone else, import it into their Studio. Column names still accept
the Spanish aliases the interface itself uses (`DT-0026`: a CSV column
named the way the rest of the app is labeled silently not matching was a
real, twice-reported bug), so a catalog exported and then hand-edited in
a spreadsheet doesn't fall into the same trap.
"""

import csv
import math
from pathlib import Path

from studio.project.materials_library import (
    PRICE_UNITS,
    MaterialRecord,
)

REQUIRED_COLUMNS = ("id", "name", "thickness_mm")

_COLUMN_ALIASES = {
    "id": ("id",),
    "name": ("name", "nombre"),
    "thickness_mm": ("thickness_mm", "grosor_mm", "grosor"),
    "provider": ("provider", "proveedor"),
    "price": ("price", "precio"),
    "price_unit": ("price_unit", "unidad_precio", "unidad"),
}

EXPORT_HEADER = ["id", "name", "thickness_mm", "provider", "price", "price_unit"]


class MaterialsCsvError(ValueError):
    """The CSV file can't be turned into a valid list of materials."""


def _column_from_row(row: dict, field: str) -> str:
    aliases = _COLUMN_ALIASES[field]
    for key in row:
        if key and key.strip().lower() in aliases:
            return (row[key] or "").strip()
    return ""


def _header_has_column(header: list[str], field: str) -> bool:
    aliases = _COLUMN_ALIASES[field]
    return any(column.strip().lower() in aliases for column in header)


def export_materials_csv(path: str | Path, materials: list[MaterialRecord]) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(EXPORT_HEADER)
        for material in materials:
            writer.writerow(
                [
                    material.material_id,
                    material.name,
                    material.thickness_mm,
                    material.provider,
                    material.price,
                    material.price_unit,
                ]
            )


def import_materials_csv(
    path: str | Path, existing_ids: frozenset[str] = frozenset()
) -> list[MaterialRecord]:
    """Reads `path` and returns one MaterialRecord per row, validated but
    not yet written to any catalog — the caller decides how to persist
    them (`materials_library.add_materials_bulk()`, all-or-nothing).

    Raises MaterialsCsvError on a missing/empty required column, a
    non-numeric dimension/price, an invalid price_unit, or an id that
    repeats within the file or against `existing_ids` — same
    "never partially apply a bad file" criterion as the piece/board CSV
    importers.
    """
    records: list[MaterialRecord] = []
    seen_ids: set[str] = set(existing_ids)

    with Path(path).open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames or []
        missing = [
            field for field in REQUIRED_COLUMNS if not _header_has_column(header, field)
        ]
        if missing:
            raise MaterialsCsvError(
                f"Faltan columnas obligatorias en el CSV: {', '.join(missing)}"
            )

        for line_number, row in enumerate(reader, start=2):
            material_id = _column_from_row(row, "id")
            if not material_id:
                raise MaterialsCsvError(f"Fila {line_number}: falta el id del material")
            if material_id in seen_ids:
                raise MaterialsCsvError(
                    f"Fila {line_number}: id repetido '{material_id}' (ya existe en "
                    "el CSV o en la biblioteca)"
                )
            seen_ids.add(material_id)

            name = _column_from_row(row, "name")
            if not name:
                raise MaterialsCsvError(
                    f"Fila {line_number}: falta el nombre del material"
                )

            thickness_raw = _column_from_row(row, "thickness_mm")
            try:
                thickness_mm = float(thickness_raw)
            except ValueError as error:
                raise MaterialsCsvError(
                    f"Fila {line_number}: thickness_mm no numérico "
                    f"(se recibió {thickness_raw!r})"
                ) from error
            if not math.isfinite(thickness_mm) or thickness_mm <= 0:
                raise MaterialsCsvError(
                    f"Fila {line_number}: thickness_mm debe ser un número finito "
                    f"mayor que 0 (se recibió {thickness_raw!r})"
                )

            provider = _column_from_row(row, "provider")

            price_raw = _column_from_row(row, "price")
            if price_raw:
                try:
                    price = float(price_raw)
                except ValueError as error:
                    raise MaterialsCsvError(
                        f"Fila {line_number}: price no numérico "
                        f"(se recibió {price_raw!r})"
                    ) from error
                if not math.isfinite(price) or price < 0:
                    raise MaterialsCsvError(
                        f"Fila {line_number}: price debe ser un número finito y no "
                        f"negativo (se recibió {price_raw!r})"
                    )
            else:
                price = 0.0

            price_unit_raw = _column_from_row(row, "price_unit").lower()
            if not price_unit_raw:
                price_unit = "board"
            elif price_unit_raw in ("board", "tablero"):
                price_unit = "board"
            elif price_unit_raw in ("m2", "m²"):
                price_unit = "m2"
            else:
                raise MaterialsCsvError(
                    f"Fila {line_number}: price_unit debe ser uno de {PRICE_UNITS} "
                    f"(se recibió {price_unit_raw!r})"
                )

            records.append(
                MaterialRecord(
                    material_id=material_id,
                    name=name,
                    thickness_mm=thickness_mm,
                    provider=provider,
                    price=price,
                    price_unit=price_unit,
                    created_at="",
                )
            )

    if not records:
        raise MaterialsCsvError("El CSV no contiene ningún material")

    return records
