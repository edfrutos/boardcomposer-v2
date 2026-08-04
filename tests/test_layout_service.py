from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.services import StudioServices
from studio.workspace.placement_fit import piece_fits_on_board


def _project_with_pieces() -> StudioProject:
    return StudioProject(
        project_id="proj-1",
        name="Demo",
        boards=[StudioBoard("A", 2000, 300)],
        pieces=[
            StudioPiece("p1", 700, 300),
            StudioPiece("p2", 520, 300),
        ],
    )


def _project_with_two_boards() -> StudioProject:
    return StudioProject(
        project_id="proj-2",
        name="Demo",
        boards=[
            StudioBoard("A", 2000, 300),
            StudioBoard("B", 1000, 300),
        ],
        pieces=[
            StudioPiece("p1", 700, 300),
            StudioPiece("p2", 520, 300),
        ],
    )


def test_compare_solutions_returns_empty_list_without_a_project():
    services = StudioServices()

    assert services.layout.compare_solutions() == []


def test_compare_solutions_returns_up_to_four_ranked_solutions():
    services = StudioServices()
    services.projects.new_project(_project_with_pieces())

    solutions = services.layout.compare_solutions()

    assert 1 <= len(solutions) <= 4
    scores = [solution.score.total for solution in solutions]
    assert scores == sorted(scores, reverse=True)


def test_apply_comparison_solution_applies_the_chosen_index():
    services = StudioServices()
    services.projects.new_project(_project_with_pieces())
    services.layout.compare_solutions()

    assert services.layout.apply_comparison_solution(0) is True
    assert len(services.projects.current_project.placements) > 0


def test_apply_comparison_solution_rejects_out_of_range_index():
    services = StudioServices()
    services.projects.new_project(_project_with_pieces())
    services.layout.compare_solutions()

    assert services.layout.apply_comparison_solution(99) is False


def test_to_core_project_uses_active_board_dimensions():
    services = StudioServices()
    services.projects.new_project(_project_with_two_boards())

    core_project = services.layout.to_core_project("B")

    assert core_project.constraints.max_length_mm == 1000


def test_to_core_project_falls_back_to_first_board_without_active_board():
    services = StudioServices()
    services.projects.new_project(_project_with_two_boards())

    core_project = services.layout.to_core_project()

    assert core_project.constraints.max_length_mm == 2000


def test_to_core_project_uses_each_pieces_own_thickness():
    services = StudioServices()
    project = StudioProject(
        project_id="proj-3",
        name="Demo",
        # Board thickness matches the piece — this test is only about the
        # value passing through, not about the thickness-matching filter
        # (covered separately below).
        boards=[StudioBoard("A", 2000, 300, thickness_mm=25.0)],
        pieces=[StudioPiece("p1", 700, 300, thickness_mm=25.0)],
    )
    services.projects.new_project(project)

    core_project = services.layout.to_core_project()

    assert core_project.boards[0].thickness_mm == 25.0


def test_to_core_project_excludes_pieces_with_a_different_thickness():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-6",
            name="Demo",
            boards=[StudioBoard("A", 2000, 300, thickness_mm=19.0)],
            pieces=[
                StudioPiece("p1", 500, 300, thickness_mm=19.0),
                StudioPiece("p2", 500, 300, thickness_mm=25.0),
            ],
        )
    )

    core_project = services.layout.to_core_project("A")

    assert {board.id for board in core_project.boards} == {"p1"}


def test_apply_last_solution_sends_leftover_to_the_matching_thickness_board():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-7",
            name="Demo",
            boards=[
                StudioBoard("A", 2000, 300, thickness_mm=19.0),
                StudioBoard("B", 2000, 300, thickness_mm=25.0),
            ],
            pieces=[
                StudioPiece("p1", 500, 300, thickness_mm=19.0),
                StudioPiece("p2", 500, 300, thickness_mm=25.0),
            ],
        )
    )

    services.layout.solve_current_project("A")
    assert services.layout.apply_last_solution_to_current_project("A") is True

    project = services.projects.current_project
    assert project.placement_by_piece_id("p1").board_id == "A"
    assert project.placement_by_piece_id("p2").board_id == "B"


def test_apply_last_solution_leaves_piece_unplaced_without_a_matching_thickness_board():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-8",
            name="Demo",
            boards=[
                StudioBoard("A", 2000, 300, thickness_mm=19.0),
                StudioBoard("B", 2000, 300, thickness_mm=19.0),
            ],
            pieces=[
                StudioPiece("p1", 500, 300, thickness_mm=19.0),
                StudioPiece("p2", 500, 300, thickness_mm=25.0),  # no 25mm board
            ],
        )
    )

    services.layout.solve_current_project("A")
    services.layout.apply_last_solution_to_current_project("A")

    project = services.projects.current_project
    assert project.placement_by_piece_id("p1").board_id == "A"
    assert project.placement_by_piece_id("p2") is None


def test_apply_last_solution_assigns_placements_to_active_board():
    services = StudioServices()
    services.projects.new_project(_project_with_two_boards())
    services.layout.solve_current_project("B")

    assert services.layout.apply_last_solution_to_current_project("B") is True

    placements = services.projects.current_project.placements
    assert placements
    # Not "all on B": a piece p1+p2 don't both fit B's 1000mm, so whichever
    # is left over now gets auto-placed on the project's other empty board
    # (A) instead of staying unplaced — proving "B" was honored just needs
    # at least one placement to land there.
    assert any(placement.board_id == "B" for placement in placements)


def test_apply_last_solution_fills_other_empty_boards_with_leftovers():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-4",
            name="Demo",
            boards=[
                StudioBoard("A", 2000, 300),
                StudioBoard("B", 600, 300),
            ],
            pieces=[
                StudioPiece("p1", 500, 300),  # fits on B
                StudioPiece("p2", 700, 300),  # too long for B, fits only A
            ],
        )
    )

    services.layout.solve_current_project("B")
    assert services.layout.apply_last_solution_to_current_project("B") is True

    project = services.projects.current_project
    assert project.placement_by_piece_id("p1").board_id == "B"
    assert project.placement_by_piece_id("p2").board_id == "A"


def test_apply_last_solution_does_not_touch_a_board_that_already_has_pieces():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-5",
            name="Demo",
            boards=[
                StudioBoard("A", 2000, 300),
                StudioBoard("B", 600, 300),
            ],
            pieces=[
                StudioPiece("p1", 500, 300),
                StudioPiece("p2", 700, 300),
            ],
        )
    )
    project = services.projects.current_project
    # A already has something on it — it must stay exactly as-is even though
    # p2 would otherwise fit there once p1 fills up B.
    project.placements.append(StudioPlacement("existing", 0, 0, board_id="A"))

    services.layout.solve_current_project("B")
    services.layout.apply_last_solution_to_current_project("B")

    assert project.placement_by_piece_id("existing").board_id == "A"
    assert project.placement_by_piece_id("p2") is None


def test_apply_solution_keeps_placements_on_other_boards():
    services = StudioServices()
    services.projects.new_project(_project_with_two_boards())
    project = services.projects.current_project

    # A piece placed by hand on board A, before solving anything.
    project.placements.append(StudioPlacement("p1", 0, 0, board_id="A"))

    services.layout.solve_current_project("B")
    assert services.layout.apply_last_solution_to_current_project("B") is True

    # Applying a layout to B must leave A's placement untouched — it used to
    # clear the whole list and silently empty every other board.
    assert any(placement.board_id == "A" for placement in project.placements)
    assert any(placement.board_id == "B" for placement in project.placements)


def _project_with_a_board_filled_to_the_millimetre() -> StudioProject:
    # 700 + 520 is exactly the board's 1220mm of length: the two pieces fit
    # side by side with nothing to spare, and stacking them is impossible
    # (300 + 300 > the board's 400mm of width).
    return StudioProject(
        project_id="proj-kerf",
        name="Demo",
        boards=[StudioBoard("A", 1220, 400)],
        pieces=[
            StudioPiece("p1", 700, 300),
            StudioPiece("p2", 520, 300),
        ],
    )


def test_to_core_project_hands_the_solver_pieces_widened_by_the_kerf():
    services = StudioServices()
    project = _project_with_pieces()
    project.kerf_mm = 3
    services.projects.new_project(project)

    core_project = services.layout.to_core_project()

    by_id = {board.id: board for board in core_project.boards}
    assert (by_id["p1"].length_mm, by_id["p1"].width_mm) == (703, 303)
    assert (by_id["p2"].length_mm, by_id["p2"].width_mm) == (523, 303)


def test_to_core_project_leaves_pieces_untouched_without_a_kerf():
    services = StudioServices()
    services.projects.new_project(_project_with_pieces())

    core_project = services.layout.to_core_project()

    by_id = {board.id: board for board in core_project.boards}
    assert (by_id["p1"].length_mm, by_id["p1"].width_mm) == (700, 300)


def test_to_core_project_grows_the_board_by_one_kerf_to_offset_the_pieces():
    services = StudioServices()
    project = _project_with_pieces()
    project.kerf_mm = 3
    services.projects.new_project(project)

    core_project = services.layout.to_core_project()

    assert core_project.constraints.max_length_mm == 2003
    assert core_project.constraints.max_width_mm == 303


def test_a_piece_as_wide_as_the_board_still_fits_with_a_kerf_set():
    # The commonest case in real work: pieces the full width of the board,
    # cut across it. There is no cut to make along the board's own edge, so
    # widening every piece without widening the board would have refused to
    # place a single one of them.
    services = StudioServices()
    project = _project_with_pieces()
    project.kerf_mm = 3
    services.projects.new_project(project)

    services.layout.solve_current_project("A")
    services.layout.apply_last_solution_to_current_project("A")

    assert len(services.projects.current_project.placements) == 2


def test_a_kerf_costs_a_piece_on_a_board_that_was_full_to_the_millimetre():
    services = StudioServices()
    services.projects.new_project(_project_with_a_board_filled_to_the_millimetre())

    services.layout.solve_current_project("A")
    services.layout.apply_last_solution_to_current_project("A")
    assert len(services.projects.current_project.placements) == 2

    services = StudioServices()
    project = _project_with_a_board_filled_to_the_millimetre()
    project.kerf_mm = 3
    services.projects.new_project(project)

    services.layout.solve_current_project("A")
    services.layout.apply_last_solution_to_current_project("A")

    # 703 + 523 no longer clears 1220. Losing the piece is the correct
    # answer: the layout that placed both could not be cut.
    assert len(services.projects.current_project.placements) == 1


def test_best_fit_distribution_returns_empty_result_without_a_project():
    services = StudioServices()

    result = services.layout.apply_best_fit_distribution()

    assert result.boards_used == []
    assert result.pieces_placed == 0
    assert result.pieces_unplaced == []


def test_best_fit_distribution_prefers_the_smallest_sufficient_board():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-best-fit-1",
            name="Demo",
            # Large board listed FIRST — proves the choice is by area, not
            # by list order (that's the old _fill_other_empty_boards_with_
            # leftovers() behavior this replaces).
            boards=[
                StudioBoard("grande", 2000, 2000),
                StudioBoard("retal", 600, 300),
            ],
            pieces=[StudioPiece("p1", 500, 300)],
        )
    )

    result = services.layout.apply_best_fit_distribution()

    assert result.boards_used == ["retal"]
    project = services.projects.current_project
    assert project.placement_by_piece_id("p1").board_id == "retal"


def test_best_fit_distribution_uses_a_partially_occupied_board():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-best-fit-2",
            name="Demo",
            boards=[StudioBoard("A", 1000, 300)],
            pieces=[
                StudioPiece("existing", 400, 300),
                StudioPiece("nueva", 400, 300),
            ],
        )
    )
    project = services.projects.current_project
    # "A" already has a piece on it — the old leftover-fill skipped any
    # board that wasn't completely empty. Best-fit must still consider it.
    project.placements.append(StudioPlacement("existing", 0, 0, board_id="A"))

    result = services.layout.apply_best_fit_distribution()

    assert "A" in result.boards_used
    assert project.placement_by_piece_id("nueva") is not None
    assert project.placement_by_piece_id("nueva").board_id == "A"
    # The pre-existing placement survives (possibly repacked, not lost).
    assert project.placement_by_piece_id("existing") is not None


def test_best_fit_distribution_falls_through_to_a_larger_board_when_needed():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-best-fit-3",
            name="Demo",
            boards=[
                StudioBoard("retal", 600, 300),
                StudioBoard("grande", 2000, 300),
            ],
            pieces=[
                StudioPiece("p1", 500, 300),  # fits only on the small board
                StudioPiece("p2", 700, 300),  # too long for the small board
            ],
        )
    )

    result = services.layout.apply_best_fit_distribution()

    project = services.projects.current_project
    assert project.placement_by_piece_id("p1").board_id == "retal"
    assert project.placement_by_piece_id("p2").board_id == "grande"
    assert set(result.boards_used) == {"retal", "grande"}
    assert result.pieces_placed == 2
    assert result.pieces_unplaced == []


def test_best_fit_distribution_leaves_pieces_unplaced_without_a_matching_board():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="proj-best-fit-4",
            name="Demo",
            boards=[StudioBoard("A", 2000, 300, thickness_mm=19.0)],
            pieces=[StudioPiece("p1", 500, 300, thickness_mm=25.0)],
        )
    )

    result = services.layout.apply_best_fit_distribution()

    assert result.boards_used == []
    assert result.pieces_unplaced == ["p1"]


def test_applied_placements_leave_the_cut_between_pieces():
    services = StudioServices()
    project = _project_with_pieces()
    project.kerf_mm = 3
    services.projects.new_project(project)

    services.layout.solve_current_project("A")
    services.layout.apply_last_solution_to_current_project("A")

    placements = services.projects.current_project.placements
    assert len(placements) == 2

    pieces_by_id = {p.piece_id: p for p in services.projects.current_project.pieces}
    for placement in placements:
        others = [other for other in placements if other is not placement]
        assert piece_fits_on_board(
            services.projects.current_project.boards[0],
            pieces_by_id[placement.piece_id],
            placement.x_mm,
            placement.y_mm,
            placement.rotated,
            others,
            pieces_by_id,
            kerf_mm=3,
        )
