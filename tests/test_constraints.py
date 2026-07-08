import pytest

from boardcomposer import ProjectConstraints


def test_constraints_accept_empty_values():
    constraints = ProjectConstraints()

    assert constraints.max_length_mm is None
    assert constraints.max_width_mm is None
    assert constraints.allow_rotation is False
    assert constraints.allow_cutting is False


def test_constraints_reject_invalid_max_length():
    with pytest.raises(ValueError):
        ProjectConstraints(max_length_mm=0)


def test_constraints_reject_invalid_max_width():
    with pytest.raises(ValueError):
        ProjectConstraints(max_width_mm=-1)
