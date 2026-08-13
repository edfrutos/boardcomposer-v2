from PySide6.QtWidgets import QApplication

from studio.dialogs import MaterialDialog, MaterialsLibraryDialog
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
