from boardcomposer import Board, Project, ProjectConstraints


def test_project_has_default_constraints():
    project = Project()

    assert project.constraints.max_length_mm is None
    assert project.constraints.max_width_mm is None


def test_project_accepts_custom_constraints():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=600,
        )
    )

    project.add_board(Board(length_mm=2000, width_mm=300, thickness_mm=20))

    assert project.constraints.max_length_mm == 3000
    assert project.total_area_mm2 == 600000
