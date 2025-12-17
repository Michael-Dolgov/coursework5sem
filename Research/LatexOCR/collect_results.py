import cv2
import os
from PIL import Image
import tkinter
import matplotlib
import matplotlib.pyplot as plt
from pix2tex.cli import LatexOCR
import json

from metrics import marzal_vidal, bleu_score_str
from texmetric import texbleu

max_subset_size = 1000
ground_truth_index = {}

json_save_file = "results.json"
images_folder = 'latexdataset/generated_png_images'
formulas_listing_file = 'latexdataset/corresponding_png_images.txt'
ground_truth_file = 'latexdataset/final_png_formulas.txt'
recognized_save_file = 'recognizedLatexOCR.txt'

iteration = 0
with open(formulas_listing_file, 'r', encoding='utf-8') as \
    f_links, open(ground_truth_file, 'r', encoding='utf-8') as f_formulas:
    for link, formula in zip(f_links, f_formulas):
        if iteration >= max_subset_size:
            break
        ground_truth_index[link.strip()] = formula.strip()
        iteration += 1

print(len(ground_truth_index))

predictions_vidal = []
predictions_BLEU = []
predictions_TeXBLEU = []

json_results = []

model = LatexOCR()

print('=====Model Work=====')
with open(recognized_save_file, 'w', encoding='utf-8') as save_file:
    cnt = 0
    for filename in os.listdir(images_folder):
        if filename not in ground_truth_index:
            continue

        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            continue

        img_path = os.path.join(images_folder, filename)
        img = Image.open(img_path)
        if img is None:
            print(f"Не удалось открыть {img_path}")
            continue

        print(f'{cnt}/{max_subset_size} : {ground_truth_index[filename]}')

        recognized_one_line = model(img)
        gt = ground_truth_index[filename]

        vidal = marzal_vidal(gt, recognized_one_line)
        bleu = bleu_score_str(gt, recognized_one_line)
        texb = texbleu(gt, recognized_one_line)

        print(gt)
        print(recognized_one_line)
        print(f'vidal accuracy: {vidal}')
        print(f'BLEU score: {bleu}')
        print(f'TeXBLEU score: {texb}')

        predictions_vidal.append(vidal)
        predictions_BLEU.append(bleu)
        predictions_TeXBLEU.append(texb)

        json_results.append({
            "filename": filename,
            "ground_truth": gt,
            "recognized": recognized_one_line,
            "marzal_vidal_accuracy": vidal,
            "BLEU_accuracy": bleu,
            "TeXBLEU_accuracy": texb
        })

        cnt += 1

with open(json_save_file, "w", encoding="utf-8") as jf:
    json.dump(json_results, jf, ensure_ascii=False, indent=2)

print(f"JSON сохранён в {json_save_file}")

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
