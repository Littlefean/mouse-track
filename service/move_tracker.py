import tkinter as tk

from service.image_cache import ImageCache


class MoveTracker(tk.BooleanVar):
    def __init__(self, cache: ImageCache, alpha_value: tk.IntVar, width_value: tk.IntVar):
        """A tracker that maintains a state of whether it should track or not"""
        super(MoveTracker, self).__init__(value=True)
        self.position = None
        self.cache = cache
        self.alpha_value = alpha_value
        self.width_value = width_value

    def track(self, x: int, y: int):
        if self.get():
            # print(f"move to ({x}, {y})")
            position = (x, y)
            if self.position:
                # self.cache.line(start=self.position, end=position, color=(255, 255, 255, 50))
                self.cache.line(
                    start=self.position,
                    end=position,
                    color=(255, 255, 255, self.alpha_value.get()),
                    width=self.width_value.get()
                )
            self.position = position
