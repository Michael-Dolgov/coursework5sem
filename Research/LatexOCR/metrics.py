import nltk
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.tokenize import word_tokenize

def levenstein(str_1, str_2):
    n, m = len(str_1), len(str_2)
    if n > m:
        str_1, str_2 = str_2, str_1
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + 1, \
                current_row[j - 1] + 1, previous_row[j - 1]
            if str_1[j - 1] != str_2[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]

def marzal_vidal(reference, prediction):
    reference = str(reference)
    prediction = str(prediction)

    n, m = len(reference), len(prediction)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if reference[i - 1] == prediction[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    distance = dp[n][m]
    path_len = max(n, m)

    normalized = distance / path_len if path_len != 0 else 0.0

    return normalized

def bleu_score_str(reference, prediction):
    nltk.download('punkt_tab', quiet=True)
    if isinstance(reference, str):
        refs = [reference]
    else:
        refs = list(reference)

    ref_tokens = [word_tokenize(r) for r in refs]
    hyp_tokens = word_tokenize(prediction)

    if len(hyp_tokens) == 0 or any(len(r) == 0 for r in ref_tokens):
        return 0.0

    sf = SmoothingFunction()

    score = sentence_bleu(ref_tokens, hyp_tokens, smoothing_function=sf.method1)

    return score