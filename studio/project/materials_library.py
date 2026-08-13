"""Persistent materials catalog for BoardComposer Studio (IDE-0041).

Pure function, no Qt dependency — same SQLite pattern as scrap_inventory.py
(IDE-0039), but for reference data (a reusable list of materials a
workshop buys from, with thickness/provider/price) instead of a
consumable resource. A catalog entry is one material at one thickness —
the same material at two thicknesses (e.g. "Aglomerado" 10mm and 18mm)
is two separate entries, same granularity as Board/StudioBoard, which
also carry a single thickness_mm.

Unlike scraps, an entry here is reference data with no lifecycle to
track — deleting one is a real DELETE, not a soft "consumed" flag.
"""

import math
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

PRICE_UNITS = ("board", "m2")


class MaterialsLibraryError(ValueError):
    """A material can't be added, updated or removed as requested."""


@dataclass(frozen=True)
class MaterialRecord:
    material_id: str
    name: str
    thickness_mm: float
    provider: str
    price: float
    price_unit: str
    created_at: str


def init_db(db_path: str | Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS materials (
                material_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                thickness_mm REAL NOT NULL,
                provider TEXT NOT NULL DEFAULT '',
                price REAL NOT NULL DEFAULT 0,
                price_unit TEXT NOT NULL DEFAULT 'board',
                created_at TEXT NOT NULL
            )
            """
        )


def _validate(
    material_id: str, name: str, thickness_mm: float, price: float, price_unit: str
) -> None:
    if not material_id:
        raise MaterialsLibraryError("El material necesita un id.")
    if not name:
        raise MaterialsLibraryError("El material necesita un nombre.")
    if not math.isfinite(thickness_mm) or thickness_mm <= 0:
        raise MaterialsLibraryError(
            "thickness_mm debe ser un número finito mayor que 0"
        )
    if not math.isfinite(price) or price < 0:
        raise MaterialsLibraryError("price debe ser un número finito y no negativo")
    if price_unit not in PRICE_UNITS:
        raise MaterialsLibraryError(
            f"price_unit debe ser uno de {PRICE_UNITS} (se recibió {price_unit!r})"
        )


def _row_to_record(row: sqlite3.Row) -> MaterialRecord:
    return MaterialRecord(
        material_id=row["material_id"],
        name=row["name"],
        thickness_mm=row["thickness_mm"],
        provider=row["provider"],
        price=row["price"],
        price_unit=row["price_unit"],
        created_at=row["created_at"],
    )


def add_material(
    db_path: str | Path,
    material_id: str,
    name: str,
    thickness_mm: float,
    provider: str = "",
    price: float = 0.0,
    price_unit: str = "board",
) -> None:
    material_id = material_id.strip()
    name = name.strip()
    _validate(material_id, name, thickness_mm, price, price_unit)

    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        existing = conn.execute(
            "SELECT 1 FROM materials WHERE material_id = ?", (material_id,)
        ).fetchone()
        if existing is not None:
            raise MaterialsLibraryError(
                f"Ya existe un material con id '{material_id}'."
            )

        conn.execute(
            "INSERT INTO materials "
            "(material_id, name, thickness_mm, provider, price, price_unit, "
            "created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                material_id,
                name,
                thickness_mm,
                provider,
                price,
                price_unit,
                datetime.now(timezone.utc).isoformat(),
            ),
        )


def add_materials_bulk(db_path: str | Path, records: list[MaterialRecord]) -> None:
    """Adds every record or none — used by CSV import (IDE-0041) so a bad
    row late in the file can't leave the catalog half-imported. A single
    transaction: raising inside the `with conn:` block rolls it back."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        seen_ids: set[str] = set()
        for record in records:
            material_id = record.material_id.strip()
            name = record.name.strip()
            _validate(
                material_id, name, record.thickness_mm, record.price, record.price_unit
            )
            if material_id in seen_ids:
                raise MaterialsLibraryError(
                    f"Id repetido en el fichero: '{material_id}'."
                )
            seen_ids.add(material_id)

            existing = conn.execute(
                "SELECT 1 FROM materials WHERE material_id = ?", (material_id,)
            ).fetchone()
            if existing is not None:
                raise MaterialsLibraryError(
                    f"Ya existe un material con id '{material_id}'."
                )

            conn.execute(
                "INSERT INTO materials "
                "(material_id, name, thickness_mm, provider, price, price_unit, "
                "created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    material_id,
                    name,
                    record.thickness_mm,
                    record.provider,
                    record.price,
                    record.price_unit,
                    datetime.now(timezone.utc).isoformat(),
                ),
            )


def list_materials(db_path: str | Path) -> list[MaterialRecord]:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT material_id, name, thickness_mm, provider, price, price_unit, "
            "created_at FROM materials ORDER BY name ASC, thickness_mm ASC"
        ).fetchall()
        return [_row_to_record(row) for row in rows]


def update_material(
    db_path: str | Path,
    material_id: str,
    name: str,
    thickness_mm: float,
    provider: str = "",
    price: float = 0.0,
    price_unit: str = "board",
) -> None:
    material_id = material_id.strip()
    name = name.strip()
    _validate(material_id, name, thickness_mm, price, price_unit)

    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        existing = conn.execute(
            "SELECT 1 FROM materials WHERE material_id = ?", (material_id,)
        ).fetchone()
        if existing is None:
            raise MaterialsLibraryError(
                f"No existe ningún material con id '{material_id}'."
            )

        conn.execute(
            "UPDATE materials SET name = ?, thickness_mm = ?, provider = ?, "
            "price = ?, price_unit = ? WHERE material_id = ?",
            (name, thickness_mm, provider, price, price_unit, material_id),
        )


def delete_material(db_path: str | Path, material_id: str) -> None:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        existing = conn.execute(
            "SELECT 1 FROM materials WHERE material_id = ?", (material_id,)
        ).fetchone()
        if existing is None:
            raise MaterialsLibraryError(
                f"No existe ningún material con id '{material_id}'."
            )

        conn.execute("DELETE FROM materials WHERE material_id = ?", (material_id,))
