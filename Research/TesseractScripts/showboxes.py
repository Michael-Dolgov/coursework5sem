import cv2
import pytesseract
import os
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/' 
custom_config = r'--oem 1' 

input_folder = "rendered_latex"
output_text_folder = "rendered_latex_text"
output_boxes_folder = "rendered_laetx_boxes"
os.makedirs(output_text_folder, exist_ok=True)
os.makedirs(output_boxes_folder, exist_ok=True)

langs = "eng+rus"

for filename in os.listdir(input_folder):
    if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
        continue

    img_path = os.path.join(input_folder, filename)
    img = cv2.imread(img_path)
    if img is None:
        print(f"Не удалось открыть {img_path}")
        continue

    h, w, _ = img.shape

    text = pytesseract.image_to_string(img, lang=langs)
    out_text_path = os.path.join(output_text_folder, os.path.splitext(filename)[0] + ".txt")
    with open(out_text_path, "w", encoding="utf-8") as f:
        f.write(text)

    data = pytesseract.image_to_data(img, lang=langs, config=custom_config, output_type=pytesseract.Output.DICT)
    img_boxes = img.copy()

    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 0:
            x, y, w_box, h_box = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cv2.rectangle(img_boxes, (x, y), (x + w_box, y + h_box), (0, 255, 0), 1)
            cv2.putText(img_boxes, data['text'][i], (x, y - 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

    out_box_path = os.path.join(output_boxes_folder, filename)
    cv2.imwrite(out_box_path, img_boxes)

print("Готово! Текст сохранён в 'results', изображения с box в 'results_boxes'")
