from boardcomposer.domain import AssemblySolution, Project, SolutionExplanation
from boardcomposer.layout.free_space_manager import FreeSpaceManager
from boardcomposer.layout.placer import place_board_in_first_space


def generate_free_space_solution(project: Project) -> AssemblySolution:
    max_length = project.constraints.max_length_mm or sum(
        board.length_mm for board in project.boards
    )
    max_width = project.constraints.max_width_mm or max(
        (board.width_mm for board in project.boards), default=0
    )

    manager = FreeSpaceManager.from_bounds(max_length, max_width)
    placements = []

    for index, board in enumerate(project.boards):
        placement = place_board_in_first_space(
            board=board,
            manager=manager,
            board_id=board.id or f"board-{index + 1}",
        )

        if placement is not None:
            placements.append(placement)

    return AssemblySolution(
        placements=placements,
        explanation=SolutionExplanation(notes=["free_space"]),
    )
