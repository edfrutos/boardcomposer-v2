"""Qt-aware glue between StudioServices and the materials catalog
(IDE-0041).

`studio/project/materials_library.py` is pure and takes a `db_path` for
every call, so it's directly unit-testable. This wrapper's only job is
picking a default `db_path` — same per-user application-data directory
`ScrapInventoryService` already uses (`studio/inventory_service.py`), in
a separate file (`materiales.db`, not `retales.db`): the catalog and the
scrap inventory are two independent workshop resources.
"""

from pathlib import Path

from PySide6.QtCore import QStandardPaths

from studio.project import materials_csv, materials_library
from studio.project.materials_library import MaterialRecord

DB_FILENAME = "materiales.db"


def default_db_path() -> Path:
    directory = QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
    directory = Path(directory) if directory else Path.cwd()
    directory.mkdir(parents=True, exist_ok=True)
    return directory / DB_FILENAME


class MaterialsLibraryService:
    def __init__(self, db_path: str | Path | None = None):
        self.db_path = db_path if db_path is not None else default_db_path()
        materials_library.init_db(self.db_path)

    def add(
        self,
        material_id: str,
        name: str,
        thickness_mm: float,
        provider: str = "",
        price: float = 0.0,
        price_unit: str = "board",
    ) -> None:
        materials_library.add_material(
            self.db_path, material_id, name, thickness_mm, provider, price, price_unit
        )

    def update(
        self,
        material_id: str,
        name: str,
        thickness_mm: float,
        provider: str = "",
        price: float = 0.0,
        price_unit: str = "board",
    ) -> None:
        materials_library.update_material(
            self.db_path, material_id, name, thickness_mm, provider, price, price_unit
        )

    def delete(self, material_id: str) -> None:
        materials_library.delete_material(self.db_path, material_id)

    def list_materials(self) -> list[MaterialRecord]:
        return materials_library.list_materials(self.db_path)

    def import_csv(self, path: str | Path) -> list[MaterialRecord]:
        existing_ids = frozenset(
            material.material_id for material in self.list_materials()
        )
        records = materials_csv.import_materials_csv(path, existing_ids=existing_ids)
        materials_library.add_materials_bulk(self.db_path, records)
        return records

    def export_csv(self, path: str | Path) -> None:
        materials_csv.export_materials_csv(path, self.list_materials())
