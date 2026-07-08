"""Project model for BoardComposer Studio."""

from dataclasses import dataclass, field

from studio.models.board import StudioBoard
from studio.models.piece import StudioPiece
from studio.models.placement import StudioPlacement


@dataclass
class StudioProject:
    """In-memory project data used by BoardComposer Studio."""

    project_id: str
    name: str
    boards: list[StudioBoard] = field(default_factory=list)
    pieces: list[StudioPiece] = field(default_factory=list)
    placements: list[StudioPlacement] = field(default_factory=list)

    def piece_by_id(self, piece_id: str) -> StudioPiece:
        for piece in self.pieces:
            if piece.piece_id == piece_id:
                return piece
        raise KeyError(piece_id)

    def placement_by_piece_id(self, piece_id: str) -> StudioPlacement | None:
        for placement in self.placements:
            if placement.piece_id == piece_id:
                return placement
        return None
