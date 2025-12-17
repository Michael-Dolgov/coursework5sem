import cv2
import os
import pytesseract
import json
from metrics import marzal_vidal, bleu_score_str
from texmetric import texbleu
from matplotlib import pyplot as plt

# ===== Настройки Tesseract =====
os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/' 
custom_config = r'--oem 1'
langs = "eng+rus"

# ===== Переменные =====
max_subset_size = 1000
ground_truth_index = {}

json_save_file = "results.json"
images_folder = 'latexdataset/generated_png_images'
formulas_listing_file = 'latexdataset/corresponding_png_images.txt'
ground_truth_file = 'latexdataset/final_png_formulas.txt'
recognized_save_file = 'recognizedLatexOCR.txt'
output_text_folder = "results"
output_boxes_folder = "results_boxes"
os.makedirs(output_text_folder, exist_ok=True)

os.makedirs(output_boxes_folder, exist_ok=True)

# ===== Загрузка ground truth =====
iteration = 0
with open(ground_truth_file, 'r', encoding='utf-8') as f:
    for line in f:
        if iteration >= max_subset_size:
            break
        parts = line.strip().split('\t')
        if len(parts) != 2:
            continue
        filename, formula = parts
        ground_truth_index[filename] = formula
        iteration += 1

print(f"Всего изображений для обработки: {len(ground_truth_index)}")

# ===== Списки для метрик =====
predictions_vidal = []
predictions_BLEU = []
predictions_TeXBLEU = []
json_results = []

# ===== Работа модели Tesseract =====
with open(recognized_save_file, 'w', encoding='utf-8') as save_file:
    cnt = 0
    for filename in os.listdir(images_folder):
        if filename not in ground_truth_index:
            continue
        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        img_path = os.path.join(images_folder, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Не удалось открыть {img_path}")
            continue

        print(f'{cnt}/{max_subset_size} : {ground_truth_index[filename]}')

        # Распознавание текста
        recognized_text = pytesseract.image_to_string(img, lang=langs, config=custom_config)
        save_file.write(f"{filename}\t{recognized_text}\n")

        # Рисуем bounding boxes
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

        # Вычисление метрик
        gt = ground_truth_index[filename]
        vidal = marzal_vidal(gt, recognized_text)
        bleu = bleu_score_str(gt, recognized_text)
        texb = texbleu(gt, recognized_text)

        print(gt)
        print(recognized_text)
        print(f'Marzal-Vidal: {vidal}, BLEU: {bleu}, TeXBLEU: {texb}')

        predictions_vidal.append(vidal)
        predictions_BLEU.append(bleu)
        predictions_TeXBLEU.append(texb)

        json_results.append({
            "filename": filename,
            "ground_truth": gt,
            "recognized": recognized_text,
            "marzal_vidal_accuracy": vidal,
            "BLEU_accuracy": bleu,
            "TeXBLEU_accuracy": texb
        })

        cnt += 1
# ---- гистограммы ----
plt.hist(predictions_vidal, 100, color='skyblue', edgecolor='black')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.title('Распределение значений по Marzal-Vidal')
plt.savefig("TexTeller_latex_vidal.png")

plt.hist(predictions_BLEU, 100, color='skyblue', edgecolor='black')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.title('Распределение значений по BLEU')
plt.savefig("TexTeller_latex_BLEU.png")

plt.hist(predictions_TeXBLEU, 100, color='skyblue', edgecolor='black')
plt.xlabel('Значение')
plt.ylabel('Частота')
plt.title('Распределение значений по TEXBLEU')
plt.savefig("TexTeller_latex_TeXBLEU.png")

print('rdy')

# ===== Сохраняем JSON =====
with open(json_save_file, "w", encoding="utf-8") as jf:
    json.dump(json_results, jf, ensure_ascii=False, indent=2)

print(f"JSON с результатами сохранён в {json_save_file}")
print(f"Все распознанные строки сохранены в {recognized_save_file}")
print("Готово!")
