import os
from pdf2image import convert_from_path

pdf_path = "sadik.pdf"

output_folder = "somedocs"
os.makedirs(output_folder, exist_ok=True)

pages = convert_from_path(pdf_path, dpi=300)

for i, page in enumerate(pages, start=1):
    output_path = os.path.join(output_folder, f"page_{i:03d}.png")
    page.save(output_path, "PNG")
    print(f"Сохранена страница {i} -> {output_path}")

print("Готово! Все страницы сохранены.")
