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
