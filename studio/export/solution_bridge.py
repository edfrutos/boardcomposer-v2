"""Bridge from the current Studio workspace state to a Core AssemblySolution.

Pure function, no Qt dependency. Lets the export modules (SVG, PDF) reuse
Core's domain types instead of Studio reimplementing bounding-box/area
geometry that already exists in boardcomposer.domain.
"""

from boardcomposer.domain import AssemblySolution, BoardPlacement

from studio.models import StudioProject


def studio_project_to_solution(project: StudioProject) -> AssemblySolution:
    pieces_by_id = {piece.piece_id: piece for piece in project.pieces}
    placements = []

    for placement in project.placements:
        piece = pieces_by_id.get(placement.piece_id)
        if piece is None:
            continue

        length_mm, width_mm = piece.length_mm, piece.width_mm
        if placement.rotated:
            length_mm, width_mm = width_mm, length_mm

        placements.append(
            BoardPlacement(
                board_id=placement.piece_id,
                x_mm=placement.x_mm,
                y_mm=placement.y_mm,
                length_mm=length_mm,
                width_mm=width_mm,
                rotated=placement.rotated,
            )
        )

    return AssemblySolution(placements=placements)
