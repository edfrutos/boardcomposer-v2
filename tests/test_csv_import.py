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
