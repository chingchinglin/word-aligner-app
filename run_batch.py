import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer

# 下載需要的 NLTK 資源
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# 正規化單字（詞形還原＋小寫）
def normalize(word):
    return lemmatizer.lemmatize(word.lower())

# 分詞（忽略標點符號與特殊字元）
def tokenize(text):
    # 先移除標點與特殊符號，只保留單字與空格
    text = re.sub(r"[^\w\s]", "", text)
    tokens = nltk.word_tokenize(text)
    return [normalize(w) for w in tokens]

# 對齊單一句子（word_or_phrase 是使用者輸入的單字／片語）
def align_single_example(word_or_phrase, text, use_ai=True):
    phrase_tokens = tokenize(word_or_phrase)
    sentence_tokens = tokenize(text)

    for i in range(len(sentence_tokens) - len(phrase_tokens) + 1):
        window = sentence_tokens[i : i + len(phrase_tokens)]
        if window == phrase_tokens:
            return i + 1, i + len(phrase_tokens), "精準對齊"

    if use_ai:
        return "-", "-", "AI補足"
    else:
        return "-", "-", "人工處理"

# 批次處理整個 DataFrame
def run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=True):
    basic_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_basic], use_ai),
        axis=1
    )
    adv_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_adv], use_ai),
        axis=1
    )

    df["basic_start"] = [r[0] for r in basic_results]
    df["basic_end"] = [r[1] for r in basic_results]
    df["status_basic"] = [r[2] for r in basic_results]

    df["adv_start"] = [r[0] for r in adv_results]
    df["adv_end"] = [r[1] for r in adv_results]
    df["status_adv"] = [r[2] for r in adv_results]

    # 整合欄位（方便在 Streamlit 顯示）
    df["index_combined"] = df.apply(
        lambda row: f"{row['basic_start']}~{row['basic_end']} / {row['adv_start']}~{row['adv_end']}",
        axis=1,
    )
    df["match_form_combined"] = df.apply(
        lambda row: f"{row[col_word]} → {row[col_basic]} / {row[col_adv]}",
        axis=1,
    )
    df["status_combined"] = df.apply(
        lambda row: f"{row['status_basic']} / {row['status_adv']}",
        axis=1,
    )

    return df
