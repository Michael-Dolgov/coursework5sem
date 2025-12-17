import cv2
import os

INPUT_DIR = "samples_processed"
KERNEL_SIZE = 3

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".png"):
        path = os.path.join(INPUT_DIR, filename)
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
        blurred = cv2.GaussianBlur(img, (KERNEL_SIZE, KERNEL_SIZE), 0)
        cv2.imwrite(path, blurred)
        print(f"Обработан {filename}")

print("Все изображения обработаны.")
