import os
import tkinter as tk
from pynput import mouse

from components.input_range import InputRange
# 组件层
from components.radio import Radio
from components.switch_button import SwitchButton

# 业务层
from service.settings import Colors
from service.image_cache import ImageCache
from service.click_tracker import ClickTracker
from service.move_tracker import MoveTracker
from service.trackers import Trackers
# 通用工具层
from utils.get_screen_size import get_main_screen_size


def open_out_folder():
    """打开输出图片的位置"""
    os.startfile(os.path.dirname("./out"))


class App(tk.Tk):
    def __init__(self):
        super(App, self).__init__()

        # 配置ui信息
        self.title("Mouse Tracker")
        self.geometry("400x400")
        self.wm_iconbitmap('assert/favicon.ico')
        self.config(
            background='#2e3e26',
        )

        # 绑定数据信息
        self.imageCache = ImageCache(
            get_main_screen_size()
        )

        self.line_opacity_value = tk.IntVar(value=50)
        self.line_opacity = InputRange(
            '线条不透明度（实时）',
            variable=self.line_opacity_value,
            from_=1,
            to=100,
        )

        self.line_width_value = tk.IntVar(value=2)
        self.line_width = InputRange(
            '线条不透明度（实时）',
            variable=self.line_width_value,
            from_=1,
            to=25,
        )

        self.trackers = Trackers(
            click_trackers={
                mouse.Button.left: ClickTracker(cache=self.imageCache, color=Colors.Left),
                mouse.Button.right: ClickTracker(cache=self.imageCache, color=Colors.Right),
                mouse.Button.middle: ClickTracker(
                    cache=self.imageCache, color=Colors.Middle
                ),
            },
            move_tracker=MoveTracker(self.imageCache, self.line_opacity_value, self.line_width_value),
        )
        # 挂载组件
        self.radio_list = [
            Radio(self, text=text, variable=tracker)
            for text, tracker in zip(
                ["记录左键点击位置", "记录右键点击位置", "记录中键点击位置", "记录鼠标移动轨迹"],
                [*self.trackers.click_trackers.values(), self.trackers.move_tracker],
            )
        ]
        self.switch_button = SwitchButton(
            [self.start_tracking, self.stop_tracking],
            ['开始记录', '结束记录'],
        )
        self.open_out_files = SwitchButton(
            [open_out_folder], ['打开out文件夹']
        )

    def start_tracking(self):
        """点击开始记录"""
        self.trackers.reset()
        self.trackers.start()

    def stop_tracking(self):
        """点击结束记录"""
        self.imageCache.save()
        self.trackers.stop()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
