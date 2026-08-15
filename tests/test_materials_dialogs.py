from PySide6.QtWidgets import QApplication

from studio.dialogs import MaterialDialog, MaterialsLibraryDialog
from studio.inventory_service import ScrapInventoryService
from studio.materials_service import MaterialsLibraryService


def _app():
    return QApplication.instance() or QApplication([])


def test_material_dialog_defaults_and_values():
    _app()
    dialog = MaterialDialog(material_id="AGL18", name="Aglomerado")

    assert dialog.values() == ("AGL18", "Aglomerado", 19.0, "", 0.0, "board")


def test_material_dialog_id_editable_flag_disables_the_field():
    _app()
    dialog = MaterialDialog(material_id="AGL18", id_editable=False)

    assert dialog.id_edit.isEnabled() is False


def test_material_dialog_rejects_an_empty_id_without_closing():
    _app()
    dialog = MaterialDialog()
    dialog.id_edit.setText("   ")

    dialog._try_accept()

    assert dialog.result() == 0
    assert dialog.error_label.isHidden() is False


def test_material_dialog_rejects_a_duplicate_id_without_closing():
    _app()
    dialog = MaterialDialog(existing_ids=frozenset({"AGL18"}))
    dialog.id_edit.setText("AGL18")
    dialog.name_edit.setText("Aglomerado")

    dialog._try_accept()

    assert dialog.result() == 0
    assert "Ya existe" in dialog.error_label.text()


def test_material_dialog_rejects_an_empty_name_without_closing():
    _app()
    dialog = MaterialDialog()
    dialog.id_edit.setText("AGL18")
    dialog.name_edit.setText("   ")

    dialog._try_accept()

    assert dialog.result() == 0
    assert "nombre" in dialog.error_label.text()


def test_material_dialog_accepts_a_unique_id_and_name():
    _app()
    dialog = MaterialDialog(existing_ids=frozenset({"AGL18"}))
    dialog.id_edit.setText("PINO25")
    dialog.name_edit.setText("Pino")

    dialog._try_accept()

    assert dialog.result() == int(dialog.DialogCode.Accepted)


def test_material_dialog_price_unit_selection():
    _app()
    dialog = MaterialDialog(material_id="AGL18", name="Aglomerado", price_unit="m2")

    _, _, _, _, _, price_unit = dialog.values()

    assert price_unit == "m2"


def test_materials_library_dialog_lists_existing_materials(tmp_path):
    _app()
    service = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    service.add("AGL18", "Aglomerado", 18, provider="Leroy", price=25.5)

    dialog = MaterialsLibraryDialog(service=service)

    assert dialog.table.rowCount() == 1
    assert dialog.table.item(0, 0).text() == "AGL18"


def test_materials_library_dialog_add_material_persists_and_reloads(
    tmp_path, monkeypatch
):
    _app()
    service = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    dialog = MaterialsLibraryDialog(service=service)

    class _FakeAddDialog:
        def exec(self):
            from PySide6.QtWidgets import QDialog

            return QDialog.DialogCode.Accepted

        def values(self):
            return ("AGL18", "Aglomerado", 18.0, "Leroy", 25.5, "board")

    monkeypatch.setattr(
        "studio.dialogs.materials_dialogs.MaterialDialog",
        lambda *a, **k: _FakeAddDialog(),
    )

    dialog._add_material()

    assert service.list_materials()[0].material_id == "AGL18"
    assert dialog.table.rowCount() == 1


def test_materials_library_dialog_delete_material_removes_it(tmp_path, monkeypatch):
    _app()
    service = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    service.add("AGL18", "Aglomerado", 18)
    dialog = MaterialsLibraryDialog(service=service)
    dialog.table.selectRow(0)

    from PySide6.QtWidgets import QMessageBox

    monkeypatch.setattr(
        QMessageBox, "question", lambda *a, **k: QMessageBox.StandardButton.Yes
    )

    dialog._delete_material()

    assert service.list_materials() == []
    assert dialog.table.rowCount() == 0


def test_materials_library_dialog_scrap_column_shows_dash_without_inventory(tmp_path):
    _app()
    service = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    service.add("AGL18", "Aglomerado", 18)

    dialog = MaterialsLibraryDialog(service=service)

    assert dialog.table.item(0, 6).text() == "-"


def test_materials_library_dialog_scrap_column_counts_matching_scraps(tmp_path):
    _app()
    service = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    service.add("AGL18", "Aglomerado", 18)
    service.add("PINO25", "Pino", 25)
    inventory = ScrapInventoryService(db_path=tmp_path / "retales.db")
    inventory.add("R-001", 800, 400, 18, material="Aglomerado")
    inventory.add("R-002", 500, 300, 18, material="Aglomerado")
    inventory.add("R-003", 600, 300, 10, material="Aglomerado")  # distinto grosor

    dialog = MaterialsLibraryDialog(service=service, scrap_inventory=inventory)

    rows = {
        dialog.table.item(row, 0).text(): dialog.table.item(row, 6).text()
        for row in range(dialog.table.rowCount())
    }
    assert rows["AGL18"] == "2"
    assert rows["PINO25"] == "0"


def test_view_scraps_without_a_selection_shows_an_error(tmp_path):
    _app()
    service = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    inventory = ScrapInventoryService(db_path=tmp_path / "retales.db")
    dialog = MaterialsLibraryDialog(service=service, scrap_inventory=inventory)

    dialog._view_scraps()

    assert "Selecciona" in dialog.error_label.text()


def test_view_scraps_without_an_inventory_shows_an_error(tmp_path):
    _app()
    service = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    service.add("AGL18", "Aglomerado", 18)
    dialog = MaterialsLibraryDialog(service=service)
    dialog.table.selectRow(0)

    dialog._view_scraps()

    assert "inventario" in dialog.error_label.text()


def test_view_scraps_opens_a_dialog_listing_matching_scraps(tmp_path, monkeypatch):
    _app()
    service = MaterialsLibraryService(db_path=tmp_path / "materiales.db")
    service.add("AGL18", "Aglomerado", 18)
    inventory = ScrapInventoryService(db_path=tmp_path / "retales.db")
    inventory.add("R-001", 800, 400, 18, material="Aglomerado")
    dialog = MaterialsLibraryDialog(service=service, scrap_inventory=inventory)
    dialog.table.selectRow(0)

    captured = {}

    class _FakeMatchingScrapsDialog:
        def __init__(self, *args, **kwargs):
            captured["material_label"] = kwargs.get("material_label")
            captured["scraps"] = kwargs.get("scraps")

        def exec(self):
            captured["executed"] = True

    monkeypatch.setattr(
        "studio.dialogs.materials_dialogs.MatchingScrapsDialog",
        _FakeMatchingScrapsDialog,
    )

    dialog._view_scraps()

    assert captured["executed"] is True
    assert captured["material_label"] == "Aglomerado (18 mm)"
    assert [s.scrap_id for s in captured["scraps"]] == ["R-001"]


def test_matching_scraps_dialog_lists_the_given_scraps():
    _app()
    from studio.dialogs import MatchingScrapsDialog
    from studio.project.scrap_inventory import ScrapRecord

    scraps = [ScrapRecord("R-001", 800, 400, 18, "Aglomerado", "Mueble X", "2026")]

    dialog = MatchingScrapsDialog(material_label="Aglomerado (18 mm)", scraps=scraps)

    assert dialog.table.rowCount() == 1
    assert dialog.table.item(0, 0).text() == "R-001"
