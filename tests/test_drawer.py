import pytest

from studio.containers import (
    CONTAINER_TEMPLATES,
    ContainerTemplateError,
    build_drawer_no_rails_pieces,
)


def test_registry_has_drawer_no_rails():
    assert CONTAINER_TEMPLATES["cajon_sin_rieles"] is build_drawer_no_rails_pieces


def test_derives_outer_dimensions_from_opening_and_clearance():
    pieces = build_drawer_no_rails_pieces(
        opening_length_mm=300.0,
        opening_height_mm=100.0,
        depth_mm=200.0,
        clearance_mm=1.5,
        thickness_mm=18.0,
    )
    by_id = {piece.piece_id: piece for piece in pieces}

    assert len(pieces) == 5
    # Ancho/alto = hueco - 2 x holgura; profundidad va directa (no depende del hueco).
    assert by_id["cajon-base"].length_mm == 300.0 - 2 * 1.5
    assert by_id["cajon-base"].width_mm == 200.0
    assert by_id["cajon-pared-frontal"].length_mm == 300.0 - 2 * 1.5
    assert by_id["cajon-pared-frontal"].width_mm == 100.0 - 2 * 1.5
    for piece in pieces:
        assert piece.thickness_mm == 18.0
        assert piece.material == "Demo"


def test_zero_clearance_is_allowed():
    pieces = build_drawer_no_rails_pieces(
        opening_length_mm=300.0,
        opening_height_mm=100.0,
        depth_mm=200.0,
        clearance_mm=0.0,
        thickness_mm=18.0,
    )
    by_id = {piece.piece_id: piece for piece in pieces}
    assert by_id["cajon-base"].length_mm == 300.0


def test_custom_prefix_and_material():
    pieces = build_drawer_no_rails_pieces(
        opening_length_mm=300.0,
        opening_height_mm=100.0,
        depth_mm=200.0,
        clearance_mm=1.5,
        thickness_mm=18.0,
        material="Contrachapado",
        id_prefix="gaveta",
    )
    ids = {piece.piece_id for piece in pieces}
    assert ids == {
        "gaveta-base",
        "gaveta-pared-frontal",
        "gaveta-pared-trasera",
        "gaveta-lateral-izquierdo",
        "gaveta-lateral-derecho",
    }
    assert all(piece.material == "Contrachapado" for piece in pieces)


@pytest.mark.parametrize(
    "field", ["opening_length_mm", "opening_height_mm", "depth_mm", "thickness_mm"]
)
@pytest.mark.parametrize("bad_value", [0, -1.0, float("nan"), float("inf")])
def test_rejects_non_finite_or_non_positive_dimensions(field, bad_value):
    kwargs = {
        "opening_length_mm": 300.0,
        "opening_height_mm": 100.0,
        "depth_mm": 200.0,
        "clearance_mm": 1.5,
        "thickness_mm": 18.0,
    }
    kwargs[field] = bad_value
    with pytest.raises(ContainerTemplateError):
        build_drawer_no_rails_pieces(**kwargs)


@pytest.mark.parametrize("bad_clearance", [-1.0, float("nan"), float("inf")])
def test_rejects_invalid_clearance(bad_clearance):
    with pytest.raises(ContainerTemplateError):
        build_drawer_no_rails_pieces(
            opening_length_mm=300.0,
            opening_height_mm=100.0,
            depth_mm=200.0,
            clearance_mm=bad_clearance,
            thickness_mm=18.0,
        )


def test_rejects_clearance_too_large_for_opening():
    with pytest.raises(ContainerTemplateError):
        build_drawer_no_rails_pieces(
            opening_length_mm=300.0,
            opening_height_mm=10.0,
            depth_mm=200.0,
            clearance_mm=6.0,
            thickness_mm=18.0,
        )


def test_rejects_id_collision_with_existing_ids():
    with pytest.raises(ContainerTemplateError):
        build_drawer_no_rails_pieces(
            opening_length_mm=300.0,
            opening_height_mm=100.0,
            depth_mm=200.0,
            clearance_mm=1.5,
            thickness_mm=18.0,
            existing_ids=frozenset({"cajon-base"}),
        )
