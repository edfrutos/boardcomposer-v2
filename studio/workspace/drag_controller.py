class DragController:
    def __init__(self):
        self.drag_start = None

    def begin(self, piece_id, x, y):
        self.drag_start = (piece_id, x, y)

    def clear(self):
        value = self.drag_start
        self.drag_start = None
        return value
