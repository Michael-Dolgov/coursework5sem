import cv2
import os
import numpy as np

INPUT_DIR = "samples_processed"
KERNEL_SIZE = 2 

kernel = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".png"):
        path = os.path.join(INPUT_DIR, filename)
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None:
            continue
        eroded = cv2.erode(img, kernel, iterations=1)
        cv2.imwrite(path, eroded)
        print(f"Обработан {filename}")

print("Все изображения обработаны.")
