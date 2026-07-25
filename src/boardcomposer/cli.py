import argparse
import json

from boardcomposer import Board, Project, ProjectConstraints

from boardcomposer.io import (
    LoaderError,
    load_project_from_csv,
    load_project_from_excel,
)
from boardcomposer.plugin_visibility import plugin_summary
from boardcomposer.presenters import solution_to_text, solutions_to_json

from boardcomposer.solver import GeometrySolver
from boardcomposer.solver.strategies import strategy_by_name


def build_demo_project() -> Project:

    project = Project()

    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))

    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))

    return project


def print_plugin_summary(as_json: bool = False) -> None:
    summary = plugin_summary()

    if as_json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return

    for group, data in summary.items():
        print(f"{group}:")

        if data["installed"]:
            for name in data["installed"]:
                print(f"  - {name}")
        else:
            print("  (ninguno instalado)")

        for error in data["errors"]:
            print(f"  ! {error['name']}: {error['error']}")


def main() -> None:

    parser = argparse.ArgumentParser(description="BoardComposer CLI")

    subparsers = parser.add_subparsers(dest="command")
    plugins_parser = subparsers.add_parser(
        "plugins", help="Lista los plugins instalados y sus errores de carga"
    )
    plugins_parser.add_argument(
        "--json", action="store_true", help="Mostrar salida JSON"
    )

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--csv", help="Ruta a un CSV con tablas")
    input_group.add_argument("--excel", help="Ruta a un Excel (.xlsx) con tablas")

    parser.add_argument("--max-length", type=float, help="Largo máximo en mm")

    parser.add_argument("--max-width", type=float, help="Ancho máximo en mm")

    parser.add_argument(
        "--allow-rotation", action="store_true", help="Permitir rotar tablas"
    )

    parser.add_argument("--json", action="store_true", help="Mostrar salida JSON")
    parser.add_argument(
        "--strategy", choices=["balanced", "material", "compact"], default="balanced"
    )
    parser.add_argument(
        "--top", type=int, default=5, help="Número máximo de soluciones a mostrar"
    )

    args = parser.parse_args()

    if args.command == "plugins":
        print_plugin_summary(as_json=args.json)
        return

    # Un fichero de entrada mal formado es el error más habitual de esta
    # herramienta, y hasta ahora salía como traza de Python (ValueError,
    # KeyError o FileNotFoundError en bruto). Aquí se traduce a una línea
    # legible en stderr y código de salida 1.
    try:
        if args.csv:
            project = load_project_from_csv(args.csv)
        elif args.excel:
            project = load_project_from_excel(args.excel)
        else:
            project = build_demo_project()
    except LoaderError as error:
        raise SystemExit(f"Error al leer el fichero de entrada: {error}") from error
    except OSError as error:
        raise SystemExit(f"No se pudo abrir el fichero de entrada: {error}") from error

    project.constraints = ProjectConstraints(
        max_length_mm=args.max_length,
        max_width_mm=args.max_width,
        allow_rotation=args.allow_rotation,
    )

    strategy = strategy_by_name(args.strategy)

    solutions = GeometrySolver(project, strategy=strategy).solve()

    if not solutions:
        print("No hay soluciones válidas.")

        return

    if args.json:
        print(
            solutions_to_json(
                project=project,
                strategy=strategy,
                solutions=solutions,
                top=args.top,
            )
        )

        return

    print(solution_to_text(project, solutions))
