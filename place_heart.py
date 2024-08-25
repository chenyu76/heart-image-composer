#!/bin/python
from PIL import Image
import os
import random

# 可配置参数，长度单位均为像素
image_length = 50  # 放置到画布的图片长
image_width = 30   # 放置到画布的图片宽
canvas_length = 1200  # 画布长
canvas_width = 800   # 画布宽
margin = 3          # 边距
y_offset = 20  # y轴偏移
x_offset = 0   # x轴偏移
folder_path = "./example/input"  # 指定文件夹
background_image_path = "./example/bg.png"  # 指定的背景图
export_path = "./example/out.png" # 导出图片到另一个指定文件夹

# 返回点(x, y)是否在心形曲线内
def is_inside_curve(x, y):
    # Parameters controlling the size of the heart
    A, B = 300, 300  # 曲线参数，控制心形大小
    return ((x/A)**2 + (-y/B)**2 - 1)**3 - ((x/A)**2) * ((-y/B)**3) <= 0

def get_folder_images():
    return [Image.open(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if True ]#file.endswith(('png', 'jpg', 'jpeg'))]

def place_images():
    # 计数器
    images_num = 0
    need_images = 0
    reuse_times = 0

    print("开始读取指定文件夹中的图片...")
    # 读取指定文件夹中的所有图片
    images = get_folder_images()
    print(f"共读取到 {len(images)} 张图片。")
    images_num = len(images)

    # 确定放置图片的点
    print("计算放置图片的点...")
    points = []
    step_x = image_length + margin
    step_y = image_width + margin
    # 计算遍历的起始点，确保包括 (0, 0)
    start_x = -(canvas_length // 2) + (canvas_length // 2) % step_x
    start_y = -(canvas_width // 2) + (canvas_width // 2) % step_y
    # 在画布上放置图片
    print("开始在画布上放置图片...")
    for x in range(start_x, canvas_length//2, step_x):
        for y in range(start_y, canvas_width//2, step_y):
            if is_inside_curve(x, y):
                points.append((x, y))
                print(f"点({x},{y})已添加 ")
    
    print(f"共计算出 {len(points)} 个点用于放置图片。")
    need_images = len(points)

    # 创建新画布并填充背景
    print("创建新画布并填充背景图...")
    canvas = Image.new('RGB', (canvas_length, canvas_width), "white")
    if background_image_path:
        background = Image.open(background_image_path)
        background = background.resize((canvas_length, canvas_width))
        canvas.paste(background, (0, 0))

    # 在画布上放置图片
    print("开始在画布上放置图片...")
    for point in points:
        if not images:
            print("已使用所有图片，重新使用已有图片。")
            images = get_folder_images()
            reuse_times += 1
        img = random.choice(images)
        images.remove(img)
        print(f"放置{img} 在 ({point[0]},{point[1]})...")
        img = img.resize((image_length, image_width))

        # 处理透明度（如果图片是PNG）
        if img.mode in ("RGBA", "LA") or (img.mode == 'P' and 'transparency' in img.info):
            alpha = img.convert('RGBA').split()[-1]
            bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
            bg.paste(img, mask=alpha)
            img = bg.convert('RGB')

        canvas.paste(img, (x_offset + point[0] + canvas_length//2 - image_length//2, y_offset + point[1] + canvas_width//2 - image_width//2))
    print("图片放置完成。")

    export_folder = os.path.dirname(export_path)
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    canvas.save(export_path)
    print(f"图片导出完成，保存路径：{export_path}")
    print(f'---\n使用{images_num}张图片，填充{need_images}个点，图片复用{reuse_times}次')

# 执行程序
place_images()
