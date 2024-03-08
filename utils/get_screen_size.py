"""
此模块仅用于获取屏幕设备大小

在App中 size=(self.winfo_screenwidth(), self.winfo_screenheight())
这样的方法获取到的屏幕尺寸大小有问题。win11，机械革命电脑，分辨率超过1080p，屏幕缩放倍数150%
"""
from PIL import ImageGrab
from functools import lru_cache

from service.types import Size


@lru_cache(1)
def get_main_screen_size() -> Size:
    """
    获取主屏幕的大小
    """
    return ImageGrab.grab().size

# 以后如果涉及多屏幕显示器
# 获取其中任意一个等方法
# 还可以继续在这里添加函数
