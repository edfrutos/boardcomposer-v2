from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.panels.inspector_panel import (
    render_board,
    render_empty,
    render_piece,
    render_project,
)


def test_render_empty_shows_no_selection():
    assert "Sin selección" in render_empty()


def test_render_project_lists_counts_and_materials():
    project = StudioProject(
        project_id="proj-1",
        name="Cocina",
        boards=[StudioBoard("A", 2000, 300, material="MDF")],
        pieces=[
            StudioPiece("p1", 500, 200, material="MDF"),
            StudioPiece("p2", 300, 200, material="Roble"),
        ],
    )

    html = render_project(project)

    assert "Cocina" in html
    assert "Tableros:</b> 1" in html
    assert "Piezas:</b> 2" in html
    assert "MDF" in html and "Roble" in html


def test_render_board_computes_utilization_and_waste():
    board = StudioBoard("A", 1000, 1000, material="MDF")
    pieces_by_id = {"p1": StudioPiece("p1", 500, 500, material="MDF")}
    placements = [StudioPlacement("p1", 0, 0)]

    html = render_board(board, placements, pieces_by_id)

    assert "Piezas colocadas:</b> 1" in html
    assert "Superficie utilizada:</b> 25.0%" in html
    assert "Desperdicio:</b> 75.0%" in html


def test_render_board_with_no_placements_has_zero_utilization():
    board = StudioBoard("A", 1000, 1000)

    html = render_board(board, [], {})

    assert "Superficie utilizada:</b> 0.0%" in html


def test_render_piece_with_placement_shows_rotation_and_coordinates():
    piece = StudioPiece("p1", 500, 200, material="MDF")
    placement = StudioPlacement("p1", 10, 20, rotated=True, rotation=90)

    html = render_piece(piece, placement)

    assert "Rotación:</b> 90°" in html
    assert "Coordenadas:</b> 10, 20 mm" in html


def test_render_piece_without_placement_notes_it_is_unplaced():
    piece = StudioPiece("p1", 500, 200)

    html = render_piece(piece, None)

    assert "Sin colocar" in html
