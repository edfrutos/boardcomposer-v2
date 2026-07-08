"""MaxRects bin packing over a set of free rectangles."""

from boardcomposer.solver.maxrects.free_rectangle import FreeRectangle
from boardcomposer.solver.maxrects.heuristics import Heuristic, best_area_fit
from boardcomposer.solver.maxrects.placement import MaxRectsPlacement


class MaxRects:
    """Place rectangles using the MaxRects free-space algorithm."""

    def __init__(
        self,
        length_mm: float = 3000,
        width_mm: float = 3000,
        heuristic: Heuristic | None = None,
    ) -> None:
        self.length_mm = length_mm
        self.width_mm = width_mm
        self.heuristic = heuristic
        self.free_rectangles = [FreeRectangle(0, 0, length_mm, width_mm)]

    def find_candidates(
        self,
        length_mm: float,
        width_mm: float,
        allow_rotation: bool = False,
    ) -> list[MaxRectsPlacement]:
        candidates = []

        for rectangle in self.free_rectangles:
            if rectangle.fits(length_mm, width_mm):
                candidates.append(
                    MaxRectsPlacement(
                        rectangle.x_mm,
                        rectangle.y_mm,
                        length_mm,
                        width_mm,
                    )
                )

            if allow_rotation and rectangle.fits(
                length_mm=width_mm,
                width_mm=length_mm,
            ):
                candidates.append(
                    MaxRectsPlacement(
                        rectangle.x_mm,
                        rectangle.y_mm,
                        length_mm=width_mm,
                        width_mm=length_mm,
                        rotated=True,
                    )
                )

        return candidates

    def find_best_rectangle(
        self,
        length_mm: float,
        width_mm: float,
        allow_rotation: bool = False,
    ) -> MaxRectsPlacement | None:
        """Return the best placement candidate without mutating free space."""
        candidates = self.find_candidates(
            length_mm=length_mm,
            width_mm=width_mm,
            allow_rotation=allow_rotation,
        )

        if self.heuristic is not None:
            return self.heuristic(candidates, self._waste_area)

        return best_area_fit(candidates, self._waste_area)

    def place_candidate(
        self,
        placement: MaxRectsPlacement,
    ) -> MaxRectsPlacement:
        new_rectangles: list[FreeRectangle] = []

        for rectangle in self.free_rectangles:
            if not self._intersects(rectangle, placement):
                new_rectangles.append(rectangle)
                continue

            new_rectangles.extend(self._split_free_rectangle(rectangle, placement))

        self.free_rectangles = [
            rectangle for rectangle in new_rectangles if rectangle.area_mm2 > 0
        ]
        self._prune_free_rectangles()
        self._resolve_overlaps()
        self._prune_free_rectangles()

        return placement

    def place(
        self,
        length_mm: float,
        width_mm: float,
        allow_rotation: bool = False,
    ) -> MaxRectsPlacement | None:
        """Place a rectangle and update the remaining free rectangles."""
        placement = self.find_best_rectangle(
            length_mm=length_mm,
            width_mm=width_mm,
            allow_rotation=allow_rotation,
        )

        if placement is None:
            return None

        return self.place_candidate(placement)

    def _split_free_rectangle(
        self,
        rectangle: FreeRectangle,
        used: MaxRectsPlacement,
    ) -> list[FreeRectangle]:
        result = []

        rect_right = rectangle.x_mm + rectangle.length_mm
        rect_bottom = rectangle.y_mm + rectangle.width_mm
        used_right = used.x_mm + used.length_mm
        used_bottom = used.y_mm + used.width_mm

        if used.x_mm > rectangle.x_mm:
            result.append(
                FreeRectangle(
                    rectangle.x_mm,
                    rectangle.y_mm,
                    used.x_mm - rectangle.x_mm,
                    rectangle.width_mm,
                )
            )

        if used_right < rect_right:
            result.append(
                FreeRectangle(
                    used_right,
                    rectangle.y_mm,
                    rect_right - used_right,
                    rectangle.width_mm,
                )
            )

        if used.y_mm > rectangle.y_mm:
            result.append(
                FreeRectangle(
                    rectangle.x_mm,
                    rectangle.y_mm,
                    rectangle.length_mm,
                    used.y_mm - rectangle.y_mm,
                )
            )

        if used_bottom < rect_bottom:
            result.append(
                FreeRectangle(
                    rectangle.x_mm,
                    used_bottom,
                    rectangle.length_mm,
                    rect_bottom - used_bottom,
                )
            )

        return result

    def _resolve_overlaps(self) -> None:
        resolved: list[FreeRectangle] = []

        for rectangle in self.free_rectangles:
            fragments = [rectangle]

            for other in resolved:
                next_fragments = []

                for fragment in fragments:
                    if self._intersect(fragment, other):
                        next_fragments.extend(self._split_overlap(fragment, other))
                    else:
                        next_fragments.append(fragment)

                fragments = next_fragments

            resolved.extend(fragment for fragment in fragments if fragment.area_mm2 > 0)

        self.free_rectangles = resolved

    def _split_overlap(
        self,
        rectangle: FreeRectangle,
        other: FreeRectangle,
    ) -> list[FreeRectangle]:
        if not self._intersect(rectangle, other):
            return [rectangle]

        rect_right = rectangle.x_mm + rectangle.length_mm
        rect_bottom = rectangle.y_mm + rectangle.width_mm
        other_right = other.x_mm + other.length_mm
        other_bottom = other.y_mm + other.width_mm

        overlap_left = max(rectangle.x_mm, other.x_mm)
        overlap_right = min(rect_right, other_right)

        fragments = []

        if other.x_mm > rectangle.x_mm:
            fragments.append(
                FreeRectangle(
                    rectangle.x_mm,
                    rectangle.y_mm,
                    other.x_mm - rectangle.x_mm,
                    rectangle.width_mm,
                )
            )

        if other_right < rect_right:
            fragments.append(
                FreeRectangle(
                    other_right,
                    rectangle.y_mm,
                    rect_right - other_right,
                    rectangle.width_mm,
                )
            )

        if other.y_mm > rectangle.y_mm:
            fragments.append(
                FreeRectangle(
                    overlap_left,
                    rectangle.y_mm,
                    overlap_right - overlap_left,
                    other.y_mm - rectangle.y_mm,
                )
            )

        if other_bottom < rect_bottom:
            fragments.append(
                FreeRectangle(
                    overlap_left,
                    other_bottom,
                    overlap_right - overlap_left,
                    rect_bottom - other_bottom,
                )
            )

        return [fragment for fragment in fragments if fragment.area_mm2 > 0]

    def _prune_free_rectangles(self) -> None:
        pruned = []

        for index, rectangle in enumerate(self.free_rectangles):
            contained = False

            for other_index, other in enumerate(self.free_rectangles):
                if index == other_index:
                    continue

                if self._contains(other, rectangle):
                    contained = True
                    break

            if not contained:
                pruned.append(rectangle)

        self.free_rectangles = pruned

    def _contains(
        self,
        outer: FreeRectangle,
        inner: FreeRectangle,
    ) -> bool:
        return (
            inner.x_mm >= outer.x_mm
            and inner.y_mm >= outer.y_mm
            and inner.x_mm + inner.length_mm <= outer.x_mm + outer.length_mm
            and inner.y_mm + inner.width_mm <= outer.y_mm + outer.width_mm
        )

    def _intersect(
        self,
        first: FreeRectangle,
        second: FreeRectangle,
    ) -> bool:
        return not (
            first.x_mm + first.length_mm <= second.x_mm
            or second.x_mm + second.length_mm <= first.x_mm
            or first.y_mm + first.width_mm <= second.y_mm
            or second.y_mm + second.width_mm <= first.y_mm
        )

    def _intersects(
        self,
        rectangle: FreeRectangle,
        used: MaxRectsPlacement,
    ) -> bool:
        return not (
            used.x_mm >= rectangle.x_mm + rectangle.length_mm
            or used.x_mm + used.length_mm <= rectangle.x_mm
            or used.y_mm >= rectangle.y_mm + rectangle.width_mm
            or used.y_mm + used.width_mm <= rectangle.y_mm
        )

    def _waste_area(self, placement: MaxRectsPlacement) -> float:
        container = next(
            rectangle
            for rectangle in self.free_rectangles
            if rectangle.x_mm == placement.x_mm and rectangle.y_mm == placement.y_mm
        )

        return container.area_mm2 - (placement.length_mm * placement.width_mm)
