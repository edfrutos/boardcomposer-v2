import pytest
from PySide6.QtWidgets import QApplication, QDialog

from studio.inventory_service import ScrapInventoryService
from studio.main_window import MainWindow
from studio.project.scrap_inventory import ScrapRecord
from studio.services import StudioServices


@pytest.fixture
def window(tmp_path):
    QApplication.instance() or QApplication([])
    inventory = ScrapInventoryService(db_path=tmp_path / "retales.db")
    return MainWindow(services=StudioServices(), inventory=inventory)


class _FakeAddScrapDialog:
    def __init__(self, values, accepted=True):
        self._values = values
        self._accepted = accepted

    def exec(self):
        return (
            QDialog.DialogCode.Accepted
            if self._accepted
            else QDialog.DialogCode.Rejected
        )

    def values(self):
        return self._values


class _FakeUseScrapDialog:
    def __init__(self, scrap, accepted=True):
        self._scrap = scrap
        self._accepted = accepted

    def exec(self):
        return (
            QDialog.DialogCode.Accepted
            if self._accepted
            else QDialog.DialogCode.Rejected
        )

    def selected_scrap(self):
        return self._scrap


def test_add_scrap_to_inventory_adds_it(window, monkeypatch):
    monkeypatch.setattr(
        "studio.main_window.AddScrapDialog",
        lambda *a, **k: _FakeAddScrapDialog(
            ("R-001", 800, 400, 19, "Roble", "Mueble X")
        ),
    )

    window._add_scrap_to_inventory()

    scraps = window.inventory.list_available()
    assert len(scraps) == 1
    assert scraps[0].scrap_id == "R-001"
    assert "añadido al inventario" in window.statusBar().currentMessage()


def test_add_scrap_to_inventory_rejects_a_duplicate_id(window, monkeypatch):
    window.inventory.add("R-001", 800, 400, 19)
    monkeypatch.setattr(
        "studio.main_window.AddScrapDialog",
        lambda *a, **k: _FakeAddScrapDialog(("R-001", 500, 300, 19, "", "")),
    )

    window._add_scrap_to_inventory()

    assert len(window.inventory.list_available()) == 1
    assert "Ya existe" in window.statusBar().currentMessage()


def test_use_scrap_from_inventory_adds_a_board_and_consumes_it(window, monkeypatch):
    window.inventory.add("R-001", 800, 400, 19, material="Roble", origin="Mueble X")
    scrap = window.inventory.list_available()[0]
    monkeypatch.setattr(
        "studio.main_window.UseScrapDialog", lambda *a, **k: _FakeUseScrapDialog(scrap)
    )

    window._use_scrap_from_inventory()

    project = window.services.projects.current_project
    board = next(b for b in project.boards if b.board_id == "R-001")
    assert board.length_mm == 800
    assert board.width_mm == 400
    assert board.material == "Roble"
    assert window.inventory.list_available() == []


def test_use_scrap_from_inventory_without_a_project_shows_a_message(
    window, monkeypatch
):
    window.services.projects.close_project()
    window.inventory.add("R-001", 800, 400, 19)

    window._use_scrap_from_inventory()

    assert "proyecto" in window.statusBar().currentMessage()
    assert len(window.inventory.list_available()) == 1


def test_use_scrap_from_inventory_with_an_empty_inventory_shows_a_message(window):
    window._use_scrap_from_inventory()

    assert "inventario" in window.statusBar().currentMessage()


def test_use_scrap_from_inventory_rejects_a_board_id_collision(window, monkeypatch):
    # TAB-001 already exists on the demo project the `window` fixture loads.
    scrap = ScrapRecord("TAB-001", 800, 400, 19, "", "", "2026-08-09")
    window.inventory.add("TAB-001", 800, 400, 19)
    monkeypatch.setattr(
        "studio.main_window.UseScrapDialog", lambda *a, **k: _FakeUseScrapDialog(scrap)
    )

    window._use_scrap_from_inventory()

    assert "Ya existe un tablero" in window.statusBar().currentMessage()
    assert len(window.inventory.list_available()) == 1
