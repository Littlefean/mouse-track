import pyautogui
from PIL import Image, ImageDraw
import tkinter as tk
from threading import Thread
import time


class MouseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Mouse Tracker")

        self.start_button = tk.Button(root, text="开始记录", command=self.start_tracking)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="停止记录", command=self.stop_tracking)
        self.stop_button.pack(pady=10)
        self.stop_button['state'] = 'disabled'

        self.points = []
        self.is_tracking = False

    def start_tracking(self):
        self.start_button['state'] = 'disabled'
        self.stop_button['state'] = 'normal'
        self.points = []
        self.is_tracking = True
        self.root.bind("<Button-1>", self.record_click)
        Thread(target=self.track_mouse).start()

    def stop_tracking(self):
        self.start_button['state'] = 'normal'
        self.stop_button['state'] = 'disabled'
        self.is_tracking = False
        self.root.unbind("<Button-1>")
        self.create_image()

    def track_mouse(self):
        while self.is_tracking:
            x, y = pyautogui.position()
            self.points.append((x, y))
            time.sleep(0.01)

    def record_click(self, event):
        x, y = pyautogui.position()
        self.points.append((x, y, 'red'))

    def create_image(self):
        image = Image.new("RGBA", (self.root.winfo_screenwidth(), self.root.winfo_screenheight()), (0, 0, 0, 255))

        for i in range(1, len(self.points)):
            temp_image = Image.new("RGBA", (self.root.winfo_screenwidth(), self.root.winfo_screenheight()),
                                   (0, 0, 0, 0))
            draw = ImageDraw.Draw(temp_image)

            x1, y1 = self.points[i - 1][:2]
            x2, y2 = self.points[i][:2]
            color = self.points[i][2] if len(self.points[i]) == 3 else (255, 255, 255, 50)  # 半透明白色
            draw.line([(x1, y1), (x2, y2)], fill=color, width=2)

            image = Image.alpha_composite(image.convert("RGBA"), temp_image)

        image = image.convert("RGB")
        image.save("mouse_track.png")
        print("轨迹图像已保存为 mouse_track.png")


if __name__ == "__main__":
    root = tk.Tk()
    tracker = MouseTracker(root)
    root.mainloop()
