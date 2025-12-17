import cv2
import os

INPUT_DIR = "samples_processed"
THRESHOLD_VALUE = 127 
MAX_VALUE = 255 

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith(".png"):
        path = os.path.join(INPUT_DIR, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        _, binary = cv2.threshold(img, THRESHOLD_VALUE, MAX_VALUE, cv2.THRESH_BINARY)
        cv2.imwrite(path, binary)
        print(f"Обработан {filename}")

print("Все изображения обработаны.")
