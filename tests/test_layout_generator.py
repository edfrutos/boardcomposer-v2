from boardcomposer import Board, Project
from boardcomposer.solver.layout_generator import (
    generate_horizontal_solution,
    generate_vertical_solution,
)


def test_generate_horizontal_solution():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_horizontal_solution(project)

    assert solution.explanation.notes == ["horizontal"]
    assert solution.total_length_mm == 3000
    assert solution.total_width_mm == 300


def test_generate_vertical_solution():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_vertical_solution(project)

    assert solution.explanation.notes == ["vertical"]
    assert solution.total_length_mm == 2000
    assert solution.total_width_mm == 600
