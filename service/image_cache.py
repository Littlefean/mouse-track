import datetime

import os

from PIL import Image, ImageDraw

from service.settings import Colors
from service.types import Position, Color, Size


class ImageCache(object):
    def __init__(self, size: Size):
        """Image Cache"""
        self._size = size
        self._refresh()

    @property
    def cache(self):
        return self._cache

    def _refresh(self):
        """
        将内部的绘制图片重置为一个纯黑色图片
        :return:
        """
        self._cache = Image.new(
            "RGBA",
            self._size,
            (0, 0, 0, 255),
        )

    def save(self, dir_path="out", create_dir=True, clean=True):
        """
        Save the image
        Parameters:
        - dir_path: the child dir name relative to 'main.py' parent dir for output
        - create_dir: whether to try creating or not
        - clean: whether to clean the cache or not
        """
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

    def line(self, start: Position, end: Position, color=Colors.Move):
        """
        Draw a line
        Parameters:
        - start: tuple of the line's start
        - end: tuple of the line's end
        """
        self._draw_transp_line(xy=[start, end], fill=color, width=2)

    def ellipse(self, x, y, color: Color, radius=10):
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
        """
        Draws a line inside the given bounding box onto given image.
        Supports transparent colors
        """
        transp = Image.new("RGBA", self._size, (0, 0, 0, 0))  # Temp drawing image.
        draw = ImageDraw.Draw(transp, "RGBA")
        draw.line(xy, **kwargs)
        # Alpha composite two images together and replace first with result.
        self._cache.paste(Image.alpha_composite(self._cache, transp))

    def _draw_transparent_ellipse(self, xy, **kwargs):
        """
        Draws an ellipse inside the given bounding box onto given image.
        Supports transparent colors
        https://stackoverflow.com/a/54426778
        """
        transp = Image.new("RGBA", self._size, (0, 0, 0, 0))  # Temp drawing image.
        draw = ImageDraw.Draw(transp, "RGBA")
        draw.ellipse(xy, **kwargs)
        # Alpha composite two images together and replace first with result.
        self._cache.paste(Image.alpha_composite(self._cache, transp))
