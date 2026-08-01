import sys

import pytest
from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.export.thumbnail import render_solution_thumbnail


@pytest.fixture(scope="session", autouse=True)
def qapp():
    return QApplication.instance() or QApplication(sys.argv)


def test_render_solution_thumbnail_returns_a_png_data_uri():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 500, 300)])

    uri = render_solution_thumbnail(solution)

    assert uri.startswith("data:image/png;base64,")
    assert len(uri) > len("data:image/png;base64,")


def test_render_solution_thumbnail_returns_empty_string_without_placements():
    solution = AssemblySolution(placements=[])

    assert render_solution_thumbnail(solution) == ""


def test_render_solution_thumbnail_handles_multiple_placements():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 500, 300),
            BoardPlacement("B", 500, 0, 200, 300),
        ]
    )

    uri = render_solution_thumbnail(solution)

    assert uri.startswith("data:image/png;base64,")
