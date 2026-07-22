import math
import time
import pandas as pd
from collections import Counter
from preprocessing import tokenize_text

def get_ngrams(tokens, n):
    if len(tokens) < n:
        return []
    return [tuple(tokens[i:i+n]) for i in range(len(tokens) - n + 1)]

def calculate_rouge_n(candidate_tokens, reference_tokens, n=1):
    cand_ngrams = get_ngrams(candidate_tokens, n)
    ref_ngrams = get_ngrams(reference_tokens, n)

    if not ref_ngrams or not cand_ngrams:
        return 0.0

    cand_counts = Counter(cand_ngrams)
    ref_counts = Counter(ref_ngrams)

    overlap = 0
    for ngram, count in cand_counts.items():
        if ngram in ref_counts:
            overlap += min(count, ref_counts[ngram])

    recall = overlap / len(ref_ngrams)
    precision = overlap / len(cand_ngrams)

    if recall + precision == 0:
        return 0.0

    f1 = (2 * precision * recall) / (precision + recall)
    return round(f1 * 100, 2)

def calculate_lcs(x, y):
    m, n = len(x), len(y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if x[i] == y[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])
    return dp[m][n]

def calculate_rouge_l(candidate_tokens, reference_tokens):
    if not candidate_tokens or not reference_tokens:
        return 0.0
    lcs_len = calculate_lcs(candidate_tokens, reference_tokens)
    recall = lcs_len / len(reference_tokens)
    precision = lcs_len / len(candidate_tokens)
    if recall + precision == 0:
        return 0.0
    f1 = (2 * precision * recall) / (precision + recall)
    return round(f1 * 100, 2)

def calculate_bleu(candidate_tokens, reference_tokens, max_n=4):
    if not candidate_tokens or not reference_tokens:
        return 0.0

    c_len = len(candidate_tokens)
    r_len = len(reference_tokens)

    if c_len == 0:
        return 0.0

    if c_len > r_len:
        bp = 1.0
    else:
        bp = math.exp(1 - (r_len / c_len))

    log_sum = 0.0
    weights = 1.0 / max_n

    for n in range(1, max_n + 1):
        cand_ngrams = get_ngrams(candidate_tokens, n)
        ref_ngrams = get_ngrams(reference_tokens, n)

        if not cand_ngrams or not ref_ngrams:
            pn = 1e-9
        else:
            cand_counts = Counter(cand_ngrams)
            ref_counts = Counter(ref_ngrams)
            overlap = sum(min(count, ref_counts[ngram]) for ngram, count in cand_counts.items())
            pn = overlap / len(cand_ngrams) if len(cand_ngrams) > 0 else 1e-9

        if pn == 0:
            pn = 1e-9
        log_sum += weights * math.log(pn)

    bleu = bp * math.exp(log_sum)
    return round(bleu * 100, 2)

def evaluate_summary(generated_summary, reference_summary):
    cand_tokens = tokenize_text(generated_summary)
    ref_tokens = tokenize_text(reference_summary)

    r1 = calculate_rouge_n(cand_tokens, ref_tokens, n=1)
    r2 = calculate_rouge_n(cand_tokens, ref_tokens, n=2)
    rl = calculate_rouge_l(cand_tokens, ref_tokens)
    bleu = calculate_bleu(cand_tokens, ref_tokens)

    return {
        "rouge_1": r1,
        "rouge_2": r2,
        "rouge_l": rl,
        "bleu": bleu,
        "summary_length": len(cand_tokens)
    }

def run_dataset_evaluation(dataset_path, summarizer_instance):
    df = pd.read_csv(dataset_path)
    results = []

    total_r1 = 0.0
    total_r2 = 0.0
    total_rl = 0.0
    total_bleu = 0.0
    total_time = 0.0
    total_length = 0

    for idx, row in df.iterrows():
        text = row['text']
        ref = row['reference_summary']
        title = row.get('title', f"Berita #{idx+1}")

        res = summarizer_instance.summarize(text)
        gen_summary = res['summary']
        inf_time = res['inference_time']

        eval_res = evaluate_summary(gen_summary, ref)

        total_r1 += eval_res['rouge_1']
        total_r2 += eval_res['rouge_2']
        total_rl += eval_res['rouge_l']
        total_bleu += eval_res['bleu']
        total_time += inf_time
        total_length += eval_res['summary_length']

        results.append({
            "id": idx + 1,
            "title": title,
            "original_text": text,
            "reference_summary": ref,
            "generated_summary": gen_summary,
            "rouge_1": eval_res['rouge_1'],
            "rouge_2": eval_res['rouge_2'],
            "rouge_l": eval_res['rouge_l'],
            "bleu": eval_res['bleu'],
            "inference_time": inf_time,
            "summary_length": eval_res['summary_length']
        })

    count = len(df) if len(df) > 0 else 1

    summary_metrics = {
        "rouge_1": round(total_r1 / count, 2),
        "rouge_2": round(total_r2 / count, 2),
        "rouge_l": round(total_rl / count, 2),
        "bleu": round(total_bleu / count, 2),
        "avg_inference_time": round(total_time / count, 4),
        "avg_summary_length": round(total_length / count, 1)
    }

    return {
        "metrics": summary_metrics,
        "dataset_results": results
    }
