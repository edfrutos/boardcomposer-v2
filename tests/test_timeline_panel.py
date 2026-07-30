from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.panels.timeline_panel import render_activity, render_overview


def test_render_overview_with_no_project_explains_there_is_nothing_yet():
    html = render_overview(None)

    assert "Sin proyecto abierto" in html


def test_render_overview_with_no_boards_explains_there_is_nothing_yet():
    html = render_overview(StudioProject(project_id="p1", name="Demo"))

    assert "sin tableros" in html


def test_render_overview_lists_every_board_with_its_pieces():
    project = StudioProject(
        project_id="p1",
        name="Demo",
        boards=[StudioBoard("A", 1000, 500), StudioBoard("B", 800, 400)],
        pieces=[StudioPiece("p1", 300, 200), StudioPiece("p2", 200, 150)],
        placements=[
            StudioPlacement("p1", 0, 0, board_id="A"),
            StudioPlacement("p2", 0, 0, board_id="B"),
        ],
    )

    html = render_overview(project)

    assert "A" in html
    assert "B" in html
    assert "p1" in html
    assert "p2" in html
    assert "1000 x 500 mm" in html


def test_render_overview_shows_an_empty_board_as_empty():
    project = StudioProject(
        project_id="p1", name="Demo", boards=[StudioBoard("A", 1000, 500)]
    )

    html = render_overview(project)

    assert "A" in html


def test_render_overview_notes_unplaced_pieces():
    project = StudioProject(
        project_id="p1",
        name="Demo",
        boards=[StudioBoard("A", 1000, 500)],
        pieces=[StudioPiece("p1", 300, 200), StudioPiece("p2", 900, 900)],
        placements=[StudioPlacement("p1", 0, 0, board_id="A")],
    )

    html = render_overview(project)

    assert "sin colocar" in html
    assert "p2" in html


def test_render_activity_with_no_entries_explains_how_it_fills_up():
    html = render_activity([])

    assert "Sin actividad todavía" in html


def test_render_activity_lists_entries():
    html = render_activity(["12:00:00 — Tablero añadido: B1", "12:00:05 — Pieza X"])

    assert "Tablero añadido: B1" in html
    assert "Pieza X" in html
