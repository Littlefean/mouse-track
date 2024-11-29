from PIL import Image, ImageDraw
from screeninfo import get_monitors

def capture_screens_with_color_distinction():
    """
    获取多个屏幕图像并组合成一张图，用黑色作为背景，每个屏幕色块添加白色边框进行区分
    """
    screen_images = []
    total_width = 0
    max_height = 0
    monitors = get_monitors()
    if len(monitors)!= 2:
        raise ValueError("当前代码仅针对两个屏幕的情况进行颜色区分，实际检测到的屏幕数量不是2个。")

    for index, monitor in enumerate(monitors):
        screen_width = monitor.width
        screen_height = monitor.height

        total_width += screen_width
        max_height = max(max_height, screen_height)

        # 创建一个与屏幕分辨率相同的空白图像，模式为RGB，背景填充为黑色
        image = Image.new('RGB', (screen_width, screen_height), (0, 0, 0))

        # 创建一个ImageDraw对象，用于在图像上绘制边框
        draw = ImageDraw.Draw(image)

        # 白色边框的宽度（可根据需要调整）
        border_width = 1

        # 绘制白色边框，坐标计算是根据边框宽度和图像尺寸来确定四个边的位置
        draw.rectangle([(0, 0), (screen_width - 1, screen_height - 1)],
                       outline=(64, 64, 64), width=border_width)

        screen_images.append(image)

    # 创建一个新的空白图像，用于组合所有屏幕图像，大小为总宽度和最大高度，背景也填充为黑色
    combined_image = Image.new('RGB', (total_width, max_height), (0, 0, 0))
    x_offset = 0
    for screen_image in screen_images:
        combined_image.paste(screen_image, (x_offset, 0))
        x_offset += screen_image.width
    return combined_image

if __name__ == "__main__":
    combined_image = capture_screens_with_color_distinction()
    combined_image.save('combined_screens_with_color.png')