import pytest

from studio.project import CsvImportError, load_pieces_from_csv


def _write_csv(tmp_path, content: str):
    path = tmp_path / "piezas.csv"
    path.write_text(content, encoding="utf-8")
    return path


def test_loads_one_piece_per_row(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nP-101,700,300,19\nP-102,520,360,16\n",
    )

    pieces = load_pieces_from_csv(path)

    assert [piece.piece_id for piece in pieces] == ["P-101", "P-102"]
    assert pieces[0].length_mm == 700
    assert pieces[0].width_mm == 300
    assert pieces[0].thickness_mm == 19
    assert pieces[1].thickness_mm == 16


def test_honors_optional_material_column(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,material\n"
        "P-101,700,300,19,Roble\n"
        "P-102,520,360,19,\n",
    )

    pieces = load_pieces_from_csv(path)

    assert pieces[0].material == "Roble"
    # Empty cell falls back to StudioPiece's default, same as no column.
    assert pieces[1].material == "Demo"


def test_rejects_missing_required_columns(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm\nP-101,700\n")

    with pytest.raises(CsvImportError, match="width_mm"):
        load_pieces_from_csv(path)


def test_rejects_a_row_without_id(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\n,700,300,19\n",
    )

    with pytest.raises(CsvImportError, match="Fila 2"):
        load_pieces_from_csv(path)


def test_rejects_duplicate_ids_within_the_file(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nP-101,700,300,19\nP-101,520,360,19\n",
    )

    with pytest.raises(CsvImportError, match="repetido 'P-101'"):
        load_pieces_from_csv(path)


def test_rejects_ids_already_in_the_project(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nP-001,700,300,19\n",
    )

    with pytest.raises(CsvImportError, match="repetido 'P-001'"):
        load_pieces_from_csv(path, existing_ids=frozenset({"P-001"}))


def test_rejects_non_numeric_dimensions(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nP-101,ancho,300,19\n",
    )

    with pytest.raises(CsvImportError, match="Fila 2"):
        load_pieces_from_csv(path)


@pytest.mark.parametrize("value", ["nan", "inf", "-inf", "1e400"])
def test_rejects_non_finite_dimensions(tmp_path, value):
    # float() se traga "nan"/"inf" sin error, y "1e400" desborda a inf.
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm\nP-101,{value},300,19\n",
    )

    with pytest.raises(CsvImportError, match="número finito"):
        load_pieces_from_csv(path)


@pytest.mark.parametrize("value", ["0", "-500"])
@pytest.mark.parametrize("column", ["length_mm", "width_mm", "thickness_mm"])
def test_rejects_non_positive_dimensions(tmp_path, column, value):
    dimensions = {"length_mm": "700", "width_mm": "300", "thickness_mm": "19"}
    dimensions[column] = value
    row = ",".join(dimensions[key] for key in ("length_mm", "width_mm", "thickness_mm"))
    path = _write_csv(tmp_path, f"id,length_mm,width_mm,thickness_mm\nP-101,{row}\n")

    with pytest.raises(CsvImportError, match=column):
        load_pieces_from_csv(path)


def test_rejects_an_empty_csv(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm,width_mm,thickness_mm\n")

    with pytest.raises(CsvImportError, match="ninguna pieza"):
        load_pieces_from_csv(path)


def test_quantity_defaults_to_one_piece_when_the_column_is_absent(tmp_path):
    path = _write_csv(
        tmp_path, "id,length_mm,width_mm,thickness_mm\nP-101,700,300,19\n"
    )

    pieces = load_pieces_from_csv(path)

    assert [piece.piece_id for piece in pieces] == ["P-101"]


def test_quantity_defaults_to_one_piece_when_the_cell_is_empty(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nP-101,700,300,19,\n",
    )

    pieces = load_pieces_from_csv(path)

    assert [piece.piece_id for piece in pieces] == ["P-101"]


def test_quantity_expands_a_row_into_several_identical_pieces(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nP-101,700,300,19,3\n",
    )

    pieces = load_pieces_from_csv(path)

    assert [piece.piece_id for piece in pieces] == ["P-101", "P-101-2", "P-101-3"]
    assert all(piece.length_mm == 700 for piece in pieces)
    assert all(piece.width_mm == 300 for piece in pieces)
    assert all(piece.thickness_mm == 19 for piece in pieces)


@pytest.mark.parametrize("header", ["Cantidad", "CANTIDAD", "Quantity", "QUANTITY"])
def test_quantity_column_accepts_spanish_name_and_any_case(tmp_path, header):
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm,{header}\nP-101,700,300,19,3\n",
    )

    pieces = load_pieces_from_csv(path)

    assert [piece.piece_id for piece in pieces] == ["P-101", "P-101-2", "P-101-3"]


def test_quantity_expansion_honors_material(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,material,quantity\n"
        "P-101,700,300,19,Roble,2\n",
    )

    pieces = load_pieces_from_csv(path)

    assert all(piece.material == "Roble" for piece in pieces)


def test_quantity_combines_with_other_rows_in_the_same_file(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\n"
        "P-101,700,300,19,2\n"
        "P-200,500,250,19,\n",
    )

    pieces = load_pieces_from_csv(path)

    assert [piece.piece_id for piece in pieces] == ["P-101", "P-101-2", "P-200"]


def test_rejects_non_integer_quantity(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nP-101,700,300,19,dos\n",
    )

    with pytest.raises(CsvImportError, match="quantity debe ser un número entero"):
        load_pieces_from_csv(path)


@pytest.mark.parametrize("value", ["0", "-2"])
def test_rejects_non_positive_quantity(tmp_path, value):
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm,quantity\nP-101,700,300,19,{value}\n",
    )

    with pytest.raises(CsvImportError, match="quantity debe ser 1 o mayor"):
        load_pieces_from_csv(path)


def test_rejects_a_quantity_derived_id_that_collides_within_the_file(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\n"
        "P-101,700,300,19,2\n"
        "P-101-2,500,250,19,\n",
    )

    with pytest.raises(CsvImportError, match="repetido 'P-101-2'"):
        load_pieces_from_csv(path)


def test_rejects_a_quantity_derived_id_that_collides_with_the_project(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nP-101,700,300,19,2\n",
    )

    with pytest.raises(CsvImportError, match="repetido 'P-101-2'"):
        load_pieces_from_csv(path, existing_ids=frozenset({"P-101-2"}))
