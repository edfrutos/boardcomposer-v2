"""JSON persistence for BoardComposer Studio projects."""

import json
from pathlib import Path

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject


def project_to_dict(project: StudioProject) -> dict:
    return {
        "project_id": project.project_id,
        "name": project.name,
        "boards": [
            {
                "board_id": board.board_id,
                "length_mm": board.length_mm,
                "width_mm": board.width_mm,
                "material": board.material,
                "thickness_mm": board.thickness_mm,
            }
            for board in project.boards
        ],
        "pieces": [
            {
                "piece_id": piece.piece_id,
                "length_mm": piece.length_mm,
                "width_mm": piece.width_mm,
                "material": piece.material,
                "thickness_mm": piece.thickness_mm,
            }
            for piece in project.pieces
        ],
        "placements": [
            {
                "piece_id": placement.piece_id,
                "x_mm": placement.x_mm,
                "y_mm": placement.y_mm,
                "board_id": placement.board_id,
                "rotated": placement.rotated,
                "rotation": placement.rotation,
            }
            for placement in project.placements
        ],
        "kerf_mm": project.kerf_mm,
    }


def project_from_dict(data: dict) -> StudioProject:
    boards = [StudioBoard(**board) for board in data.get("boards", [])]
    default_board_id = boards[0].board_id if boards else None

    placements = []
    for placement in data.get("placements", []):
        placement.setdefault("board_id", default_board_id)
        placements.append(StudioPlacement(**placement))

    return StudioProject(
        project_id=data["project_id"],
        name=data["name"],
        boards=boards,
        pieces=[StudioPiece(**piece) for piece in data.get("pieces", [])],
        placements=placements,
        kerf_mm=data.get("kerf_mm", 0.0),
    )


def save_project_to_file(project: StudioProject, path: str | Path) -> None:
    Path(path).write_text(
        json.dumps(project_to_dict(project), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_project_from_file(path: str | Path) -> StudioProject:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return project_from_dict(data)
