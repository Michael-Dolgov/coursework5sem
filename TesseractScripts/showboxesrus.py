import cv2
import pytesseract
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/' 
custom_config = r'--oem 1 --psm 3' 

input_folder = "rendered_latex"
output_text_folder = "rendered_latex_text"
output_boxes_folder = "rendered_latex_boxes"
os.makedirs(output_text_folder, exist_ok=True)
os.makedirs(output_boxes_folder, exist_ok=True)

langs = "eng+rus"

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_size = 20
font = ImageFont.truetype(font_path, font_size)

for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    img_path = os.path.join(input_folder, filename)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Не удалось открыть {img_path}")
        continue

    text = pytesseract.image_to_string(img, lang=langs, config=custom_config)
    out_text_path = os.path.join(output_text_folder, os.path.splitext(filename)[0] + ".txt")
    with open(out_text_path, "w", encoding="utf-8") as f:
        f.write(text)

    data = pytesseract.image_to_data(img, lang=langs, config=custom_config, output_type=pytesseract.Output.DICT)
    img_boxes = img.copy()

    img_pil = Image.fromarray(cv2.cvtColor(img_boxes, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 0:
            x, y, w_box, h_box = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            draw.rectangle([x, y, x + w_box, y + h_box], outline=(0, 255, 0), width=2)

            draw.text((x, y - font_size), data['text'][i], font=font, fill=(255, 0, 0))
    img_boxes = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    out_box_path = os.path.join(output_boxes_folder, filename)
    cv2.imwrite(out_box_path, img_boxes)

print('rdy')