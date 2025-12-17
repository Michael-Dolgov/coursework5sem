for img in samples/*.png; do
    filename=$(basename "$img" .png)
    tesseract "$img" "results/$filename" -l eng+rus
done
