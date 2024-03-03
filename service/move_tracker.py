import tkinter as tk

from service.image_cache import ImageCache


class MoveTracker(tk.BooleanVar):
    def __init__(self, cache: ImageCache):
        """A tracker that maintains a state of whether it should track or not"""
        super(MoveTracker, self).__init__(value=True)
        self.position = None
        self.cache = cache

    def track(self, x: int, y: int):
        if self.get():
            # print(f"move to ({x}, {y})")
            position = (x, y)
            if self.position:
                self.cache.line(start=self.position, end=position)
            self.position = position
