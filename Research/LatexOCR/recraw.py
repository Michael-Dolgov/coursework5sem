import cv2
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pix2tex.cli import LatexOCR

input_folder = "samples_raw"
recognized_file = "recognized_raw.txt"

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_size = 16
font = ImageFont.truetype(font_path, font_size)

model = LatexOCR()

print('=====Model Work=====')
with open(recognized_file, 'w', encoding='utf-8') as save_file:
    cnt = 0
    for filename in os.listdir(input_folder):
        print(filename)
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)
        if img is None:
            print(f"Не удалось открыть {img_path}")
            continue

        recognized = model(img)
        save_file.write(recognized)
        save_file.write('\n')

print('rdy')