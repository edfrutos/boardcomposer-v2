"""Minimal HTTP API over the Core (IDE-0006 — API pública).

Thin adapter, same role as cli.py but over HTTP instead of argparse: it
never implements business logic itself, only translates requests into
calls to the same Core the CLI and Studio already use.

Scope note: this is a first, minimal contract — create a project inline,
run the solver, get results back. No authentication, versioning,
persistence or rate limiting yet. docs/masterplan/DOC-008-API.md lists
those as still-pending decisions ("Pendiente de: definir los contratos
públicos...", "En revisión"), not as requirements for this first cut.
"""

from flask import Flask, Response, jsonify, request

from boardcomposer.domain import Board, Project, ProjectConstraints
from boardcomposer.presenters import solutions_to_json
from boardcomposer.solver import GeometrySolver
from boardcomposer.solver.strategies import strategy_by_name

STRATEGY_NAMES = ("balanced", "material", "compact")


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/strategies")
    def strategies():
        return jsonify(strategies=list(STRATEGY_NAMES))

    @app.post("/solve")
    def solve():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="El cuerpo debe ser un objeto JSON."), 400

        boards_data = payload.get("boards")
        if not isinstance(boards_data, list) or not boards_data:
            return jsonify(error="'boards' debe ser una lista no vacía."), 400

        try:
            boards = [
                Board(
                    id=board.get("id"),
                    length_mm=float(board["length_mm"]),
                    width_mm=float(board["width_mm"]),
                    thickness_mm=float(board.get("thickness_mm", 1)),
                )
                for board in boards_data
            ]
        except (KeyError, TypeError, ValueError) as error:
            return jsonify(error=f"Tabla inválida: {error}"), 400

        constraints_data = payload.get("constraints") or {}
        if not isinstance(constraints_data, dict):
            return jsonify(error="'constraints' debe ser un objeto."), 400

        try:
            constraints = ProjectConstraints(
                max_length_mm=constraints_data.get("max_length_mm"),
                max_width_mm=constraints_data.get("max_width_mm"),
                allow_rotation=bool(constraints_data.get("allow_rotation", False)),
                allow_cutting=bool(constraints_data.get("allow_cutting", False)),
            )
        except (TypeError, ValueError) as error:
            return jsonify(error=f"Restricciones inválidas: {error}"), 400

        project = Project(boards=boards, constraints=constraints)

        strategy_name = payload.get("strategy", "balanced")
        try:
            strategy = strategy_by_name(strategy_name)
        except ValueError as error:
            return jsonify(error=str(error)), 400

        top = payload.get("top", 5)
        if not isinstance(top, int) or isinstance(top, bool) or top < 1:
            return jsonify(error="'top' debe ser un entero mayor que 0."), 400

        solutions = GeometrySolver(project, strategy=strategy).solve()
        if not solutions:
            return jsonify(
                input_boards=len(project.boards),
                strategy=strategy.name,
                solutions=[],
                message="No se encontraron soluciones válidas para las restricciones dadas.",
            )

        return Response(
            solutions_to_json(project, strategy, solutions, top),
            mimetype="application/json",
        )

    return app


if __name__ == "__main__":
    create_app().run()
