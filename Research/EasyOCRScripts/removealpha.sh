#!/bin/bash

INPUT_DIR="samples_raw"
OUTPUT_DIR="samples_processed"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.png; do
    filename=$(basename "$file")
    output_file="$OUTPUT_DIR/$filename"
    magick "$file" -alpha off "$output_file"
    echo "Обработан $filename"
done

echo "Все изображения обработаны."
