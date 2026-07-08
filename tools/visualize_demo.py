from pathlib import Path

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.maxrects_search import (
    generate_beam_maxrects_solution,
    generate_best_maxrects_solution,
)
from boardcomposer.solver.skyline_search import generate_best_skyline_solution


def svg(solution, title):
    w = max((p.x_mm + p.length_mm for p in solution.placements), default=1)
    h = max((p.y_mm + p.width_mm for p in solution.placements), default=1)

    parts = [
        f"<h2>{title}</h2>",
        f"<p>{len(solution.placements)} piezas · {', '.join(solution.explanation.notes)}</p>",
        f'<svg viewBox="0 0 {w} {h}" width="100%" style="border:1px solid #999;background:#fafafa;max-height:520px">',
    ]

    for p in solution.placements:
        parts.append(
            f'<rect x="{p.x_mm}" y="{p.y_mm}" width="{p.length_mm}" height="{p.width_mm}" '
            f'fill="hsl({hash(p.board_id) % 360},70%,75%)" stroke="#333" stroke-width="3"/>'
        )
        parts.append(
            f'<text x="{p.x_mm + 16}" y="{p.y_mm + 38}" font-size="36" font-family="system-ui">{p.board_id}</text>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


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

solutions = [
    ("Skyline", generate_best_skyline_solution(project)),
    ("MaxRects clásico", generate_best_maxrects_solution(project)),
    ("MaxRects Beam width=4", generate_beam_maxrects_solution(project, beam_width=4)),
]

html = (
    "<html><body style='font-family:system-ui;padding:24px;background:#f3f4f6'>"
    + "\n<hr>\n".join(svg(solution, title) for title, solution in solutions)
    + "</body></html>"
)

Path("out").mkdir(exist_ok=True)
Path("out/demo.html").write_text(html, encoding="utf-8")
print("Creado: out/demo.html")
