import pytest

from studio.materials_service import MaterialsLibraryService
from studio.project.materials_csv import MaterialsCsvError
from studio.project.materials_library import MaterialsLibraryError


@pytest.fixture
def service(tmp_path):
    return MaterialsLibraryService(db_path=tmp_path / "materiales.db")


def test_add_and_list_materials(service):
    service.add("AGL18", "Aglomerado", 18, provider="Leroy", price=25.5)

    materials = service.list_materials()

    assert len(materials) == 1
    assert materials[0].material_id == "AGL18"


def test_update_material(service):
    service.add("AGL18", "Aglomerado", 18)

    service.update("AGL18", "Aglomerado premium", 19, price=30.0, price_unit="m2")

    materials = service.list_materials()
    assert materials[0].name == "Aglomerado premium"
    assert materials[0].price_unit == "m2"


def test_delete_material(service):
    service.add("AGL18", "Aglomerado", 18)

    service.delete("AGL18")

    assert service.list_materials() == []


def test_add_rejects_a_duplicate_id(service):
    service.add("AGL18", "Aglomerado", 18)

    with pytest.raises(MaterialsLibraryError):
        service.add("AGL18", "Otro", 10)


def test_export_then_import_csv_round_trips(service, tmp_path):
    service.add("AGL18", "Aglomerado", 18, provider="Leroy", price=25.5)
    service.add("PINO25", "Pino", 25)
    csv_path = tmp_path / "export.csv"

    service.export_csv(csv_path)

    other = MaterialsLibraryService(db_path=tmp_path / "other.db")
    other.import_csv(csv_path)

    names = {m.material_id for m in other.list_materials()}
    assert names == {"AGL18", "PINO25"}


def test_import_csv_rejects_a_collision_with_an_existing_material(service, tmp_path):
    service.add("AGL18", "Aglomerado", 18)
    csv_path = tmp_path / "import.csv"
    csv_path.write_text("id,name,thickness_mm\nAGL18,Otro,10\n", encoding="utf-8")

    with pytest.raises(MaterialsCsvError):
        service.import_csv(csv_path)

    assert len(service.list_materials()) == 1
