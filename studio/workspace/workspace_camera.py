from dataclasses import dataclass

from PySide6.QtCore import QPointF


@dataclass
class WorkspaceCamera:
    center: QPointF
    zoom: float = 1.0
    min_zoom: float = 0.15
    max_zoom: float = 8.0

    def clamp_zoom(self, value: float) -> float:
        return max(self.min_zoom, min(self.max_zoom, value))

    def zoom_factor(self, wheel_delta: int) -> float:
        return 1.12 if wheel_delta > 0 else 1 / 1.12
