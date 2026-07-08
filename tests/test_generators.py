from boardcomposer import Board, Project
from boardcomposer.solver.generators import generators_by_name


def test_generators_by_name():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    generators = generators_by_name(["horizontal", "vertical", "free_space"])
    solutions = []

    for generator in generators:
        solutions.extend(generator(project))

    layouts = {tuple(solution.explanation.notes) for solution in solutions}

    assert ("horizontal_permutation",) in layouts
    assert ("vertical_permutation",) in layouts
    assert ("free_space",) in layouts


def test_skyline_generator_is_registered():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    generator = generators_by_name(["skyline"])[0]
    solutions = generator(project)

    assert len(solutions) == 1
    assert "skyline" in solutions[0].explanation.notes


def test_maxrects_generator_is_registered():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    generator = generators_by_name(["maxrects"])[0]
    solutions = generator(project)

    assert len(solutions) == 1
    assert "maxrects" in solutions[0].explanation.notes
