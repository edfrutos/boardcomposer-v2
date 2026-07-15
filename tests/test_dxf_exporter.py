import io

import ezdxf

from boardcomposer import AssemblySolution, BoardPlacement
from boardcomposer.export import solution_to_dxf


def test_solution_to_dxf_is_valid_dxf():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    dxf = solution_to_dxf(solution)

    assert "SECTION" in dxf
    assert "ENDSEC" in dxf
    doc = ezdxf.read(io.StringIO(dxf))
    modelspace = doc.modelspace()
    assert len(list(modelspace.query("LWPOLYLINE"))) == 1
    assert len(list(modelspace.query("TEXT"))) == 1


def test_solution_to_dxf_draws_one_polyline_per_placement():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 80, 40),
        ]
    )

    dxf = solution_to_dxf(solution)

    doc = ezdxf.read(io.StringIO(dxf))
    modelspace = doc.modelspace()
    assert len(list(modelspace.query("LWPOLYLINE"))) == 2
    texts = {entity.dxf.text for entity in modelspace.query("TEXT")}
    assert texts == {"A", "B"}


def test_solution_to_dxf_with_no_placements():
    solution = AssemblySolution(placements=[])

    dxf = solution_to_dxf(solution)

    doc = ezdxf.read(io.StringIO(dxf))
    modelspace = doc.modelspace()
    assert len(list(modelspace.query("LWPOLYLINE"))) == 0
