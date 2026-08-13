import pytest

from studio.project.materials_csv import (
    MaterialsCsvError,
    export_materials_csv,
    import_materials_csv,
)
from studio.project.materials_library import MaterialRecord


def _write(path, text):
    path.write_text(text, encoding="utf-8")
    return path


def test_import_materials_csv_reads_the_basic_columns(tmp_path):
    path = _write(
        tmp_path / "materials.csv",
        "id,name,thickness_mm,provider,price,price_unit\n"
        "AGL18,Aglomerado,18,Leroy,25.5,board\n",
    )

    materials = import_materials_csv(path)

    assert len(materials) == 1
    assert materials[0].material_id == "AGL18"
    assert materials[0].name == "Aglomerado"
    assert materials[0].thickness_mm == 18
    assert materials[0].provider == "Leroy"
    assert materials[0].price == 25.5
    assert materials[0].price_unit == "board"


def test_import_materials_csv_defaults_optional_columns(tmp_path):
    path = _write(
        tmp_path / "materials.csv", "id,name,thickness_mm\nAGL18,Aglomerado,18\n"
    )

    materials = import_materials_csv(path)

    assert materials[0].provider == ""
    assert materials[0].price == 0.0
    assert materials[0].price_unit == "board"


@pytest.mark.parametrize(
    "header",
    [
        "Id,Nombre,Grosor_mm\nAGL18,Aglomerado,18\n",
        "ID,NOMBRE,GROSOR\nAGL18,Aglomerado,18\n",
    ],
)
def test_import_materials_csv_accepts_spanish_and_uppercase_column_aliases(
    tmp_path, header
):
    # DT-0026 lesson applied proactively: a column named the way the rest
    # of the app's UI is labeled must not silently fail to match.
    path = _write(tmp_path / "materials.csv", header)

    materials = import_materials_csv(path)

    assert materials[0].material_id == "AGL18"
    assert materials[0].name == "Aglomerado"
    assert materials[0].thickness_mm == 18


@pytest.mark.parametrize("value", ["tablero", "Board", "TABLERO"])
def test_import_materials_csv_accepts_board_price_unit_aliases(tmp_path, value):
    path = _write(
        tmp_path / "materials.csv",
        f"id,name,thickness_mm,price_unit\nAGL18,Aglomerado,18,{value}\n",
    )

    materials = import_materials_csv(path)

    assert materials[0].price_unit == "board"


@pytest.mark.parametrize("value", ["m2", "M2", "m²"])
def test_import_materials_csv_accepts_m2_price_unit_aliases(tmp_path, value):
    path = _write(
        tmp_path / "materials.csv",
        f"id,name,thickness_mm,price_unit\nAGL18,Aglomerado,18,{value}\n",
    )

    materials = import_materials_csv(path)

    assert materials[0].price_unit == "m2"


def test_import_materials_csv_rejects_missing_required_columns(tmp_path):
    path = _write(tmp_path / "materials.csv", "id,name\nAGL18,Aglomerado\n")

    with pytest.raises(MaterialsCsvError, match="Faltan columnas"):
        import_materials_csv(path)


def test_import_materials_csv_rejects_a_missing_id(tmp_path):
    path = _write(tmp_path / "materials.csv", "id,name,thickness_mm\n,Aglomerado,18\n")

    with pytest.raises(MaterialsCsvError, match="falta el id"):
        import_materials_csv(path)


def test_import_materials_csv_rejects_a_missing_name(tmp_path):
    path = _write(tmp_path / "materials.csv", "id,name,thickness_mm\nAGL18,,18\n")

    with pytest.raises(MaterialsCsvError, match="falta el nombre"):
        import_materials_csv(path)


def test_import_materials_csv_rejects_a_non_numeric_thickness(tmp_path):
    path = _write(
        tmp_path / "materials.csv", "id,name,thickness_mm\nAGL18,Aglomerado,abc\n"
    )

    with pytest.raises(MaterialsCsvError, match="no numérico"):
        import_materials_csv(path)


def test_import_materials_csv_rejects_a_non_positive_thickness(tmp_path):
    path = _write(
        tmp_path / "materials.csv", "id,name,thickness_mm\nAGL18,Aglomerado,0\n"
    )

    with pytest.raises(MaterialsCsvError, match="mayor que 0"):
        import_materials_csv(path)


def test_import_materials_csv_rejects_a_non_numeric_price(tmp_path):
    path = _write(
        tmp_path / "materials.csv",
        "id,name,thickness_mm,price\nAGL18,Aglomerado,18,abc\n",
    )

    with pytest.raises(MaterialsCsvError, match="no numérico"):
        import_materials_csv(path)


def test_import_materials_csv_rejects_an_unknown_price_unit(tmp_path):
    path = _write(
        tmp_path / "materials.csv",
        "id,name,thickness_mm,price_unit\nAGL18,Aglomerado,18,litre\n",
    )

    with pytest.raises(MaterialsCsvError, match="price_unit"):
        import_materials_csv(path)


def test_import_materials_csv_rejects_a_duplicate_id_within_the_file(tmp_path):
    path = _write(
        tmp_path / "materials.csv",
        "id,name,thickness_mm\nAGL18,Aglomerado,18\nAGL18,Otro,10\n",
    )

    with pytest.raises(MaterialsCsvError, match="id repetido"):
        import_materials_csv(path)


def test_import_materials_csv_rejects_a_collision_with_existing_ids(tmp_path):
    path = _write(
        tmp_path / "materials.csv", "id,name,thickness_mm\nAGL18,Aglomerado,18\n"
    )

    with pytest.raises(MaterialsCsvError, match="id repetido"):
        import_materials_csv(path, existing_ids=frozenset({"AGL18"}))


def test_import_materials_csv_rejects_an_empty_file(tmp_path):
    path = _write(tmp_path / "materials.csv", "id,name,thickness_mm\n")

    with pytest.raises(MaterialsCsvError, match="no contiene ningún material"):
        import_materials_csv(path)


def test_export_then_import_round_trips(tmp_path):
    materials = [
        MaterialRecord("AGL10", "Aglomerado", 10, "Leroy", 20.0, "board", "now"),
        MaterialRecord("PINO25", "Pino", 25, "", 0.0, "m2", "now"),
    ]
    path = tmp_path / "export.csv"

    export_materials_csv(path, materials)
    imported = import_materials_csv(path)

    assert [m.material_id for m in imported] == ["AGL10", "PINO25"]
    assert imported[0].name == "Aglomerado"
    assert imported[0].provider == "Leroy"
    assert imported[0].price == 20.0
    assert imported[1].price_unit == "m2"
