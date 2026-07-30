"""Content builders for the Inspector panel (SCR-004 — Inspector Contextual).

Pure functions, no Qt dependency, so they can be unit-tested directly.
Each renders the same visual structure (título, propiedades, métricas)
for a different selection context, showing only fields backed by real
data — no placeholder values for fields the domain doesn't model yet
(e.g. board thickness, project description, modification timestamps).
"""

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.panels.board_metrics import board_utilization


def render_empty() -> str:
    return (
        '<table id="empty-state-table"><tr><td id="empty-state">'
        "<h3>Inspector</h3>"
        "<p>Sin selección. Elige un tablero o una pieza en el Explorer.</p>"
        "</td></tr></table>"
    )


def render_project(project: StudioProject) -> str:
    materials = sorted(
        {board.material for board in project.boards}
        | {piece.material for piece in project.pieces}
    )

    return (
        f"<h3>Proyecto: {project.name}</h3>"
        f"<p><b>Materiales:</b> {', '.join(materials) if materials else '—'}</p>"
        f"<p><b>Tableros:</b> {len(project.boards)}</p>"
        f"<p><b>Piezas:</b> {len(project.pieces)}</p>"
    )


def render_board(
    board: StudioBoard,
    placements: list[StudioPlacement],
    pieces_by_id: dict[str, StudioPiece],
) -> str:
    utilization = board_utilization(board, placements, pieces_by_id)

    return (
        f"<h3>Tablero: {board.board_id}</h3>"
        f"<p><b>Dimensiones:</b> {board.length_mm:g} x {board.width_mm:g} mm</p>"
        f"<p><b>Material:</b> {board.material}</p>"
        f"<p><b>Piezas colocadas:</b> {len(placements)}</p>"
        f"<p><b>Superficie utilizada:</b> {utilization:.1%}</p>"
        f"<p><b>Desperdicio:</b> {1 - utilization:.1%}</p>"
    )


def render_piece(piece: StudioPiece, placement: StudioPlacement | None) -> str:
    lines = [
        f"<h3>Pieza: {piece.piece_id}</h3>",
        f"<p><b>Dimensiones:</b> {piece.length_mm:g} x {piece.width_mm:g} mm</p>",
        f"<p><b>Material:</b> {piece.material}</p>",
    ]

    if placement is not None:
        lines.append(f"<p><b>Rotación:</b> {placement.rotation}°</p>")
        lines.append(
            f"<p><b>Coordenadas:</b> {placement.x_mm:g}, {placement.y_mm:g} mm</p>"
        )
    else:
        lines.append("<p><i>Sin colocar en el workspace.</i></p>")

    return "".join(lines)
