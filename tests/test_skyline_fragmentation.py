from boardcomposer.solver.skyline.node import SkylineNode
from boardcomposer.solver.skyline.skyline import Skyline


def test_prefers_less_fragmented_candidate():
    skyline = Skyline(width_mm=3000)
    skyline.nodes = [
        SkylineNode(0, 0, 1500),
        SkylineNode(1500, 0, 1500),
    ]

    candidate = skyline._candidate_from_node(
        index=0,
        width_mm=1000,
        height_mm=300,
        rotated=False,
    )

    assert candidate is not None
    assert candidate.fragmentation == 1
