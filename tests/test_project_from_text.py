import json

import pytest

from boardcomposer.ai import MockAIProvider, ProjectFromTextError, project_from_text


def _provider(response) -> MockAIProvider:
    if not isinstance(response, str):
        response = json.dumps(response)
    return MockAIProvider(response=response)


def test_project_from_text_builds_boards_and_constraints():
    provider = _provider(
        {
            "boards": [
                {"id": "A", "length_mm": 1200, "width_mm": 600, "thickness_mm": 18},
                {"id": "B", "length_mm": 800, "width_mm": 400, "thickness_mm": 18},
            ],
            "constraints": {
                "max_length_mm": 3000,
                "max_width_mm": 600,
                "allow_rotation": True,
                "allow_cutting": False,
            },
        }
    )

    project = project_from_text("dos tablas de 1200x600 y 800x400", provider)

    assert [board.id for board in project.boards] == ["A", "B"]
    assert project.boards[0].length_mm == 1200
    assert project.constraints.max_length_mm == 3000
    assert project.constraints.allow_rotation is True


def test_project_from_text_sends_the_input_text_in_the_prompt():
    provider = _provider({"boards": [{"length_mm": 100, "width_mm": 100}]})

    project_from_text("tres tablas de pino", provider)

    assert "tres tablas de pino" in provider.calls[0]


def test_project_from_text_defaults_missing_constraints():
    provider = _provider({"boards": [{"length_mm": 100, "width_mm": 100}]})

    project = project_from_text("una tabla", provider)

    assert project.constraints.max_length_mm is None
    assert project.constraints.allow_rotation is False


def test_project_from_text_defaults_missing_thickness():
    provider = _provider({"boards": [{"length_mm": 100, "width_mm": 100}]})

    project = project_from_text("una tabla", provider)

    assert project.boards[0].thickness_mm == 1


def test_project_from_text_rejects_invalid_json():
    provider = _provider("esto no es json")

    with pytest.raises(ProjectFromTextError):
        project_from_text("texto", provider)


def test_project_from_text_rejects_non_object_json():
    provider = _provider([1, 2, 3])

    with pytest.raises(ProjectFromTextError):
        project_from_text("texto", provider)


def test_project_from_text_rejects_missing_boards():
    provider = _provider({"constraints": {}})

    with pytest.raises(ProjectFromTextError):
        project_from_text("texto", provider)


def test_project_from_text_rejects_empty_boards():
    provider = _provider({"boards": []})

    with pytest.raises(ProjectFromTextError):
        project_from_text("texto", provider)


def test_project_from_text_rejects_invalid_board():
    provider = _provider({"boards": [{"length_mm": 100}]})

    with pytest.raises(ProjectFromTextError):
        project_from_text("texto", provider)


def test_project_from_text_rejects_non_object_constraints():
    provider = _provider(
        {"boards": [{"length_mm": 100, "width_mm": 100}], "constraints": [1]}
    )

    with pytest.raises(ProjectFromTextError):
        project_from_text("texto", provider)
