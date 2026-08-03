import pytest

from studio.containers import CONTAINER_TEMPLATES, ContainerTemplateError, build_simple_box_pieces


def test_registry_has_simple_box():
    assert CONTAINER_TEMPLATES["caja_simple"] is build_simple_box_pieces


def test_builds_five_pieces_with_expected_dimensions():
    pieces = build_simple_box_pieces(
        outer_length_mm=300.0,
        outer_width_mm=200.0,
        outer_height_mm=100.0,
        thickness_mm=18.0,
    )
    by_id = {piece.piece_id: piece for piece in pieces}

    assert len(pieces) == 5
    assert by_id["caja-base"].length_mm == 300.0
    assert by_id["caja-base"].width_mm == 200.0
    assert by_id["caja-pared-frontal"].length_mm == 300.0
    assert by_id["caja-pared-frontal"].width_mm == 100.0
    assert by_id["caja-pared-trasera"].length_mm == 300.0
    assert by_id["caja-pared-trasera"].width_mm == 100.0
    # Laterales encajan entre frontal y trasera: ancho exterior menos 2 grosores.
    assert by_id["caja-lateral-izquierdo"].length_mm == 200.0 - 2 * 18.0
    assert by_id["caja-lateral-izquierdo"].width_mm == 100.0
    assert by_id["caja-lateral-derecho"].length_mm == 200.0 - 2 * 18.0
    for piece in pieces:
        assert piece.thickness_mm == 18.0
        assert piece.material == "Demo"


def test_custom_prefix_and_material():
    pieces = build_simple_box_pieces(
        outer_length_mm=300.0,
        outer_width_mm=200.0,
        outer_height_mm=100.0,
        thickness_mm=18.0,
        material="Contrachapado",
        id_prefix="organizador",
    )
    ids = {piece.piece_id for piece in pieces}
    assert ids == {
        "organizador-base",
        "organizador-pared-frontal",
        "organizador-pared-trasera",
        "organizador-lateral-izquierdo",
        "organizador-lateral-derecho",
    }
    assert all(piece.material == "Contrachapado" for piece in pieces)


@pytest.mark.parametrize(
    "field",
    ["outer_length_mm", "outer_width_mm", "outer_height_mm", "thickness_mm"],
)
@pytest.mark.parametrize("bad_value", [0, -1.0, float("nan"), float("inf")])
def test_rejects_non_finite_or_non_positive_dimensions(field, bad_value):
    kwargs = {
        "outer_length_mm": 300.0,
        "outer_width_mm": 200.0,
        "outer_height_mm": 100.0,
        "thickness_mm": 18.0,
    }
    kwargs[field] = bad_value
    with pytest.raises(ContainerTemplateError):
        build_simple_box_pieces(**kwargs)


def test_rejects_width_too_small_for_thickness():
    with pytest.raises(ContainerTemplateError):
        build_simple_box_pieces(
            outer_length_mm=300.0,
            outer_width_mm=30.0,
            outer_height_mm=100.0,
            thickness_mm=18.0,
        )


def test_rejects_unsupported_joint():
    with pytest.raises(ContainerTemplateError):
        build_simple_box_pieces(
            outer_length_mm=300.0,
            outer_width_mm=200.0,
            outer_height_mm=100.0,
            thickness_mm=18.0,
            joint="rebajada",
        )


def test_rejects_unsupported_dividers():
    with pytest.raises(ContainerTemplateError):
        build_simple_box_pieces(
            outer_length_mm=300.0,
            outer_width_mm=200.0,
            outer_height_mm=100.0,
            thickness_mm=18.0,
            dividers=2,
        )


def test_rejects_id_collision_with_existing_ids():
    with pytest.raises(ContainerTemplateError):
        build_simple_box_pieces(
            outer_length_mm=300.0,
            outer_width_mm=200.0,
            outer_height_mm=100.0,
            thickness_mm=18.0,
            existing_ids=frozenset({"caja-base"}),
        )
