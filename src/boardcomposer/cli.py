import argparse

from boardcomposer import Board, Project, ProjectConstraints

from boardcomposer.io import load_project_from_csv
from boardcomposer.presenters import solution_to_text, solutions_to_json

from boardcomposer.solver import GeometrySolver
from boardcomposer.solver.strategies import strategy_by_name


def build_demo_project() -> Project:

    project = Project()

    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20, id="A"))

    project.add_board(Board(length_mm=1000, width_mm=300, thickness_mm=20, id="B"))

    return project


def main() -> None:

    parser = argparse.ArgumentParser(description="BoardComposer CLI")

    parser.add_argument("--csv", help="Ruta a un CSV con tablas")

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

    project = load_project_from_csv(args.csv) if args.csv else build_demo_project()

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
