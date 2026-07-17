from studio.main_window import _generate_ids


def test_generate_ids_returns_just_the_base_id_for_quantity_one():
    assert _generate_ids("p1", 1, frozenset()) == ["p1"]


def test_generate_ids_suffixes_extra_copies():
    assert _generate_ids("p1", 3, frozenset()) == ["p1", "p1-2", "p1-3"]


def test_generate_ids_skips_suffixes_already_taken():
    existing = frozenset({"p1-2"})

    assert _generate_ids("p1", 2, existing) == ["p1", "p1-3"]
