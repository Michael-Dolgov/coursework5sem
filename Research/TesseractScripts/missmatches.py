def count_char_mismatches(file1, file2):
    with open(file1, 'r', encoding='utf-8') as f1:
        text1 = f1.read().replace('\n', '').strip()
    with open(file2, 'r', encoding='utf-8') as f2:
        text2 = f2.read().replace('\n', '').strip()

    max_len = max(len(text1), len(text2))
    text1 = text1.ljust(max_len).strip()
    text2 = text2.ljust(max_len).strip()

    mismatches = sum(c1 != c2 for c1, c2 in zip(text1, text2))
    mismatch_ratio = (mismatches / max_len) * 100 if max_len > 0 else 0
    
    print(f"Всего символов: {max_len}")
    print(f"Количество несовпадений: {mismatches}")
    print(f"Количество несовпадений символов: {mismatches}")
    return mismatches

count_char_mismatches("results_txt_output/page_001.txt", "results_txt_ground/page_001.txt")
