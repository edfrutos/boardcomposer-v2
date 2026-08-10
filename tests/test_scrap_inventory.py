import pytest

from studio.project.scrap_inventory import (
    ScrapInventoryError,
    add_scrap,
    consume,
    list_available,
)


@pytest.fixture
def db_path(tmp_path):
    return tmp_path / "retales.db"


def test_list_available_is_empty_for_a_fresh_database(db_path):
    assert list_available(db_path) == []


def test_add_scrap_appears_in_list_available(db_path):
    add_scrap(db_path, "R-001", 800, 400, 19, material="Roble", origin="Mueble X")

    scraps = list_available(db_path)

    assert len(scraps) == 1
    assert scraps[0].scrap_id == "R-001"
    assert scraps[0].length_mm == 800
    assert scraps[0].width_mm == 400
    assert scraps[0].thickness_mm == 19
    assert scraps[0].material == "Roble"
    assert scraps[0].origin == "Mueble X"


def test_add_scrap_defaults_material_and_origin_to_empty_string(db_path):
    add_scrap(db_path, "R-001", 800, 400, 19)

    scraps = list_available(db_path)

    assert scraps[0].material == ""
    assert scraps[0].origin == ""


def test_list_available_is_sorted_by_area_ascending(db_path):
    add_scrap(db_path, "big", 2000, 1000, 19)
    add_scrap(db_path, "small", 300, 200, 19)
    add_scrap(db_path, "medium", 800, 400, 19)

    scraps = list_available(db_path)

    assert [scrap.scrap_id for scrap in scraps] == ["small", "medium", "big"]


def test_add_scrap_rejects_an_empty_id(db_path):
    with pytest.raises(ScrapInventoryError, match="necesita un id"):
        add_scrap(db_path, "  ", 800, 400, 19)


def test_add_scrap_rejects_a_duplicate_id(db_path):
    add_scrap(db_path, "R-001", 800, 400, 19)

    with pytest.raises(ScrapInventoryError, match="Ya existe un retal"):
        add_scrap(db_path, "R-001", 500, 300, 19)


@pytest.mark.parametrize("value", [0, -100, float("nan"), float("inf")])
def test_add_scrap_rejects_unusable_dimensions(db_path, value):
    with pytest.raises(ScrapInventoryError, match="número finito mayor que 0"):
        add_scrap(db_path, "R-001", value, 400, 19)


def test_consume_removes_a_scrap_from_the_available_list(db_path):
    add_scrap(db_path, "R-001", 800, 400, 19)

    consume(db_path, "R-001")

    assert list_available(db_path) == []


def test_consume_keeps_the_row_for_history_instead_of_deleting_it(db_path):
    import sqlite3

    add_scrap(db_path, "R-001", 800, 400, 19)
    consume(db_path, "R-001")

    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT consumed_at FROM scraps WHERE scrap_id = ?", ("R-001",)
        ).fetchone()

    assert row is not None
    assert row[0] is not None


def test_consume_rejects_an_unknown_id(db_path):
    with pytest.raises(ScrapInventoryError, match="No existe ningún retal"):
        consume(db_path, "ghost")


def test_consume_rejects_an_already_consumed_scrap(db_path):
    add_scrap(db_path, "R-001", 800, 400, 19)
    consume(db_path, "R-001")

    with pytest.raises(ScrapInventoryError, match="ya estaba consumido"):
        consume(db_path, "R-001")
