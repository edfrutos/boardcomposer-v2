import pytest

from studio.project.materials_library import (
    MaterialsLibraryError,
    MaterialRecord,
    add_material,
    add_materials_bulk,
    delete_material,
    list_materials,
    update_material,
)


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "materiales.db"


def test_list_materials_is_empty_for_a_fresh_database(db_path):
    assert list_materials(db_path) == []


def test_add_material_appears_in_list_materials(db_path):
    add_material(
        db_path,
        "AGL18",
        "Aglomerado",
        18,
        provider="Leroy",
        price=25.5,
        price_unit="board",
    )

    materials = list_materials(db_path)

    assert len(materials) == 1
    assert materials[0].material_id == "AGL18"
    assert materials[0].name == "Aglomerado"
    assert materials[0].thickness_mm == 18
    assert materials[0].provider == "Leroy"
    assert materials[0].price == 25.5
    assert materials[0].price_unit == "board"


def test_add_material_defaults_provider_price_and_unit(db_path):
    add_material(db_path, "AGL18", "Aglomerado", 18)

    materials = list_materials(db_path)

    assert materials[0].provider == ""
    assert materials[0].price == 0.0
    assert materials[0].price_unit == "board"


def test_list_materials_is_sorted_by_name_then_thickness(db_path):
    add_material(db_path, "PINO25", "Pino", 25)
    add_material(db_path, "AGL10", "Aglomerado", 10)
    add_material(db_path, "AGL18", "Aglomerado", 18)

    materials = list_materials(db_path)

    assert [m.material_id for m in materials] == ["AGL10", "AGL18", "PINO25"]


def test_add_material_rejects_an_empty_id(db_path):
    with pytest.raises(MaterialsLibraryError, match="necesita un id"):
        add_material(db_path, "  ", "Aglomerado", 18)


def test_add_material_rejects_an_empty_name(db_path):
    with pytest.raises(MaterialsLibraryError, match="necesita un nombre"):
        add_material(db_path, "AGL18", "  ", 18)


def test_add_material_rejects_a_duplicate_id(db_path):
    add_material(db_path, "AGL18", "Aglomerado", 18)

    with pytest.raises(MaterialsLibraryError, match="Ya existe un material"):
        add_material(db_path, "AGL18", "Otro", 10)


@pytest.mark.parametrize("value", [0, -10, float("nan"), float("inf")])
def test_add_material_rejects_unusable_thickness(db_path, value):
    with pytest.raises(MaterialsLibraryError, match="número finito mayor que 0"):
        add_material(db_path, "AGL18", "Aglomerado", value)


@pytest.mark.parametrize("value", [-1, float("nan"), float("inf")])
def test_add_material_rejects_unusable_price(db_path, value):
    with pytest.raises(MaterialsLibraryError, match="no negativo"):
        add_material(db_path, "AGL18", "Aglomerado", 18, price=value)


def test_add_material_rejects_an_unknown_price_unit(db_path):
    with pytest.raises(MaterialsLibraryError, match="price_unit"):
        add_material(db_path, "AGL18", "Aglomerado", 18, price_unit="litre")


def test_update_material_changes_its_fields(db_path):
    add_material(db_path, "AGL18", "Aglomerado", 18)

    update_material(
        db_path,
        "AGL18",
        "Aglomerado premium",
        19,
        provider="Bricor",
        price=30.0,
        price_unit="m2",
    )

    materials = list_materials(db_path)
    assert materials[0].name == "Aglomerado premium"
    assert materials[0].thickness_mm == 19
    assert materials[0].provider == "Bricor"
    assert materials[0].price == 30.0
    assert materials[0].price_unit == "m2"


def test_update_material_rejects_an_unknown_id(db_path):
    with pytest.raises(MaterialsLibraryError, match="No existe ningún material"):
        update_material(db_path, "ghost", "Aglomerado", 18)


def test_delete_material_removes_it(db_path):
    add_material(db_path, "AGL18", "Aglomerado", 18)

    delete_material(db_path, "AGL18")

    assert list_materials(db_path) == []


def test_delete_material_rejects_an_unknown_id(db_path):
    with pytest.raises(MaterialsLibraryError, match="No existe ningún material"):
        delete_material(db_path, "ghost")


def test_add_materials_bulk_adds_every_record(db_path):
    records = [
        MaterialRecord("AGL10", "Aglomerado", 10, "", 0.0, "board", ""),
        MaterialRecord("AGL18", "Aglomerado", 18, "", 0.0, "board", ""),
    ]

    add_materials_bulk(db_path, records)

    assert [m.material_id for m in list_materials(db_path)] == ["AGL10", "AGL18"]


def test_add_materials_bulk_adds_nothing_on_a_duplicate_id_within_the_batch(db_path):
    records = [
        MaterialRecord("AGL10", "Aglomerado", 10, "", 0.0, "board", ""),
        MaterialRecord("AGL10", "Aglomerado", 18, "", 0.0, "board", ""),
    ]

    with pytest.raises(MaterialsLibraryError, match="Id repetido"):
        add_materials_bulk(db_path, records)

    assert list_materials(db_path) == []


def test_add_materials_bulk_adds_nothing_on_a_collision_with_an_existing_id(db_path):
    add_material(db_path, "AGL10", "Aglomerado", 10)
    records = [MaterialRecord("AGL10", "Aglomerado", 18, "", 0.0, "board", "")]

    with pytest.raises(MaterialsLibraryError, match="Ya existe un material"):
        add_materials_bulk(db_path, records)

    assert len(list_materials(db_path)) == 1


def test_add_materials_bulk_adds_nothing_on_an_invalid_record(db_path):
    records = [
        MaterialRecord("AGL10", "Aglomerado", 10, "", 0.0, "board", ""),
        MaterialRecord("BAD", "Malo", -1, "", 0.0, "board", ""),
    ]

    with pytest.raises(MaterialsLibraryError):
        add_materials_bulk(db_path, records)

    assert list_materials(db_path) == []
