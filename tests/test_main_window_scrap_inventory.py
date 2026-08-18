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
    def __init__(self, scrap=None, accepted=True, new_board_requested=False):
        self._scrap = scrap
        self._accepted = accepted
        self.new_board_requested = new_board_requested

    def exec(self):
        return (
            QDialog.DialogCode.Accepted
            if self._accepted
            else QDialog.DialogCode.Rejected
        )

    def selected_scrap(self):
        return self._scrap


class _FakeBoardDialog:
    def __init__(self, values, accepted=True, quantity=1):
        self._values = values
        self._accepted = accepted
        self._quantity = quantity

    def exec(self):
        return (
            QDialog.DialogCode.Accepted
            if self._accepted
            else QDialog.DialogCode.Rejected
        )

    def values(self):
        return self._values

    def quantity(self):
        return self._quantity


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


def test_add_board_offers_a_matching_scrap_and_consumes_it_on_selection(
    window, monkeypatch
):
    window.inventory.add("R-001", 800, 400, 19, material="Roble", origin="Mueble X")
    scrap = window.inventory.list_available()[0]
    monkeypatch.setattr(
        "studio.main_window.UseScrapDialog", lambda *a, **k: _FakeUseScrapDialog(scrap)
    )

    window._add_board()

    project = window.services.projects.current_project
    board = next(b for b in project.boards if b.board_id == "R-001")
    assert board.length_mm == 800
    assert board.width_mm == 400
    assert board.material == "Roble"
    assert window.inventory.list_available() == []


def test_add_board_without_a_project_does_nothing(window, monkeypatch):
    window.services.projects.close_project()
    window.inventory.add("R-001", 800, 400, 19)
    monkeypatch.setattr(
        "studio.main_window.UseScrapDialog",
        lambda *a, **k: pytest.fail("no project — UseScrapDialog shouldn't open"),
    )

    window._add_board()

    assert len(window.inventory.list_available()) == 1


def test_add_board_with_an_empty_inventory_goes_straight_to_the_new_board_dialog(
    window, monkeypatch
):
    monkeypatch.setattr(
        "studio.main_window.UseScrapDialog",
        lambda *a, **k: pytest.fail("empty inventory — UseScrapDialog shouldn't open"),
    )
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeBoardDialog(("B2", 1500, 400, "Demo", 19.0)),
    )

    window._add_board()

    project = window.services.projects.current_project
    assert any(board.board_id == "B2" for board in project.boards)


def test_add_board_new_board_requested_falls_through_to_the_new_board_dialog(
    window, monkeypatch
):
    window.inventory.add("R-001", 800, 400, 19)
    monkeypatch.setattr(
        "studio.main_window.UseScrapDialog",
        lambda *a, **k: _FakeUseScrapDialog(accepted=False, new_board_requested=True),
    )
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: _FakeBoardDialog(("B2", 1500, 400, "Demo", 19.0)),
    )

    window._add_board()

    project = window.services.projects.current_project
    assert any(board.board_id == "B2" for board in project.boards)
    # The scrap was never touched — the user explicitly asked for a new board.
    assert len(window.inventory.list_available()) == 1


def test_add_board_cancelled_outright_does_nothing(window, monkeypatch):
    window.inventory.add("R-001", 800, 400, 19)
    monkeypatch.setattr(
        "studio.main_window.UseScrapDialog",
        lambda *a, **k: _FakeUseScrapDialog(accepted=False, new_board_requested=False),
    )
    monkeypatch.setattr(
        "studio.main_window.BoardDialog",
        lambda *a, **k: pytest.fail("cancelled outright — BoardDialog shouldn't open"),
    )
    boards_before = len(window.services.projects.current_project.boards)

    window._add_board()

    assert len(window.services.projects.current_project.boards) == boards_before
    assert len(window.inventory.list_available()) == 1


def test_add_board_rejects_a_scrap_that_collides_with_an_existing_board_id(
    window, monkeypatch
):
    # TAB-001 already exists on the demo project the `window` fixture loads.
    scrap = ScrapRecord("TAB-001", 800, 400, 19, "", "", "2026-08-09")
    window.inventory.add("TAB-001", 800, 400, 19)
    monkeypatch.setattr(
        "studio.main_window.UseScrapDialog", lambda *a, **k: _FakeUseScrapDialog(scrap)
    )

    window._add_board()

    assert "Ya existe un tablero" in window.statusBar().currentMessage()
    assert len(window.inventory.list_available()) == 1
