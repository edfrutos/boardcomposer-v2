import csv
from pathlib import Path

from boardcomposer import Board, Project
from boardcomposer.io.errors import LoaderError

REQUIRED_COLUMNS = ("length_mm", "width_mm", "thickness_mm")


def load_project_from_csv(path: str | Path) -> Project:
    project = Project()

    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        header = reader.fieldnames or []
        missing = [column for column in REQUIRED_COLUMNS if column not in header]
        if missing:
            raise LoaderError(
                f"Faltan columnas obligatorias en el CSV: {', '.join(missing)}"
            )

        # Numeración igual que la del importador de Studio: la fila 1 es la
        # cabecera, así que los datos empiezan en la 2 y el número coincide
        # con el que ve el usuario en su editor.
        for line_number, row in enumerate(reader, start=2):
            try:
                board = Board(
                    id=row.get("id") or None,
                    length_mm=float(row["length_mm"]),
                    width_mm=float(row["width_mm"]),
                    thickness_mm=float(row["thickness_mm"]),
                )
            except (TypeError, ValueError) as error:
                raise LoaderError(f"Fila {line_number}: {error}") from error

            project.add_board(board)

    if not project.boards:
        raise LoaderError("El CSV no contiene ninguna tabla")

    return project
