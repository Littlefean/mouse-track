import time
import tkinter as tk

from service.image_cache import ImageCache
import threading
from collections import deque


class MoveTracker(tk.BooleanVar):
    def __init__(self, cache: ImageCache, alpha_value: tk.IntVar, width_value: tk.IntVar):
        """A tracker that maintains a state of whether it should track or not"""
        super(MoveTracker, self).__init__(value=True)
        self.cache = cache
        self.alpha_value = alpha_value
        self.width_value = width_value
        # 线段缓存，用于存储鼠标移动的线段，在图像上绘制
        self.line_cache = deque()

        # 开启新线程
        self.render_timer = threading.Thread(target=self.render).start()

    def __del__(self):
        # 关闭定时器线程
        self.render_timer.join()
        pass

    def render(self):
        """渲染，清空缓存，将线段缓存绘制到图像上"""
        # 线程一旦开启就不再退出，等待主线程关闭
        while True:
            # 一旦队列中有元素，则渲染，直到队列只有一个点，表示鼠标不动
            while len(self.line_cache) > 1:
                start = self.line_cache.popleft()
                end = self.line_cache[0]
                self.cache.line(
                    start=start,
                    end=end,
                    color=(255, 255, 255, self.alpha_value.get()),
                    width=self.width_value.get()
                )

    def on_move(self, x: int, y: int):
        """鼠标移动监听事件函数"""
        if self.get():
            # 此处将在每次鼠标移动时调用，非常频繁，因此需要优化
            # 如果该点已经在缓存中最后一个元素，则不再重复添加
            if self.line_cache and self.line_cache[-1] == (x, y):
                return
            self.line_cache.append((x, y))
