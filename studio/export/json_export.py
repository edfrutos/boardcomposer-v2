"""JSON export for the current Studio workspace state (IDE-0022).

Purpose-built for a single, already-placed layout — unlike
`boardcomposer.presenters.solutions_to_json()`, which describes several
candidate solutions ranked by an `OptimizationStrategy` (CLI/API `/solve`
output). Studio's current layout has no strategy behind it once the user
starts moving pieces by hand, so that shape doesn't fit here.
"""

import json
from pathlib import Path

from studio.export.solution_bridge import studio_project_to_solution
from studio.models import StudioProject


def export_project_to_json(project: StudioProject, path: str | Path) -> bool:
    solution = studio_project_to_solution(project)
    if not solution.placements:
        return False

    data = {
        "project_name": project.name,
        "placed_pieces": len(solution.placements),
        "total_length_mm": solution.total_length_mm,
        "total_width_mm": solution.total_width_mm,
        "placements": [
            {
                "piece_id": placement.board_id,
                "x_mm": placement.x_mm,
                "y_mm": placement.y_mm,
                "length_mm": placement.length_mm,
                "width_mm": placement.width_mm,
                "rotated": placement.rotated,
            }
            for placement in solution.placements
        ],
    }

    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")
    return True
