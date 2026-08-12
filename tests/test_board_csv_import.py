import pytest

from studio.project.board_csv_import import BoardCsvImportError, load_boards_from_csv


def _write_csv(tmp_path, content: str):
    path = tmp_path / "tableros.csv"
    path.write_text(content, encoding="utf-8")
    return str(path)


def test_loads_boards_with_required_columns(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nT-101,1200,600,19\nT-102,800,400,16\n",
    )

    boards = load_boards_from_csv(path)

    assert len(boards) == 2
    assert boards[0].board_id == "T-101"
    assert boards[0].length_mm == 1200
    assert boards[0].width_mm == 600
    assert boards[0].thickness_mm == 19
    assert boards[0].material == "Demo"


def test_honors_optional_material_column(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,material\n"
        "T-101,1200,600,19,Retal - contrachapado\n",
    )

    boards = load_boards_from_csv(path)

    assert boards[0].material == "Retal - contrachapado"


def test_missing_required_column_raises(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm,width_mm\nT-101,1200,600\n")

    with pytest.raises(BoardCsvImportError):
        load_boards_from_csv(path)


def test_empty_id_raises(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm,width_mm,thickness_mm\n,1200,600,19\n")

    with pytest.raises(BoardCsvImportError):
        load_boards_from_csv(path)


def test_duplicate_id_within_file_raises(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nT-101,1200,600,19\nT-101,800,400,19\n",
    )

    with pytest.raises(BoardCsvImportError):
        load_boards_from_csv(path)


def test_duplicate_id_against_existing_ids_raises(tmp_path):
    path = _write_csv(
        tmp_path, "id,length_mm,width_mm,thickness_mm\nT-101,1200,600,19\n"
    )

    with pytest.raises(BoardCsvImportError):
        load_boards_from_csv(path, existing_ids=frozenset({"T-101"}))


def test_non_numeric_dimension_raises(tmp_path):
    path = _write_csv(
        tmp_path, "id,length_mm,width_mm,thickness_mm\nT-101,abc,600,19\n"
    )

    with pytest.raises(BoardCsvImportError):
        load_boards_from_csv(path)


@pytest.mark.parametrize("bad_value", ["0", "-1", "nan", "inf"])
def test_non_finite_or_non_positive_dimension_raises(tmp_path, bad_value):
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm\nT-101,{bad_value},600,19\n",
    )

    with pytest.raises(BoardCsvImportError):
        load_boards_from_csv(path)


def test_empty_file_raises(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm,width_mm,thickness_mm\n")

    with pytest.raises(BoardCsvImportError):
        load_boards_from_csv(path)


def test_quantity_defaults_to_one_board_when_the_column_is_absent(tmp_path):
    path = _write_csv(
        tmp_path, "id,length_mm,width_mm,thickness_mm\nT-101,1200,600,19\n"
    )

    boards = load_boards_from_csv(path)

    assert [board.board_id for board in boards] == ["T-101"]


def test_quantity_expands_a_row_into_several_identical_boards(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nT-101,1200,600,19,3\n",
    )

    boards = load_boards_from_csv(path)

    assert [board.board_id for board in boards] == ["T-101", "T-101-2", "T-101-3"]
    assert all(board.length_mm == 1200 for board in boards)


@pytest.mark.parametrize("header", ["Cantidad", "CANTIDAD", "Quantity", "QUANTITY"])
def test_quantity_column_accepts_spanish_name_and_any_case(tmp_path, header):
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm,{header}\nT-101,1200,600,19,3\n",
    )

    boards = load_boards_from_csv(path)

    assert [board.board_id for board in boards] == ["T-101", "T-101-2", "T-101-3"]
    assert all(board.width_mm == 600 for board in boards)


@pytest.mark.parametrize("header", ["Material", "MATERIAL"])
def test_material_column_accepts_any_case(tmp_path, header):
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm,{header}\nT-101,1200,600,19,Roble\n",
    )

    boards = load_boards_from_csv(path)

    assert boards[0].material == "Roble"


def test_quantity_combines_with_other_rows_in_the_same_file(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\n"
        "T-101,1200,600,19,2\n"
        "T-200,800,400,19,\n",
    )

    boards = load_boards_from_csv(path)

    assert [board.board_id for board in boards] == ["T-101", "T-101-2", "T-200"]


def test_rejects_non_integer_quantity(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nT-101,1200,600,19,dos\n",
    )

    with pytest.raises(BoardCsvImportError, match="quantity debe ser un número entero"):
        load_boards_from_csv(path)


@pytest.mark.parametrize("value", ["0", "-2"])
def test_rejects_non_positive_quantity(tmp_path, value):
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm,quantity\nT-101,1200,600,19,{value}\n",
    )

    with pytest.raises(BoardCsvImportError, match="quantity debe ser 1 o mayor"):
        load_boards_from_csv(path)


def test_rejects_a_quantity_derived_id_that_collides_within_the_file(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\n"
        "T-101,1200,600,19,2\n"
        "T-101-2,800,400,19,\n",
    )

    with pytest.raises(BoardCsvImportError, match="repetido 'T-101-2'"):
        load_boards_from_csv(path)


def test_rejects_a_quantity_derived_id_that_collides_with_the_project(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nT-101,1200,600,19,2\n",
    )

    with pytest.raises(BoardCsvImportError, match="repetido 'T-101-2'"):
        load_boards_from_csv(path, existing_ids=frozenset({"T-101-2"}))
