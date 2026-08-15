"""Read-only cross-reference between the materials catalog (IDE-0041) and
the scrap inventory (IDE-0039) — IDE-0042.

Deliberately pure and tiny: the user asked for this to inform which
scraps they already own for a given catalog material, so they can favor
what's on the shelf over cutting new stock — a query, not a solver
change (scoped explicitly with the user: the solver and the automatic
best-fit distribution stay untouched).

Matching is exact on name and thickness_mm, same convention as every
other material/thickness comparison in the codebase (StudioBoard vs
StudioPiece thickness matching, `IDE-0038`) — no fuzzy tolerance.
"""

from studio.project.scrap_inventory import ScrapRecord


def matching_scraps(
    scraps: list[ScrapRecord], material_name: str, thickness_mm: float
) -> list[ScrapRecord]:
    return [
        scrap
        for scrap in scraps
        if scrap.material == material_name and scrap.thickness_mm == thickness_mm
    ]
