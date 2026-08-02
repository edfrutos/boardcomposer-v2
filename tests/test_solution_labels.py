import pytest

from studio.solution_labels import solution_label


def test_solution_label_uses_letters_for_the_first_26():
    assert solution_label(0) == "A"
    assert solution_label(1) == "B"
    assert solution_label(3) == "D"


def test_solution_label_falls_back_to_a_number_past_z():
    assert solution_label(26) == "27"


def test_solution_label_rejects_negative_index():
    with pytest.raises(ValueError):
        solution_label(-1)
