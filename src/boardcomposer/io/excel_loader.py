from pathlib import Path

from openpyxl import load_workbook

from boardcomposer import Board, Project
from boardcomposer.io.errors import LoaderError

REQUIRED_COLUMNS = ("length_mm", "width_mm", "thickness_mm")


def load_project_from_excel(path: str | Path) -> Project:
    project = Project()

    workbook = load_workbook(path, read_only=True, data_only=True)
    try:
        rows = workbook.active.iter_rows(values_only=True)
        try:
            header = [str(cell).strip() for cell in next(rows)]
        except StopIteration as error:
            # Un StopIteration escapando de aquí no sería un error legible,
            # sino un RuntimeError de generador agotado más arriba.
            raise LoaderError("El Excel está vacío: no tiene ni cabecera") from error

        missing = [column for column in REQUIRED_COLUMNS if column not in header]
        if missing:
            raise LoaderError(
                f"Faltan columnas obligatorias en el Excel: {', '.join(missing)}"
            )

        # La cabecera es la fila 1, igual que en el CSV.
        for line_number, row in enumerate(rows, start=2):
            if all(value is None for value in row):
                continue

            try:
                data = dict(zip(header, row, strict=True))
            except ValueError as error:
                raise LoaderError(
                    f"Fila {line_number}: tiene un número de celdas distinto "
                    f"al de la cabecera ({error})"
                ) from error

            try:
                board = Board(
                    id=data.get("id") or None,
                    length_mm=float(data["length_mm"]),
                    width_mm=float(data["width_mm"]),
                    thickness_mm=float(data["thickness_mm"]),
                )
            except (TypeError, ValueError) as error:
                raise LoaderError(f"Fila {line_number}: {error}") from error

            project.add_board(board)
    finally:
        workbook.close()

    if not project.boards:
        raise LoaderError("El Excel no contiene ninguna tabla")

    return project
