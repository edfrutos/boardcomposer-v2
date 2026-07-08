import csv
from pathlib import Path

from boardcomposer import Board, Project


def load_project_from_csv(path: str | Path) -> Project:
    project = Project()

    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            project.add_board(
                Board(
                    id=row.get("id") or None,
                    length_mm=float(row["length_mm"]),
                    width_mm=float(row["width_mm"]),
                    thickness_mm=float(row["thickness_mm"]),
                )
            )

    return project
