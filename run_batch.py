from aligner import find_match_indices
from gemini_aligner import align_with_ai  # 如果啟用 Gemini 模式
import pandas as pd

def align_single_example(word_or_phrase, sentence, use_ai=False):
    start, end, match_form, status = find_match_indices(word_or_phrase, sentence)

    # 若 NLP 模組找不到，使用 Gemini 補齊
    if use_ai and status == "人工處理":
        ai_result = align_with_ai(word_or_phrase, sentence)
        if ai_result:
            start, end, match_form, status = ai_result

    return pd.Series([start, end, match_form, status])

def run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=False):
    # 對基礎句處理
    basic_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_basic], use_ai),
        axis=1
    )
    basic_results.columns = [
        "mark_start_basic", "mark_end_basic", "match_form_basic", "status_basic"
    ]

    # 對進階句處理
    adv_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_adv], use_ai),
        axis=1
    )
    adv_results.columns = [
        "mark_start_adv", "mark_end_adv", "match_form_adv", "status_adv"
    ]

    # 整合欄位
    df["index_combined"] = basic_results["mark_start_basic"].astype(str) + " / " + adv_results["mark_start_adv"].astype(str)
    df["match_form_combined"] = basic_results["match_form_basic"] + " / " + adv_results["match_form_adv"]
    df["status_combined"] = basic_results["status_basic"] + " / " + adv_results["status_adv"]

    return pd.concat([df, basic_results, adv_results], axis=1)
