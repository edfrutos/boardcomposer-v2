"""Minimal HTTP API over the Core (IDE-0006 — API pública; IDE-0007 Fase F).

Thin adapter, same role as cli.py but over HTTP instead of argparse: it
never implements business logic itself, only translates requests into
calls to the same Core the CLI and Studio already use.

Scope note: no versioning or persistence between requests yet.
docs/masterplan/DOC-008-API.md lists those as still-pending decisions
("Pendiente de: definir los contratos públicos...", "En revisión"), not
as requirements for this first cut. Authentication and rate limiting
(IDE-0009) are covered below.

Auth: if BOARDCOMPOSER_API_KEY is set in the environment (or passed
explicitly as api_key), every route except /health requires it via the
X-API-Key header. Unset, no auth is enforced — same permissive behaviour
as before IDE-0009, so existing local/CI usage keeps working unchanged.
That single shared key is treated as an unmetered admin key: it bypasses
quota checks entirely, for internal/local use.

Billing (billing.py): if db_path (or BOARDCOMPOSER_DB_PATH) points at a
SQLite key registry, X-API-Key is additionally checked against per-customer
keys issued via billing.create_key(). Each of those keys is on a plan
(free/basico/pro) with a monthly request quota, enforced on the metered
endpoints (billing.METERED_ENDPOINTS: /solve, /assist/*). Free-plan keys
are hard-blocked with 402 once the quota is used up; paid plans stay
available past their quota and accrue overage for billing. /health,
/strategies and /plugins are metadata-only and never metered.

Rate limiting: Flask-Limiter with a fixed per-IP default (60/minute),
exempting /health. Uses the in-memory storage backend — fine for a
single-process deployment, but limits aren't shared across gunicorn
workers; see DOC-006-DeudaTecnica.md if that becomes a real constraint.
Pass redis_url (or set REDIS_URL) to back both the rate limiter and the
billing quota counter with Redis instead, which fixes that same
cross-worker gap.

The /assist/* routes expose boardcomposer.ai (IDE-0007) the same way:
no AI logic of its own, just request/response translation. create_app()
defaults to default_provider(), which resolves to AnthropicProvider when
ANTHROPIC_API_KEY is set in the environment and falls back to
MockAIProvider otherwise. ai_provider is an explicit create_app()
parameter so tests (and any deployment wanting a specific provider) can
supply one without changing this module.
"""

import json
import os

from flask import Flask, Response, g, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from boardcomposer import billing
from boardcomposer.ai import (
    AIProvider,
    ProjectFromTextError,
    SuggestStrategyError,
    default_provider,
    explain_solution,
    project_from_text,
    suggest_strategy,
)
from boardcomposer.domain import Board, Project, ProjectConstraints
from boardcomposer.plugin_visibility import plugin_summary
from boardcomposer.presenters import solutions_to_json
from boardcomposer.solver import GeometrySolver
from boardcomposer.solver.strategies import (
    OptimizationStrategy,
    available_strategies,
    strategy_by_name,
)

# GeometrySolver's runtime grows sharply past a few hundred boards (measured:
# 100 boards ~1s, 200 ~7s, 300+ effectively unbounded) even though the
# combinatorial generators (horizontal/vertical) already cap themselves at 6
# boards internally. 100 is comfortably fast and far beyond a realistic
# real-world cutting project.
MAX_BOARDS = 100

API_KEY_ENV_VAR = "BOARDCOMPOSER_API_KEY"
API_KEY_HEADER = "X-API-Key"
DEFAULT_RATE_LIMIT = "60 per minute"
DB_PATH_ENV_VAR = "BOARDCOMPOSER_DB_PATH"
REDIS_URL_ENV_VAR = "REDIS_URL"


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


def create_app(
    ai_provider: AIProvider | None = None,
    api_key: str | None = None,
    rate_limit: str | None = None,
    db_path: str | None = None,
    quota_store: billing.QuotaStore | None = None,
    redis_url: str | None = None,
) -> Flask:
    provider = ai_provider or default_provider()
    api_key = api_key if api_key is not None else os.environ.get(API_KEY_ENV_VAR)
    rate_limit = rate_limit or DEFAULT_RATE_LIMIT
    db_path = db_path if db_path is not None else os.environ.get(DB_PATH_ENV_VAR)
    redis_url = (
        redis_url if redis_url is not None else os.environ.get(REDIS_URL_ENV_VAR)
    )

    if db_path:
        billing.init_db(db_path)

    if quota_store is None:
        if redis_url:
            import redis as redis_lib

            quota_store = billing.RedisQuotaStore(redis_lib.from_url(redis_url))
        else:
            quota_store = billing.InMemoryQuotaStore()

    app = Flask(__name__)
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=[rate_limit],
        storage_uri=redis_url or "memory://",
    )

    @app.errorhandler(429)
    def _rate_limit_exceeded(_error):
        return jsonify(
            error="Demasiadas peticiones. Inténtalo de nuevo más tarde."
        ), 429

    @app.before_request
    def _authenticate_and_meter():
        if request.endpoint == "health":
            return None

        header_key = request.headers.get(API_KEY_HEADER)

        # Legacy shared admin key: unmetered, bypasses billing entirely.
        if api_key and header_key == api_key:
            g.billing_plan = None
            return None

        if db_path:
            if not header_key:
                return jsonify(error="Clave de API inválida o ausente."), 401
            record = billing.lookup_key(db_path, billing.hash_key(header_key))
            if record is None or not record["active"]:
                return jsonify(error="Clave de API inválida o ausente."), 401

            g.billing_plan = record["plan"]
            g.billing_key_hash = record["key_hash"]

            if request.endpoint in billing.METERED_ENDPOINTS:
                result = billing.check_quota(
                    quota_store, record["key_hash"], record["plan"]
                )
                if not result.allowed:
                    return jsonify(
                        error="Cuota mensual del plan agotada. "
                        "Actualiza tu plan para continuar.",
                        plan=result.plan,
                        used=result.used,
                        limit=result.limit,
                    ), 402
            return None

        if api_key:
            return jsonify(error="Clave de API inválida o ausente."), 401

        return None

    @app.get("/health")
    @limiter.exempt
    def health():
        return jsonify(status="ok")

    @app.get("/strategies")
    def strategies():
        return jsonify(strategies=list(available_strategies()))

    @app.get("/plugins")
    def plugins():
        return jsonify(plugin_summary())

    @app.post("/solve")
    def solve():
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            return jsonify(error="El cuerpo debe ser un objeto JSON."), 400

        boards_data = payload.get("boards")
        if not isinstance(boards_data, list) or not boards_data:
            return jsonify(error="'boards' debe ser una lista no vacía."), 400

        if len(boards_data) > MAX_BOARDS:
            return (
                jsonify(error=f"'boards' admite como máximo {MAX_BOARDS} tablas."),
                400,
            )

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

        if len(boards_data) > MAX_BOARDS:
            return (
                jsonify(error=f"'boards' admite como máximo {MAX_BOARDS} tablas."),
                400,
            )

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

        if len(boards_data) > MAX_BOARDS:
            return (
                jsonify(error=f"'boards' admite como máximo {MAX_BOARDS} tablas."),
                400,
            )

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
    create_app().run(port=5050)
