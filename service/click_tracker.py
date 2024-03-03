import tkinter as tk

from service.image_cache import ImageCache
from service.types import Color


class ClickTracker(tk.BooleanVar):
    def __init__(self, cache: ImageCache, color: Color):
        """A tracker that maintains a state of whether it should track or not"""
        super(ClickTracker, self).__init__(value=True)
        self.color = color
        self.cache = cache

    def track(self, x: int, y: int):
        if self.get():
            # print(f"click at ({x}, {y})")
            self.cache.ellipse(x, y, color=self.color)
