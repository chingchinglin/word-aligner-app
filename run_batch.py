import re
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gemini_aligner import call_gemini_for_alignment

lemmatizer = WordNetLemmatizer()

def normalize(word):
    return lemmatizer.lemmatize(word.lower())

def tokenize(text):
    # 移除所有標點符號和所有格
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\b(\w+)s\b", r"\1", text)  # 簡單處理所有格 's
    return [normalize(w) for w in word_tokenize(text)]

def align_single_example(word_or_phrase, sentence, use_ai=True):
    phrase_tokens = tokenize(word_or_phrase)
    sentence_tokens = tokenize(sentence)

    phrase_len = len(phrase_tokens)

    for i in range(len(sentence_tokens) - phrase_len + 1):
        if sentence_tokens[i:i + phrase_len] == phrase_tokens:
            return i + 1, i + phrase_len, "對齊成功 ✅"

    # 詞形沒對上，自動轉 Gemini
    if use_ai:
        ai_result = call_gemini_for_alignment(word_or_phrase, sentence)
        if ai_result:
            return ai_result["start_index"], ai_result["end_index"], "AI補足 ✅"

    return "-", "-", "人工處理 🔧"

def run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=True):
    # 對基礎例句處理
    basic_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_basic], use_ai),
        axis=1
    )
    df["basic_start"] = basic_results.apply(lambda x: x[0])
    df["basic_end"] = basic_results.apply(lambda x: x[1])
    df["basic_status"] = basic_results.apply(lambda x: x[2])

    # 對進階例句處理
    adv_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_adv], use_ai),
        axis=1
    )
    df["adv_start"] = adv_results.apply(lambda x: x[0])
    df["adv_end"] = adv_results.apply(lambda x: x[1])
    df["adv_status"] = adv_results.apply(lambda x: x[2])

    # 合併欄位方便顯示
    df["index_combined"] = df["basic_start"].astype(str) + " / " + df["adv_start"].astype(str)
    df["match_form_combined"] = df["basic_end"].astype(str) + " / " + df["adv_end"].astype(str)
    df["status_combined"] = df["basic_status"] + " / " + df["adv_status"]

    return df
