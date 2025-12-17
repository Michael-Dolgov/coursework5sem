import cv2
import os

INPUT_DIR = "samples_processed"
OUTPUT_DIR = "rotated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

ROTATION_ANGLE = int(input("rotation angle: "))

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".png"):
        input_path = os.path.join(INPUT_DIR, filename)
        img = cv2.imread(input_path)
        if img is None:
            continue

        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)

        M = cv2.getRotationMatrix2D(center, ROTATION_ANGLE, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))

        output_path = os.path.join(OUTPUT_DIR, filename)
        cv2.imwrite(output_path, rotated)
        print(f"Вращено {filename}")

print("Все изображения обработаны и сохранены в папку 'rotated'.")
