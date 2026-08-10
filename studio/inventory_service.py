"""Qt-aware glue between StudioServices and the scrap inventory (IDE-0039).

`studio/project/scrap_inventory.py` is pure and takes a `db_path` for every
call, so it's directly unit-testable. This wrapper's only job is picking a
default `db_path` — the same per-user application-data directory
`QSettings()` already relies on for theme/last-project-path
(`studio/app.py`), so the inventory survives across projects and Studio
restarts without asking the user to choose a file.
"""

from pathlib import Path

from PySide6.QtCore import QStandardPaths

from studio.project import scrap_inventory
from studio.project.scrap_inventory import ScrapRecord

DB_FILENAME = "retales.db"


def default_db_path() -> Path:
    directory = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    directory = Path(directory) if directory else Path.cwd()
    directory.mkdir(parents=True, exist_ok=True)
    return directory / DB_FILENAME


class ScrapInventoryService:
    def __init__(self, db_path: str | Path | None = None):
        self.db_path = db_path if db_path is not None else default_db_path()
        scrap_inventory.init_db(self.db_path)

    def add(
        self,
        scrap_id: str,
        length_mm: float,
        width_mm: float,
        thickness_mm: float,
        material: str = "",
        origin: str = "",
    ) -> None:
        scrap_inventory.add_scrap(
            self.db_path,
            scrap_id,
            length_mm,
            width_mm,
            thickness_mm,
            material,
            origin,
        )

    def list_available(self) -> list[ScrapRecord]:
        return scrap_inventory.list_available(self.db_path)

    def consume(self, scrap_id: str) -> None:
        scrap_inventory.consume(self.db_path, scrap_id)
