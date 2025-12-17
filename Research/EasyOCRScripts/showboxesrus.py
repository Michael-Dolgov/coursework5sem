import cv2
import easyocr
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

input_folder = "rendered_latex/selected"
output_text_folder = "results_txt_output"
output_boxes_folder = "results"
os.makedirs(output_text_folder, exist_ok=True)
os.makedirs(output_boxes_folder, exist_ok=True)

langs = ['en', 'ru']
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_size = 16
font = ImageFont.truetype(font_path, font_size)

reader = easyocr.Reader(langs, gpu=True)

for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    img_path = os.path.join(input_folder, filename)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Не удалось открыть {img_path}")
        continue

    result = reader.readtext(img_path)
    if not result:
        print(f"Текст не найден: {filename}")
        continue

    out_text_path = os.path.join(output_text_folder, os.path.splitext(filename)[0] + ".txt")
    with open(out_text_path, "w", encoding="utf-8") as f:
        for (bbox, text, conf) in result:
            f.write(f"{text} ({conf:.2f})\n")

    img_boxes = img.copy()
    img_pil = Image.fromarray(cv2.cvtColor(img_boxes, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    for (bbox, text, conf) in result:
        dot1, dot2, dot3, dot4 = bbox
        draw.line([dot1, dot2, dot3, dot4, dot1], fill=(0, 0, 255), width=2)
        draw.text((dot1[0], dot1[1] - font_size), 
                  str(text) + ' : ', font=font, fill=(255, 0, 0))

    img_boxes = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    out_box_path = os.path.join(output_boxes_folder, filename)
    cv2.imwrite(out_box_path, img_boxes)

print("rdy")
