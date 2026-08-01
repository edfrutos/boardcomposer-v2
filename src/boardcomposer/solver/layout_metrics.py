"""Post-hoc geometric analysis of an already-solved AssemblySolution
(IDE-0023) — how fragmented the leftover material is, and roughly how many
saw cuts the layout needs. `comparator_panel.py` deliberately left both
uncalculated until now rather than fill them with invented numbers.

Distinct from `scoring.py`'s `evaluate()`: that ranks candidates against
each other during the solve; these describe one already-chosen candidate's
geometry after the fact, for a human comparing it against others.
"""

from boardcomposer.domain import AssemblySolution, BoardPlacement
from boardcomposer.geometry import Rectangle
from boardcomposer.layout.bounds import bounding_rectangle


def _subtract(free: Rectangle, used: Rectangle) -> list[Rectangle]:
    """Rectangle-minus-rectangle: `free` split into the parts not covered
    by its overlap with `used`. Left/right slivers keep `free`'s full
    height; top/bottom slivers are narrowed to the overlap's width, so the
    resulting pieces never overlap each other — no double-counted area."""
    if not free.overlaps(used):
        return [free]

    ix = max(free.x_mm, used.x_mm)
    iy = max(free.y_mm, used.y_mm)
    iright = min(free.right_mm, used.right_mm)
    itop = min(free.top_mm, used.top_mm)

    pieces = []
    if ix > free.x_mm:
        pieces.append(Rectangle(free.x_mm, free.y_mm, ix - free.x_mm, free.width_mm))
    if free.right_mm > iright:
        pieces.append(
            Rectangle(iright, free.y_mm, free.right_mm - iright, free.width_mm)
        )
    if iy > free.y_mm:
        pieces.append(Rectangle(ix, free.y_mm, iright - ix, iy - free.y_mm))
    if free.top_mm > itop:
        pieces.append(Rectangle(ix, itop, iright - ix, free.top_mm - itop))
    return pieces


def _free_rectangles(
    placements: list[BoardPlacement], bounds: Rectangle
) -> list[Rectangle]:
    free = [bounds]
    for placement in placements:
        used = Rectangle(
            placement.x_mm, placement.y_mm, placement.length_mm, placement.width_mm
        )
        free = [piece for rect in free for piece in _subtract(rect, used)]
    return free


def fragmentation_ratio(solution: AssemblySolution) -> float:
    """1 = el hueco libre está roto en fragmentos pequeños; 0 = un único
    hueco contiguo (o sin hueco que fragmentar). Descompone el área libre
    del rectángulo envolvente en rectángulos disjuntos y compara el mayor
    contra el total — mismo rectángulo envolvente que ya usa `waste_ratio`,
    no las dimensiones reales del tablero físico."""
    if not solution.placements:
        return 0.0

    bounds = bounding_rectangle(solution.placements)
    total_free = bounds.area_mm2 - solution.used_area_mm2
    if total_free <= 0:
        return 0.0

    free_rects = _free_rectangles(solution.placements, bounds)
    largest_free = max((rect.area_mm2 for rect in free_rects), default=0.0)
    return 1 - (largest_free / total_free)


def cut_count(solution: AssemblySolution) -> int:
    """Aproximación, no cifra exacta: cuenta líneas de corte interiores
    distintas (verticales + horizontales) entre bordes de pieza que no
    coinciden con el borde del rectángulo envolvente, asumiendo corte
    guillotina de línea completa — mismo supuesto que ya usa el kerf
    (DEC-0016: N piezas en fila = N-1 cortes). Layouts no-guillotina
    (posibles en MaxRects/Skyline) pueden infracontar: un corte real ahí
    necesitaría más de una línea recta."""
    if not solution.placements:
        return 0

    bounds = bounding_rectangle(solution.placements)
    x_cuts: set[float] = set()
    y_cuts: set[float] = set()

    for placement in solution.placements:
        if placement.x_mm > bounds.x_mm:
            x_cuts.add(round(placement.x_mm, 6))
        if placement.right_mm < bounds.right_mm:
            x_cuts.add(round(placement.right_mm, 6))
        if placement.y_mm > bounds.y_mm:
            y_cuts.add(round(placement.y_mm, 6))
        if placement.top_mm < bounds.top_mm:
            y_cuts.add(round(placement.top_mm, 6))

    return len(x_cuts) + len(y_cuts)
