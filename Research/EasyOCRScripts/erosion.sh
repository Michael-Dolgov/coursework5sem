#!/bin/bash

INPUT_DIR="samples_processed"
KERNEL_SIZE=10

for file in "$INPUT_DIR"/*.png; do
    magick "$file" -morphology Erode "Disk:$KERNEL_SIZE" "$file"
    echo "Обработан $file"
done

echo "Все изображения обработаны."
