import os

from PIL import Image, ImageDraw
import tkinter as tk
import datetime
from pynput import mouse


class Button(tk.Button):
    def __init__(self, *args, **kwarges):
        super(Button, self).__init__(*args, **kwarges)
        self.pack(pady=10)
        self['state'] = 'normal'

    def switch(self):
        self['state'] = 'disable' if self['state'] == 'normal' else 'normal'


class ImageCache(object):
    def __init__(self, size: tuple[int, int]):
        '''Image Cache'''
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

    def save(self, dirname='out', create_dir=True, clean=True):
        '''
        Save the image
        Parameters:
        - dirname: the child dir name relative to the python file's parent dir for output
        - create_dir: whether to try creating or not
        - clean: whether to clean the cache or not
        '''
        dir_path = os.path.join(os.path.dirname(__file__), dirname)
        if create_dir:
            os.makedirs(dir_path, exist_ok=True)
        elif not os.path.exists(dir_path):
            raise FileNotFoundError

        now = datetime.datetime.now()
        file_path = os.path.join(
            dir_path,
            f'mouse_track-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.png',
        )
        self.cache.save(file_path)

        if clean:
            self._refresh()
        print(f"轨迹图像已保存: {file_path}")

    def line(self, start, end):
        '''
        Draw a line
        Parameters:
        - start: tuple of the line's start
        - end: tuple of the line's end
        '''
        self._draw_transp_line(xy=[start, end], fill=(255, 255, 255, 50), width=2)

    def ellipse(self, x, y, color, radius=10):
        '''
        Draw a point at `(x, y)`
        '''
        self._draw_transp_ellipse(
            [(x - radius, y - radius), (x + radius, y + radius)],
            fill=color,
        )

    def _draw_transp_line(self, xy, **kwargs):
        '''Draws a line inside the given bounding box onto given image.
        Supports transparent colors
        '''
        transp = Image.new('RGBA', self._size, (0, 0, 0, 0))  # Temp drawing image.
        draw = ImageDraw.Draw(transp, "RGBA")
        draw.line(xy, **kwargs)
        # Alpha composite two images together and replace first with result.
        self._cache.paste(Image.alpha_composite(self._cache, transp))

    def _draw_transp_ellipse(self, xy, **kwargs):
        '''Draws an ellipse inside the given bounding box onto given image.
        Supports transparent colors
        https://stackoverflow.com/a/54426778
        '''
        transp = Image.new('RGBA', self._size, (0, 0, 0, 0))  # Temp drawing image.
        draw = ImageDraw.Draw(transp, "RGBA")
        draw.ellipse(xy, **kwargs)
        # Alpha composite two images together and replace first with result.
        self._cache.paste(Image.alpha_composite(self._cache, transp))


class Tracker(mouse.Listener):
    def __init__(self, size):
        '''Implemented by pynput.mouse
        This `mouse.Listener` will create a thread.
        '''
        super(Tracker, self).__init__(on_move=self.on_move, on_click=self.on_click)
        self.position = None  # (int(size[0] / 2), int(size[1] / 2))
        self.cache = ImageCache(size=size)

    def save(self):
        self.cache.save()  # This will clean the cache

    def on_move(self, x, y):
        # print(f'moving {x},{y};')
        position = (x, y)
        # WARNING remove this line if default set to mid of the screen for better perfomance
        if self.position:
            self.cache.line(start=self.position, end=position)
        self.position = position

    def on_click(self, x, y, button, pressed):
        if not pressed:
            return
        color = (
            0 if button == mouse.Button.left else 255,
            0 if button == mouse.Button.right else 255,
            0,
            100,
        )
        # print(f'click {x},{y}; {color}')
        self.cache.ellipse(x, y, color=color)


class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()
        self.window_size = (self.winfo_screenwidth(), self.winfo_screenheight())

        self.title("Mouse Tracker")

        self.start_button = Button(self, text="开始记录", command=self.start_tracking)

        self.stop_button = Button(self, text="停止记录", command=self.stop_tracking)
        self.stop_button.switch()

        self.tracker = Tracker(self.window_size)

    def start_tracking(self):
        """点击开始记录"""
        self.start_button.switch()
        self.stop_button.switch()
        self.tracker = Tracker(self.window_size)
        self.tracker.start()

    def stop_tracking(self):
        """点击结束记录"""
        self.stop_button.switch()
        self.start_button.switch()
        self.tracker.save()
        self.tracker.stop()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
