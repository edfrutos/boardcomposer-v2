import pytest

from boardcomposer.io import LoaderError, load_project_from_csv


def _write_csv(tmp_path, content: str):
    path = tmp_path / "tablas.csv"
    path.write_text(content, encoding="utf-8")
    return path


def test_load_project_from_csv():
    project = load_project_from_csv("data/samples/basic_boards.csv")

    assert len(project.boards) == 3
    assert project.boards[0].id == "A"
    assert project.total_area_mm2 == 1100000


def test_rejects_a_csv_without_the_required_columns(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm\nT1,2000\n")

    with pytest.raises(LoaderError, match="width_mm"):
        load_project_from_csv(path)


def test_reports_the_line_number_of_a_non_numeric_dimension(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm\nT1,2000,300,19\nT2,ancho,300,19\n",
    )

    # La cabecera es la fila 1, así que la fila mala es la 3 — el mismo
    # número que ve el usuario en su editor.
    with pytest.raises(LoaderError, match="Fila 3"):
        load_project_from_csv(path)


@pytest.mark.parametrize("value", ["nan", "inf", "-500", "0"])
def test_reports_the_line_number_of_an_unusable_dimension(tmp_path, value):
    path = _write_csv(
        tmp_path, f"id,length_mm,width_mm,thickness_mm\nT1,{value},300,19\n"
    )

    with pytest.raises(LoaderError, match="Fila 2"):
        load_project_from_csv(path)


def test_rejects_a_csv_without_rows(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm,width_mm,thickness_mm\n")

    with pytest.raises(LoaderError, match="ninguna tabla"):
        load_project_from_csv(path)


def test_material_defaults_to_empty_string_when_the_column_is_absent(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm,width_mm,thickness_mm\nA,2000,300,20\n")

    project = load_project_from_csv(path)

    assert project.boards[0].material == ""


def test_material_is_honored_as_a_passive_label(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,material\nA,2000,300,20,Roble\n",
    )

    project = load_project_from_csv(path)

    assert project.boards[0].material == "Roble"


def test_quantity_defaults_to_one_board_when_the_column_is_absent(tmp_path):
    path = _write_csv(tmp_path, "id,length_mm,width_mm,thickness_mm\nA,2000,300,20\n")

    project = load_project_from_csv(path)

    assert [board.id for board in project.boards] == ["A"]


def test_quantity_expands_a_row_into_several_identical_boards(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nA,2000,300,20,3\n",
    )

    project = load_project_from_csv(path)

    assert [board.id for board in project.boards] == ["A", "A-2", "A-3"]
    assert all(board.length_mm == 2000 for board in project.boards)


@pytest.mark.parametrize("header", ["Cantidad", "CANTIDAD", "Quantity", "QUANTITY"])
def test_quantity_column_accepts_spanish_name_and_any_case(tmp_path, header):
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm,{header}\nA,2000,300,20,3\n",
    )

    project = load_project_from_csv(path)

    assert [board.id for board in project.boards] == ["A", "A-2", "A-3"]


def test_quantity_without_an_id_produces_boards_with_no_id(tmp_path):
    path = _write_csv(
        tmp_path,
        "length_mm,width_mm,thickness_mm,quantity\n2000,300,20,3\n",
    )

    project = load_project_from_csv(path)

    assert [board.id for board in project.boards] == [None, None, None]


def test_rejects_non_integer_quantity(tmp_path):
    path = _write_csv(
        tmp_path,
        "id,length_mm,width_mm,thickness_mm,quantity\nA,2000,300,20,dos\n",
    )

    with pytest.raises(LoaderError, match="quantity debe ser un número entero"):
        load_project_from_csv(path)


@pytest.mark.parametrize("value", ["0", "-2"])
def test_rejects_non_positive_quantity(tmp_path, value):
    path = _write_csv(
        tmp_path,
        f"id,length_mm,width_mm,thickness_mm,quantity\nA,2000,300,20,{value}\n",
    )

    with pytest.raises(LoaderError, match="quantity debe ser 1 o mayor"):
        load_project_from_csv(path)
