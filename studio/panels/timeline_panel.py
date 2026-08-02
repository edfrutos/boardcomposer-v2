"""Content builders for the Timeline dock's two tabs — Resumen and
Actividad (studio/events/event_bus.py, ADR-003).

Pure functions, no Qt dependency, same pattern as the other panels: tested
by asserting substrings, painted via studio.theme.panel_html_stylesheet().
"""

from studio.activity_log import ActivityEntry
from studio.models import StudioProject
from studio.panels.board_metrics import board_utilization


def render_overview(project: StudioProject | None) -> str:
    if project is None or not project.boards:
        return (
            '<table id="empty-state-table"><tr><td id="empty-state">'
            "<h3>Resumen</h3>"
            "<p>Sin proyecto abierto o sin tableros todavía.</p>"
            "</td></tr></table>"
        )

    pieces_by_id = {piece.piece_id: piece for piece in project.pieces}
    rows = []

    for board in project.boards:
        placements = [
            placement
            for placement in project.placements
            if placement.board_id == board.board_id
        ]
        utilization = board_utilization(board, placements, pieces_by_id)

        piece_list = ", ".join(p.piece_id for p in placements) or "—"

        rows.append(
            "<tr>"
            f"<td>{board.board_id}</td>"
            f"<td>{board.length_mm:g} x {board.width_mm:g} mm</td>"
            f"<td>{board.material}</td>"
            f"<td>{len(placements)}</td>"
            f"<td>{utilization:.0%}</td>"
            f"<td>{piece_list}</td>"
            "</tr>"
        )

    unplaced = [
        piece.piece_id
        for piece in project.pieces
        if project.placement_by_piece_id(piece.piece_id) is None
    ]
    unplaced_note = (
        f"<p><i>Piezas sin colocar: {', '.join(unplaced)}</i></p>" if unplaced else ""
    )

    return (
        f"<h3>Resumen — {project.name}</h3>"
        "<table>"
        "<tr><th>Tablero</th><th>Dimensiones</th><th>Material</th>"
        "<th>Piezas</th><th>Uso</th><th>Contenido</th></tr>"
        f"{''.join(rows)}"
        "</table>"
        f"{unplaced_note}"
    )


def render_activity(entries: list[ActivityEntry], category: str | None = None) -> str:
    if category is not None:
        entries = [entry for entry in entries if entry.category == category]

    if not entries:
        return (
            '<table id="empty-state-table"><tr><td id="empty-state">'
            "<h3>Actividad</h3>"
            "<p>Sin actividad todavía. Aquí aparecerán las acciones "
            "según las vayas haciendo — añadir o editar piezas y "
            "tableros, calcular o aplicar una disposición, guardar…</p>"
            "</td></tr></table>"
        )

    rows = "".join(
        f"<tr><td>{entry.timestamp} — <i>{entry.category}</i> — {entry.message}</td></tr>"
        for entry in entries
    )
    return f"<h3>Actividad</h3><table>{rows}</table>"
