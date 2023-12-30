import os

from PIL import Image, ImageDraw
import tkinter as tk
import datetime
from pynput import mouse


class Button(tk.Button):
    def __init__(self, *args, **kwarges):
        super(Button, self).__init__(*args, **kwarges)
        self.pack(pady=10)
        self["state"] = "normal"

    def switch(self):
        self["state"] = "disable" if self["state"] == "normal" else "normal"


class Checkbutton(tk.Checkbutton):
    def __init__(self, *args, **kwargs):
        super(Checkbutton, self).__init__(*args, **kwargs)
        self.pack(pady=2)


class ImageCache(object):
    def __init__(self, size: tuple[int, int]):
        """Image Cache"""
        self._size = size
        self._refresh()

    @property
    def cache(self):
        return self._cache

    def _refresh(self):
        self._cache = Image.new(
            "RGBA",
            self._size,
            (0, 0, 0, 255),
        )

    def save(self, dirname="out", create_dir=True, clean=True):
        """
        Save the image
        Parameters:
        - dirname: the child dir name relative to the python file's parent dir for output
        - create_dir: whether to try creating or not
        - clean: whether to clean the cache or not
        """
        dir_path = os.path.join(os.path.dirname(__file__), dirname)
        if create_dir:
            os.makedirs(dir_path, exist_ok=True)
        elif not os.path.exists(dir_path):
            raise FileNotFoundError

        now = datetime.datetime.now()
        file_path = os.path.join(
            dir_path,
            f"mouse_track-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.png",
        )
        self.cache.save(file_path)

        if clean:
            self._refresh()
        print(f"轨迹图像已保存: {file_path}")

    def line(self, start, end):
        """
        Draw a line
        Parameters:
        - start: tuple of the line's start
        - end: tuple of the line's end
        """
        self._draw_transp_line(xy=[start, end], fill=(255, 255, 255, 50), width=2)

    def ellipse(self, x, y, color: tuple[int, int, int, int], radius=10):
        """
        Draw a point at `(x, y)`
        :param x:
        :param y:
        :param color: 注意：有四个值，最后一个值的不透明度最大值是255，不是float的0~1
        :param radius:
        :return: None
        """
        self._draw_transparent_ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            fill=color,
        )

    def _draw_transp_line(self, xy, **kwargs):
        """Draws a line inside the given bounding box onto given image.
        Supports transparent colors
        """
        transp = Image.new("RGBA", self._size, (0, 0, 0, 0))  # Temp drawing image.
        draw = ImageDraw.Draw(transp, "RGBA")
        draw.line(xy, **kwargs)
        # Alpha composite two images together and replace first with result.
        self._cache.paste(Image.alpha_composite(self._cache, transp))

    def _draw_transparent_ellipse(self, xy, **kwargs):
        """Draws an ellipse inside the given bounding box onto given image.
        Supports transparent colors
        https://stackoverflow.com/a/54426778
        """
        transp = Image.new("RGBA", self._size, (0, 0, 0, 0))  # Temp drawing image.
        draw = ImageDraw.Draw(transp, "RGBA")
        draw.ellipse(xy, **kwargs)
        # Alpha composite two images together and replace first with result.
        self._cache.paste(Image.alpha_composite(self._cache, transp))


class Color:
    Green = (0, 255, 0, 100)
    Red = (255, 0, 0, 100)
    Yellow = (255, 255, 0, 100)


class MoveTracker(tk.BooleanVar):
    """A worker that maintains a state of whether it should do something or not"""

    def __init__(self, cache: ImageCache):
        super(MoveTracker, self).__init__(value=True)
        self.position = None
        self.cache = cache

    def __call__(self, position: tuple[int, int]):
        if self.get():
            print(f"move to ({position[0]}, {position[1]})")
            if self.position:
                self.cache.line(start=self.position, end=position)
            self.position = position


class ClickTracker(tk.BooleanVar):
    """A worker that maintains a state of whether it should do something or not"""

    def __init__(self, cache: ImageCache, color: tuple[int, int, int, int]):
        super(ClickTracker, self).__init__(value=True)
        self.color = color
        self.cache = cache

    def __call__(self, x: int, y: int):
        if self.get():
            print(f"click at ({x}, {y})")
            self.cache.ellipse(x, y, color=self.color)


class Trackers(mouse.Listener):
    def __init__(
        self,
        click_trackers: dict[mouse.Button, ClickTracker],
        move_tracker: MoveTracker,
    ):
        """Implemented by pynput.mouse
        This `mouse.Listener` will create a thread.
        """
        self.click_trackers = click_trackers
        self.move_tracker = move_tracker

    def reset(self):
        super(Trackers, self).__init__(on_move=self.on_move, on_click=self.on_click)

    def on_move(self, x, y):
        """
        鼠标移动的时触发
        :param x: ---->
        :param y: ↓
        :return: None
        """
        self.move_tracker(position=(x, y))

    def on_click(self, x, y, button, pressed):
        if pressed:
            # print(f'click {x},{y}; {color}')
            self.click_trackers[button](x, y)


class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        self.window_size = (self.winfo_screenwidth(), self.winfo_screenheight())

        self.title("Mouse Tracker")
        self.geometry("400x400")

        self.start_button = Button(self, text="开始记录", command=self.start_tracking)

        self.stop_button = Button(self, text="停止记录", command=self.stop_tracking)
        self.stop_button.switch()

        self.cache = ImageCache(size=self.window_size)

        self.trackers = Trackers(
            click_trackers={
                mouse.Button.left: ClickTracker(cache=self.cache, color=Color.Green),
                mouse.Button.right: ClickTracker(cache=self.cache, color=Color.Red),
                mouse.Button.middle: ClickTracker(cache=self.cache, color=Color.Yellow),
            },
            move_tracker=MoveTracker(self.cache),
        )

        Checkbutton(
            self,
            text="记录左键点击位置",
            variable=self.trackers.click_trackers[mouse.Button.left],
        )
        Checkbutton(
            self,
            text="记录右键点击位置",
            variable=self.trackers.click_trackers[mouse.Button.right],
        )
        Checkbutton(
            self,
            text="记录中键点击位置",
            variable=self.trackers.click_trackers[mouse.Button.middle],
        )
        Checkbutton(self, text="记录轨迹", variable=self.trackers.move_tracker)

    def start_tracking(self):
        """点击开始记录"""
        self.start_button.switch()
        self.stop_button.switch()
        self.trackers.reset()
        self.trackers.start()

    def stop_tracking(self):
        """点击结束记录"""
        self.stop_button.switch()
        self.start_button.switch()
        self.cache.save()
        self.trackers.stop()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
