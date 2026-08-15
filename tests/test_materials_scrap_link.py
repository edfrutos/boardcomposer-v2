from studio.project.materials_scrap_link import matching_scraps
from studio.project.scrap_inventory import ScrapRecord


def _scrap(scrap_id, material, thickness_mm, length_mm=800, width_mm=400):
    return ScrapRecord(
        scrap_id, length_mm, width_mm, thickness_mm, material, "", "2026-08-15"
    )


def test_matching_scraps_filters_by_material_and_thickness():
    scraps = [
        _scrap("R-001", "Aglomerado", 18),
        _scrap("R-002", "Aglomerado", 10),
        _scrap("R-003", "Contrachapado", 18),
    ]

    result = matching_scraps(scraps, "Aglomerado", 18)

    assert [s.scrap_id for s in result] == ["R-001"]


def test_matching_scraps_returns_every_match():
    scraps = [
        _scrap("R-001", "Aglomerado", 18),
        _scrap("R-002", "Aglomerado", 18),
    ]

    result = matching_scraps(scraps, "Aglomerado", 18)

    assert [s.scrap_id for s in result] == ["R-001", "R-002"]


def test_matching_scraps_is_empty_when_nothing_matches():
    scraps = [_scrap("R-001", "Aglomerado", 18)]

    assert matching_scraps(scraps, "Pino", 18) == []
    assert matching_scraps(scraps, "Aglomerado", 10) == []


def test_matching_scraps_is_case_sensitive_same_as_the_rest_of_the_codebase():
    scraps = [_scrap("R-001", "aglomerado", 18)]

    assert matching_scraps(scraps, "Aglomerado", 18) == []
