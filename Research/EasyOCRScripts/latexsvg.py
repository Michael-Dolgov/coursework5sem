import os
import matplotlib.pyplot as plt

plt.rcParams['text.usetex'] = True 

INPUT_FILE = "latex_samples.txt"
SAVE_DIR = "rendered_latex"
IMG_DPI = 300

os.makedirs(SAVE_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    formulas = [line.strip() for line in f if line.strip()]

for i, formula in enumerate(formulas, start=1):
    fig, ax = plt.subplots(figsize=(2, 1))
    ax.text(0.5, 0.5, f"${formula}$", fontsize=20, ha="center", va="center")
    ax.axis("off")

    output_path = os.path.join(SAVE_DIR, f"{i:03d}.png")
    plt.savefig(output_path, dpi=IMG_DPI, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)

    print(f"Сохранено: {output_path}")
print("end")
