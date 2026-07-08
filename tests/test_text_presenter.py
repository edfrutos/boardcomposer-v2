from boardcomposer import Board, Project
from boardcomposer.presenters import solution_to_text
from boardcomposer.solver import GeometrySolver


def test_solution_to_text_contains_summary():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    solutions = GeometrySolver(project).solve()
    output = solution_to_text(project, solutions)

    assert "BoardComposer" in output
    assert "Tablas entrada: 1" in output
    assert "Puntuación:" in output
