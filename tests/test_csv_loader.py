from boardcomposer.io import load_project_from_csv


def test_load_project_from_csv():
    project = load_project_from_csv("data/samples/basic_boards.csv")

    assert len(project.boards) == 3
    assert project.boards[0].id == "A"
    assert project.total_area_mm2 == 1100000
