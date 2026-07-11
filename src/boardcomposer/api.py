"""Minimal HTTP API over the Core (IDE-0006 — API pública; IDE-0007 Fase F).

Thin adapter, same role as cli.py but over HTTP instead of argparse: it
never implements business logic itself, only translates requests into
calls to the same Core the CLI and Studio already use.

Scope note: this is a first, minimal contract — create a project inline,
run the solver, get results back. No authentication, versioning,
persistence or rate limiting yet. docs/masterplan/DOC-008-API.md lists
those as still-pending decisions ("Pendiente de: definir los contratos
públicos...", "En revisión"), not as requirements for this first cut.

The /assist/* routes expose boardcomposer.ai (IDE-0007) the same way:
no AI logic of its own, just request/response translation. create_app()
defaults to the "mock" AIProvider — there's still no real provider wired
in (docs/masterplan/DOC-004-Backlog.md), so /assist/project and
/assist/strategy will 502 with the default provider until one exists,
since MockAIProvider's canned reply isn't the JSON those two expect.
/assist/explain works today: it only needs free text back. ai_provider
is an explicit create_app() parameter so tests (and, later, a real
provider) can supply one without changing this module.
"""

import json

from flask import Flask, Response, jsonify, request

from boardcomposer.ai import (
    AIProvider,
    ProjectFromTextError,
    SuggestStrategyError,
    explain_solution,
    project_from_text,
    provider_by_name,
    suggest_strategy,
)
from boardcomposer.domain import Board, Project, ProjectConstraints
from boardcomposer.presenters import solutions_to_json
from boardcomposer.solver import GeometrySolver
from boardcomposer.solver.strategies import OptimizationStrategy, strategy_by_name

STRATEGY_NAMES = ("balanced", "material", "compact")


def _parse_boards(boards_data) -> list[Board]:
    return [
        Board(
            id=board.get("id"),
            length_mm=float(board["length_mm"]),
            width_mm=float(board["width_mm"]),
            thickness_mm=float(board.get("thickness_mm", 1)),
        )
        for board in boards_data
    ]


def _parse_constraints(constraints_data: dict) -> ProjectConstraints:
    return ProjectConstraints(
        max_length_mm=constraints_data.get("max_length_mm"),
        max_width_mm=constraints_data.get("max_width_mm"),
        allow_rotation=bool(constraints_data.get("allow_rotation", False)),
        allow_cutting=bool(constraints_data.get("allow_cutting", False)),
    )


def _parse_top(payload: dict) -> int:
    top = payload.get("top", 5)
    if not isinstance(top, int) or isinstance(top, bool) or top < 1:
        raise ValueError("'top' debe ser un entero mayor que 0.")
    return top


def _solve_response(project: Project, strategy: OptimizationStrategy, top: int):
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


def create_app(ai_provider: AIProvider | None = None) -> Flask:
    provider = ai_provider or provider_by_name("mock")
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
            boards = _parse_boards(boards_data)
        except (KeyError, TypeError, ValueError) as error:
            return jsonify(error=f"Tabla inválida: {error}"), 400

        constraints_data = payload.get("constraints") or {}
        if not isinstance(constraints_data, dict):
            return jsonify(error="'constraints' debe ser un objeto."), 400

        try:
            constraints = _parse_constraints(constraints_data)
        except (TypeError, ValueError) as error:
            return jsonify(error=f"Restricciones inválidas: {error}"), 400

        project = Project(boards=boards, constraints=constraints)

        strategy_name = payload.get("strategy", "balanced")
        try:
            strategy = strategy_by_name(strategy_name)
        except ValueError as error:
            return jsonify(error=str(error)), 400

        try:
            top = _parse_top(payload)
        except ValueError as error:
            return jsonify(error=str(error)), 400

        return _solve_response(project, strategy, top)

    @app.post("/assist/project")
    def assist_project():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="El cuerpo debe ser un objeto JSON."), 400

        text = payload.get("text")
        if not isinstance(text, str) or not text.strip():
            return jsonify(error="'text' debe ser una cadena no vacía."), 400

        try:
            project = project_from_text(text, provider)
        except ProjectFromTextError as error:
            return jsonify(error=str(error)), 502

        return jsonify(
            boards=[
                {
                    "id": board.id,
                    "length_mm": board.length_mm,
                    "width_mm": board.width_mm,
                    "thickness_mm": board.thickness_mm,
                }
                for board in project.boards
            ],
            constraints={
                "max_length_mm": project.constraints.max_length_mm,
                "max_width_mm": project.constraints.max_width_mm,
                "allow_rotation": project.constraints.allow_rotation,
                "allow_cutting": project.constraints.allow_cutting,
            },
        )

    @app.post("/assist/strategy")
    def assist_strategy():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="El cuerpo debe ser un objeto JSON."), 400

        boards_data = payload.get("boards")
        if not isinstance(boards_data, list) or not boards_data:
            return jsonify(error="'boards' debe ser una lista no vacía."), 400

        try:
            boards = _parse_boards(boards_data)
        except (KeyError, TypeError, ValueError) as error:
            return jsonify(error=f"Tabla inválida: {error}"), 400

        constraints_data = payload.get("constraints") or {}
        if not isinstance(constraints_data, dict):
            return jsonify(error="'constraints' debe ser un objeto."), 400

        try:
            constraints = _parse_constraints(constraints_data)
        except (TypeError, ValueError) as error:
            return jsonify(error=f"Restricciones inválidas: {error}"), 400

        project = Project(boards=boards, constraints=constraints)

        goal = payload.get("goal", "")
        if not isinstance(goal, str):
            return jsonify(error="'goal' debe ser una cadena de texto."), 400

        try:
            strategy = suggest_strategy(project, provider, goal=goal)
        except SuggestStrategyError as error:
            return jsonify(error=str(error)), 502

        try:
            top = _parse_top(payload)
        except ValueError as error:
            return jsonify(error=str(error)), 400

        return _solve_response(project, strategy, top)

    @app.post("/assist/explain")
    def assist_explain():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="El cuerpo debe ser un objeto JSON."), 400

        boards_data = payload.get("boards")
        if not isinstance(boards_data, list) or not boards_data:
            return jsonify(error="'boards' debe ser una lista no vacía."), 400

        try:
            boards = _parse_boards(boards_data)
        except (KeyError, TypeError, ValueError) as error:
            return jsonify(error=f"Tabla inválida: {error}"), 400

        constraints_data = payload.get("constraints") or {}
        if not isinstance(constraints_data, dict):
            return jsonify(error="'constraints' debe ser un objeto."), 400

        try:
            constraints = _parse_constraints(constraints_data)
        except (TypeError, ValueError) as error:
            return jsonify(error=f"Restricciones inválidas: {error}"), 400

        project = Project(boards=boards, constraints=constraints)

        strategy_name = payload.get("strategy", "balanced")
        try:
            strategy = strategy_by_name(strategy_name)
        except ValueError as error:
            return jsonify(error=str(error)), 400

        solutions = GeometrySolver(project, strategy=strategy).solve()
        if not solutions:
            return jsonify(
                input_boards=len(project.boards),
                strategy=strategy.name,
                solutions=[],
                message="No se encontraron soluciones válidas para las restricciones dadas.",
            )

        explanation = explain_solution(solutions[0], provider)

        result = json.loads(solutions_to_json(project, strategy, solutions, top=1))
        result["assistant_explanation"] = explanation

        return jsonify(result)

    return app


if __name__ == "__main__":
    create_app().run()
