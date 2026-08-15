import pytest
from PySide6.QtWidgets import QApplication, QDialog

from studio.main_window import MainWindow
from studio.materials_service import MaterialsLibraryService
from studio.services import StudioServices


@pytest.fixture
def window(tmp_path):
    QApplication.instance() or QApplication([])
    materials = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    return MainWindow(services=StudioServices(), materials=materials)


def test_material_names_is_empty_for_a_fresh_catalog(window):
    assert window._material_names() == []


def test_material_names_deduplicates_by_name(window):
    window.materials.add("AGL10", "Aglomerado", 10)
    window.materials.add("AGL18", "Aglomerado", 18)
    window.materials.add("PINO25", "Pino", 25)

    assert window._material_names() == ["Aglomerado", "Pino"]


class _FakeMaterialsLibraryDialog:
    def __init__(self, *args, **kwargs):
        self.executed = False

    def exec(self):
        self.executed = True
        return QDialog.DialogCode.Accepted


def test_open_materials_library_opens_the_dialog(window, monkeypatch):
    fake = _FakeMaterialsLibraryDialog()
    monkeypatch.setattr(
        "studio.main_window.MaterialsLibraryDialog", lambda *a, **k: fake
    )

    window._open_materials_library()

    assert fake.executed is True


def test_open_materials_library_passes_the_scrap_inventory(window, monkeypatch):
    captured = {}

    class _CapturingDialog:
        def __init__(self, *args, **kwargs):
            captured.update(kwargs)

        def exec(self):
            return QDialog.DialogCode.Accepted

    monkeypatch.setattr("studio.main_window.MaterialsLibraryDialog", _CapturingDialog)

    window._open_materials_library()

    assert captured["scrap_inventory"] is window.inventory


def test_add_board_dialog_receives_the_catalog_names(window, monkeypatch):
    window.materials.add("AGL18", "Aglomerado", 18)
    captured = {}

    class _FakeBoardDialog:
        def __init__(self, *args, **kwargs):
            captured["materials"] = kwargs.get("materials")

        def exec(self):
            return QDialog.DialogCode.Rejected

    monkeypatch.setattr("studio.main_window.BoardDialog", _FakeBoardDialog)

    window._add_board()

    assert captured["materials"] == ["Aglomerado"]
