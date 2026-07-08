from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.generators import generators_by_name


def _placed(generator_name: str) -> int:
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=2400,
            max_width_mm=600,
        )
    )

    boards = [
        Board(1200, 300, 19, "A"),
        Board(1200, 300, 19, "B"),
        Board(800, 300, 19, "C"),
        Board(800, 300, 19, "D"),
        Board(600, 300, 19, "E"),
        Board(600, 300, 19, "F"),
    ]

    for board in boards:
        project.add_board(board)

    generator = generators_by_name([generator_name])[0]
    solution = generator(project)[0]

    return len(solution.placements)


def test_maxrects_places_at_least_as_many_boards_as_skyline():
    skyline = _placed("skyline")
    maxrects = _placed("maxrects")

    assert maxrects >= skyline
