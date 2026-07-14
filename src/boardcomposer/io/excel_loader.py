from pathlib import Path

from openpyxl import load_workbook

from boardcomposer import Board, Project


def load_project_from_excel(path: str | Path) -> Project:
    project = Project()

    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        rows = workbook.active.iter_rows(values_only=True)
        header = [str(cell).strip() for cell in next(rows)]

        for row in rows:
            if all(value is None for value in row):
                continue

            data = dict(zip(header, row, strict=True))
            project.add_board(
                Board(
                    id=data.get("id") or None,
                    length_mm=float(data["length_mm"]),
                    width_mm=float(data["width_mm"]),
                    thickness_mm=float(data["thickness_mm"]),
                )
            )
    finally:
        workbook.close()

    return project
