"""Persistent scrap-board inventory for BoardComposer Studio (IDE-0039).

Pure function, no Qt dependency — same SQLite pattern as the Core's
billing.py, but for a single-user, single-machine workshop inventory
instead of a multi-tenant API resource: leftover cut-offs from previous
projects, registered once and reused across unrelated projects instead of
buying new stock.

A scrap is never deleted once registered — consuming it (using it in a
project) sets `consumed_at` instead of removing the row, so the history
survives even though the piece is gone from `list_available()`. Same
"never act in silence, never lose data" criterion as the rest of the
project.
"""

import math
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


class ScrapInventoryError(ValueError):
    """A scrap can't be registered or consumed as requested."""


@dataclass(frozen=True)
class ScrapRecord:
    scrap_id: str
    length_mm: float
    width_mm: float
    thickness_mm: float
    material: str
    origin: str
    created_at: str


def init_db(db_path: str | Path) -> None:
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scraps (
                scrap_id TEXT PRIMARY KEY,
                length_mm REAL NOT NULL,
                width_mm REAL NOT NULL,
                thickness_mm REAL NOT NULL,
                material TEXT NOT NULL DEFAULT '',
                origin TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL,
                consumed_at TEXT
            )
            """
        )


def add_scrap(
    db_path: str | Path,
    scrap_id: str,
    length_mm: float,
    width_mm: float,
    thickness_mm: float,
    material: str = "",
    origin: str = "",
) -> None:
    scrap_id = scrap_id.strip()
    if not scrap_id:
        raise ScrapInventoryError("El retal necesita un id.")

    # Same invariant as Board/StudioBoard: dimensions come from a dialog
    # here, but float() elsewhere in the codebase accepts "nan"/"inf" from
    # less trusted sources, and a copy-pasted pattern is easy to get wrong.
    for name, value in (
        ("length_mm", length_mm),
        ("width_mm", width_mm),
        ("thickness_mm", thickness_mm),
    ):
        if not math.isfinite(value) or value <= 0:
            raise ScrapInventoryError(f"{name} debe ser un número finito mayor que 0")

    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        existing = conn.execute(
            "SELECT 1 FROM scraps WHERE scrap_id = ?", (scrap_id,)
        ).fetchone()
        if existing is not None:
            raise ScrapInventoryError(f"Ya existe un retal con id '{scrap_id}'.")

        conn.execute(
            "INSERT INTO scraps "
            "(scrap_id, length_mm, width_mm, thickness_mm, material, origin, "
            "created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                scrap_id,
                length_mm,
                width_mm,
                thickness_mm,
                material,
                origin,
                datetime.now(timezone.utc).isoformat(),
            ),
        )


def list_available(db_path: str | Path) -> list[ScrapRecord]:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT scrap_id, length_mm, width_mm, thickness_mm, material, "
            "origin, created_at FROM scraps WHERE consumed_at IS NULL "
            "ORDER BY length_mm * width_mm ASC"
        ).fetchall()
        return [
            ScrapRecord(
                scrap_id=row["scrap_id"],
                length_mm=row["length_mm"],
                width_mm=row["width_mm"],
                thickness_mm=row["thickness_mm"],
                material=row["material"],
                origin=row["origin"],
                created_at=row["created_at"],
            )
            for row in rows
        ]


def consume(db_path: str | Path, scrap_id: str) -> None:
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT consumed_at FROM scraps WHERE scrap_id = ?", (scrap_id,)
        ).fetchone()
        if row is None:
            raise ScrapInventoryError(f"No existe ningún retal con id '{scrap_id}'.")
        if row[0] is not None:
            raise ScrapInventoryError(f"El retal '{scrap_id}' ya estaba consumido.")

        conn.execute(
            "UPDATE scraps SET consumed_at = ? WHERE scrap_id = ?",
            (datetime.now(timezone.utc).isoformat(), scrap_id),
        )
