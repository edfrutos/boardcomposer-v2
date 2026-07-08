from dataclasses import dataclass

from boardcomposer.solver.skyline.node import SkylineNode
from boardcomposer.solver.skyline.placement import SkylinePlacement


@dataclass(frozen=True)
class SkylineCandidate:
    x_mm: float
    y_mm: float
    width_mm: float
    height_mm: float
    waste_mm: float
    fragmentation: int
    rotated: bool = False


class Skyline:
    def __init__(self, width_mm: float = 3000.0) -> None:
        self.width_mm = width_mm
        self.nodes = [SkylineNode(x_mm=0.0, y_mm=0.0, width_mm=width_mm)]

    @property
    def height_mm(self) -> float:
        return max((node.y_mm for node in self.nodes), default=0.0)

    def find_position(self, width_mm: float) -> SkylinePlacement | None:
        candidate = self._find_best_candidate(width_mm, height_mm=0)

        if candidate is None:
            return None

        return SkylinePlacement(candidate.x_mm, candidate.y_mm, candidate.rotated)

    def place(
        self,
        width_mm: float,
        height_mm: float,
        allow_rotation: bool = False,
    ) -> SkylinePlacement | None:
        normal = self._find_best_candidate(width_mm, height_mm, rotated=False)
        rotated = (
            self._find_best_candidate(height_mm, width_mm, rotated=True)
            if allow_rotation
            else None
        )

        candidate = self._choose_candidate(normal, rotated)

        if candidate is None:
            return None

        x_start = candidate.x_mm
        x_end = x_start + candidate.width_mm
        y_top = candidate.y_mm + candidate.height_mm

        updated_nodes: list[SkylineNode] = []

        for node in self.nodes:
            node_start = node.x_mm
            node_end = node.x_mm + node.width_mm

            if node_end <= x_start or node_start >= x_end:
                updated_nodes.append(node)
                continue

            if node_start < x_start:
                updated_nodes.append(
                    SkylineNode(node_start, node.y_mm, x_start - node_start)
                )

            if node_end > x_end:
                updated_nodes.append(SkylineNode(x_end, node.y_mm, node_end - x_end))

        updated_nodes.append(
            SkylineNode(
                x_mm=x_start,
                y_mm=y_top,
                width_mm=candidate.width_mm,
            )
        )

        self.nodes = [node for node in updated_nodes if node.width_mm > 0]
        self.nodes.sort(key=lambda node: node.x_mm)
        self._merge_adjacent_nodes()

        return SkylinePlacement(
            x_mm=x_start,
            y_mm=candidate.y_mm,
            rotated=candidate.rotated,
        )

    def _find_best_candidate(
        self,
        width_mm: float,
        height_mm: float,
        rotated: bool = False,
    ) -> SkylineCandidate | None:
        candidates = []

        for index in range(len(self.nodes)):
            candidate = self._candidate_from_node(
                index=index,
                width_mm=width_mm,
                height_mm=height_mm,
                rotated=rotated,
            )

            if candidate is not None:
                candidates.append(candidate)

        return self._choose_candidate(*candidates)

    def _candidate_from_node(
        self,
        index: int,
        width_mm: float,
        height_mm: float,
        rotated: bool,
    ) -> SkylineCandidate | None:
        start = self.nodes[index]
        x_start = start.x_mm
        x_end = x_start + width_mm

        if x_end > self.width_mm:
            return None

        covered_width = 0.0
        max_y = start.y_mm
        covered_nodes = 0

        for node in self.nodes[index:]:
            covered_nodes += 1

            if node.x_mm > x_start + covered_width:
                return None

            max_y = max(max_y, node.y_mm)
            covered_width = (node.x_mm + node.width_mm) - x_start

            if covered_width >= width_mm:
                return SkylineCandidate(
                    x_mm=x_start,
                    y_mm=max_y,
                    width_mm=width_mm,
                    height_mm=height_mm,
                    waste_mm=covered_width - width_mm,
                    fragmentation=covered_nodes,
                    rotated=rotated,
                )

        return None

    def _choose_candidate(
        self,
        *candidates: SkylineCandidate | None,
    ) -> SkylineCandidate | None:
        valid = [candidate for candidate in candidates if candidate is not None]

        if not valid:
            return None

        return min(
            valid,
            key=lambda candidate: (
                candidate.y_mm + candidate.height_mm,
                candidate.fragmentation,
                candidate.y_mm,
                candidate.x_mm,
            ),
        )

    def _merge_adjacent_nodes(self) -> None:
        if not self.nodes:
            return

        merged = [self.nodes[0]]

        for node in self.nodes[1:]:
            last = merged[-1]

            if last.y_mm == node.y_mm and last.x_mm + last.width_mm == node.x_mm:
                merged[-1] = SkylineNode(
                    x_mm=last.x_mm,
                    y_mm=last.y_mm,
                    width_mm=last.width_mm + node.width_mm,
                )
            else:
                merged.append(node)

        self.nodes = merged
