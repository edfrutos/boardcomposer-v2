from boardcomposer import Board, Project, ProjectConstraints

from boardcomposer.solver.generators import generators_by_name


def _run(generator_name: str, boards):

    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=2440,
            max_width_mm=610,
            allow_rotation=True,
        )
    )

    for board in boards:
        project.add_board(board)

    generator = generators_by_name([generator_name])[0]

    return generator(project)[0]


def test_benchmark_long_strips():

    boards = [
        Board(1800, 120, 19, "A"),
        Board(1600, 120, 19, "B"),
        Board(1400, 120, 19, "C"),
        Board(1000, 120, 19, "D"),
        Board(800, 120, 19, "E"),
    ]

    skyline = _run("skyline", boards)

    maxrects = _run("maxrects", boards)

    assert len(maxrects.placements) > 0
    assert len(skyline.placements) > 0


def test_benchmark_mixed_sizes():

    boards = [
        Board(1800, 300, 19, "A"),
        Board(1200, 300, 19, "B"),
        Board(800, 200, 19, "C"),
        Board(700, 180, 19, "D"),
        Board(600, 250, 19, "E"),
        Board(500, 150, 19, "F"),
        Board(400, 120, 19, "G"),
    ]

    skyline = _run("skyline", boards)

    maxrects = _run("maxrects", boards)

    assert len(maxrects.placements) > 0
    assert len(skyline.placements) > 0
