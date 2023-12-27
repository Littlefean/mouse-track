import os

from PIL import Image, ImageDraw
import tkinter as tk
from threading import Thread
import datetime
from pynput import mouse


class MouseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Tracker")

        self.start_button = tk.Button(root, text="开始记录", command=self.start_tracking)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="停止记录", command=self.stop_tracking)
        self.stop_button.pack(pady=10)
        self.stop_button['state'] = 'disabled'

        self.image = Image.new(
            "RGBA",
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
            (0, 0, 0, 255)
        )
        self.current_location = {"x": -1, "y": -1}
        # 当前是否正在记录
        self.is_tracking = False
        # 创建鼠标监听器
        self.mouse_listener = mouse.Listener(on_click=self.on_click)

        self.mouse_listener.start()

    def start_tracking(self):
        """点击开始记录"""
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
        self.is_tracking = True
        # self.root.bind("<Button-1>", self.record_click)
        Thread(target=self.track_mouse).start()
        # 启动鼠标监听器

    def stop_tracking(self):
        """点击结束记录"""
        self.stop_button['state'] = 'disabled'
        self.create_image()
        # self.mouse_listener.stop()
        self.start_button['state'] = 'normal'
        self.is_tracking = False
        self.root.unbind("<Button-1>")
        # 停止鼠标监听器

    def clear_img(self):
        """清除原有的图像层"""
        self.image = Image.new(
            "RGBA",
            (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
            (0, 0, 0, 255)
        )

    def track_mouse(self):
        """开始记录后，此函数将开启另一个线程执行"""
        mouse_controller = mouse.Controller()
        while self.is_tracking:

            x1, y1 = self.current_location["x"], self.current_location["y"]
            # 获取新坐标
            x2, y2 = mouse_controller.position
            # 连线
            if not (x1 == -1 and y1 == -1):
                temp_image = Image.new(
                    "RGBA",
                    (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
                    (0, 0, 0, 0)
                )
                draw = ImageDraw.Draw(temp_image)
                draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 50), width=2)
                self.image = Image.alpha_composite(self.image.convert("RGBA"), temp_image)
            # 迭代更新坐标
            self.current_location = {"x": x2, "y": y2}

            pass
        pass

    def on_click(self, x, y, button, pressed):
        """鼠标点击事件回调函数"""
        mouse_controller = mouse.Controller()
        x, y = mouse_controller.position  # 解决坐标不一致的问题
        if pressed:
            print(x, y)
            color = (0, 255, 0)  # 默认为绿色
            if button == mouse.Button.right:
                color = (255, 0, 0)  # 右键为红色
            elif button == mouse.Button.middle:
                color = (255, 255, 0)  # 中键为黄色
            radius = 10

            temp_image = Image.new(
                "RGBA",
                (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
                (0, 0, 0, 0)
            )
            draw = ImageDraw.Draw(temp_image)
            draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=color + (100,))
            self.image = Image.alpha_composite(self.image.convert("RGBA"), temp_image)

    def create_image(self):
        now = datetime.datetime.now()
        if not (os.path.exists("out") and os.path.isdir("out")):
            os.makedirs("out")
        self.image.save(f"out/mouse_track-{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.png")
        print("轨迹图像已保存")
        self.clear_img()

        pass


def main():
    root = tk.Tk()
    MouseTracker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
