import pytest

from studio.inventory_service import ScrapInventoryService
from studio.project.scrap_inventory import ScrapInventoryError


@pytest.fixture
def service(tmp_path):
    return ScrapInventoryService(db_path=tmp_path / "retales.db")


def test_add_and_list_available(service):
    service.add("R-001", 800, 400, 19, material="Roble", origin="Mueble X")

    scraps = service.list_available()

    assert len(scraps) == 1
    assert scraps[0].scrap_id == "R-001"


def test_consume_removes_from_list_available(service):
    service.add("R-001", 800, 400, 19)

    service.consume("R-001")

    assert service.list_available() == []


def test_add_rejects_a_duplicate_id(service):
    service.add("R-001", 800, 400, 19)

    with pytest.raises(ScrapInventoryError):
        service.add("R-001", 500, 300, 19)
