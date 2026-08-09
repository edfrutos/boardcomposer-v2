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
                board_id = row.get("id") or None
                length_mm = float(row["length_mm"])
                width_mm = float(row["width_mm"])
                thickness_mm = float(row["thickness_mm"])
            except (TypeError, ValueError) as error:
                raise LoaderError(f"Fila {line_number}: {error}") from error

            quantity_raw = (row.get("quantity") or "").strip()
            if quantity_raw:
                try:
                    quantity = int(quantity_raw)
                except ValueError as error:
                    raise LoaderError(
                        f"Fila {line_number}: quantity debe ser un número entero "
                        f"(se recibió {quantity_raw!r})"
                    ) from error
                if quantity < 1:
                    raise LoaderError(
                        f"Fila {line_number}: quantity debe ser 1 o mayor "
                        f"(se recibió {quantity})"
                    )
            else:
                quantity = 1

            # Sin id no hay nada que derivar: las N boards quedan con
            # id=None, igual que hoy con quantity=1 — el Core nunca ha
            # exigido ni validado unicidad de id, ni siquiera literal.
            if board_id is None:
                unit_ids: list[str | None] = [None] * quantity
            else:
                unit_ids = [board_id] + [
                    f"{board_id}-{suffix}" for suffix in range(2, quantity + 1)
                ]

            material = (row.get("material") or "").strip()

            for unit_id in unit_ids:
                try:
                    board = Board(
                        id=unit_id,
                        length_mm=length_mm,
                        width_mm=width_mm,
                        thickness_mm=thickness_mm,
                        material=material,
                    )
                except (TypeError, ValueError) as error:
                    raise LoaderError(f"Fila {line_number}: {error}") from error

                project.add_board(board)

    if not project.boards:
        raise LoaderError("El CSV no contiene ninguna tabla")

    return project
