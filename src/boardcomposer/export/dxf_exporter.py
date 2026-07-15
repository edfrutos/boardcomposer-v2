import io

import ezdxf

from boardcomposer.domain import AssemblySolution


def solution_to_dxf(solution: AssemblySolution) -> str:
    doc = ezdxf.new()
    modelspace = doc.modelspace()

    for placement in solution.placements:
        x, y = placement.x_mm, placement.y_mm
        length, width = placement.length_mm, placement.width_mm
        modelspace.add_lwpolyline(
            [(x, y), (x + length, y), (x + length, y + width), (x, y + width)],
            close=True,
        )
        modelspace.add_text(placement.board_id, height=16).set_placement(
            (x + 5, y + 20)
        )

    stream = io.StringIO()
    doc.write(stream)
    return stream.getvalue()
