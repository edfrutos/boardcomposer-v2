from flask import Flask

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.maxrects_search import (
    generate_beam_maxrects_solution,
    generate_best_maxrects_solution,
)
from boardcomposer.solver.skyline_search import generate_best_skyline_solution

app = Flask(__name__)


def demo_project() -> Project:
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
            allow_rotation=True,
        )
    )

    for board in [
        Board(1800, 300, 19, "A"),
        Board(1200, 300, 19, "B"),
        Board(800, 200, 19, "C"),
        Board(700, 180, 19, "D"),
        Board(600, 250, 19, "E"),
        Board(500, 150, 19, "F"),
        Board(400, 120, 19, "G"),
    ]:
        project.add_board(board)

    return project


def render_svg(solution) -> str:
    width = max((p.x_mm + p.length_mm for p in solution.placements), default=1)
    height = max((p.y_mm + p.width_mm for p in solution.placements), default=1)

    rects = []
    for p in solution.placements:
        color = f"hsl({hash(p.board_id) % 360}, 70%, 76%)"
        rects.append(
            f'<rect x="{p.x_mm}" y="{p.y_mm}" width="{p.length_mm}" height="{p.width_mm}" '
            f'fill="{color}" stroke="#222" stroke-width="3"/>'
        )
        rects.append(
            f'<text x="{p.x_mm + 16}" y="{p.y_mm + 38}" '
            f'font-size="36" font-family="system-ui">{p.board_id}</text>'
        )

    return f"""
    <svg viewBox="0 0 {width} {height}" width="100%" style="background:#fafafa;border:1px solid #999">
        {"".join(rects)}
    </svg>
    """


def render_solution(title: str, solution) -> str:
    notes = " · ".join(solution.explanation.notes)
    return f"""
    <section class="solution">
        <h2>{title}</h2>
        <p><strong>{len(solution.placements)}</strong> piezas · {notes}</p>
        {render_svg(solution)}
    </section>
    """


@app.get("/")
def index():
    project = demo_project()

    solutions = [
        ("Skyline", generate_best_skyline_solution(project)),
        ("MaxRects clásico", generate_best_maxrects_solution(project)),
        (
            "MaxRects Beam width=4",
            generate_beam_maxrects_solution(project, beam_width=4),
        ),
    ]

    body = "\n".join(render_solution(title, solution) for title, solution in solutions)

    return f"""
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>BoardComposer Workbench</title>
        <style>
            body {{
                font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
                margin: 32px;
                background: #f3f4f6;
                color: #111827;
            }}
            h1 {{ margin-bottom: 8px; }}
            .solution {{
                background: white;
                border-radius: 16px;
                padding: 24px;
                margin: 24px 0;
                box-shadow: 0 1px 8px rgba(0,0,0,.08);
            }}
            svg {{
                max-height: 520px;
            }}
        </style>
    </head>
    <body>
        <h1>BoardComposer Workbench</h1>
        <p>Comparativa visual rápida: Skyline, MaxRects clásico y Beam Search.</p>
        {body}
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(debug=True, port=8000)
