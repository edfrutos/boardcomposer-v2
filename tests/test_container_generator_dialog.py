import pytest
from PySide6.QtWidgets import QApplication

from studio.dialogs.container_generator_dialog import ContainerGeneratorDialog


@pytest.fixture
def dialog():
    QApplication.instance() or QApplication([])
    return ContainerGeneratorDialog()


def _select(dialog, key):
    index = dialog.template_combo.findData(key)
    dialog.template_combo.setCurrentIndex(index)


def test_defaults_to_simple_box_values(dialog):
    values = dialog.values()
    assert values.keys() == {
        "outer_length_mm",
        "outer_width_mm",
        "outer_height_mm",
        "thickness_mm",
        "material",
        "id_prefix",
    }
    assert values["id_prefix"] == "caja"


def test_switching_to_drawer_swaps_values_shape(dialog):
    _select(dialog, "cajon_sin_rieles")
    values = dialog.values()
    assert values.keys() == {
        "opening_length_mm",
        "opening_height_mm",
        "depth_mm",
        "clearance_mm",
        "thickness_mm",
        "material",
        "id_prefix",
    }
    assert values["id_prefix"] == "cajon"


def test_switching_back_restores_simple_box_prefix(dialog):
    _select(dialog, "cajon_sin_rieles")
    _select(dialog, "caja_simple")
    assert dialog.prefix_edit.text() == "caja"


def test_custom_prefix_survives_template_switch(dialog):
    dialog.prefix_edit.setText("organizador")
    _select(dialog, "cajon_sin_rieles")
    assert dialog.prefix_edit.text() == "organizador"


def test_drawer_fields_hidden_for_simple_box(dialog):
    assert dialog.form.isRowVisible(dialog.length_spin)
    assert not dialog.form.isRowVisible(dialog.opening_length_spin)


def test_simple_box_fields_hidden_for_drawer(dialog):
    _select(dialog, "cajon_sin_rieles")
    assert not dialog.form.isRowVisible(dialog.length_spin)
    assert dialog.form.isRowVisible(dialog.opening_length_spin)
