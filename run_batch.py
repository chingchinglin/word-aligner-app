import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer

# ⛑️ 自動下載需要的資源（避免 LookupError）
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

try:
    nltk.data.find('corpora/omw-1.4')
except LookupError:
    nltk.download('omw-1.4')

lemmatizer = WordNetLemmatizer()

# ✅ 文本標準化（去除標點、還原詞形）
def normalize(word):
    return lemmatizer.lemmatize(word.lower())

# ✅ 分詞並標準化（不含標點）
def tokenize(text):
    return [normalize(w) for w in nltk.word_tokenize(re.sub(r"[^\w\s]", "", text))]

# ✅ 比對邏輯（找出 word_or_phrase 在 sentence 中的位置）
def align_single_example(word_or_phrase, sentence, use_ai=False):
    phrase_tokens = tokenize(word_or_phrase)
    sentence_tokens = tokenize(sentence)

    for i in range(len(sentence_tokens) - len(phrase_tokens) + 1):
        window = sentence_tokens[i:i + len(phrase_tokens)]
        if window == phrase_tokens:
            return i + 1, i + len(phrase_tokens), "匹配 ✅"

    if use_ai:
        return "-", "-", "AI補足"
    else:
        return "-", "-", "人工處理"

# ✅ 批次處理函數
def run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=False):
    # 基礎例句對齊
    basic_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_basic], use_ai),
        axis=1
    )
    df["basic_start"] = basic_results.apply(lambda x: x[0])
    df["basic_end"] = basic_results.apply(lambda x: x[1])
    df["basic_status"] = basic_results.apply(lambda x: x[2])

    # 進階例句對齊
    adv_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_adv], use_ai),
        axis=1
    )
    df["adv_start"] = adv_results.apply(lambda x: x[0])
    df["adv_end"] = adv_results.apply(lambda x: x[1])
    df["adv_status"] = adv_results.apply(lambda x: x[2])

    # 合併顯示欄位
    df["index_combined"] = df["basic_start"].astype(str) + "~" + df["basic_end"].astype(str) + " / " + df["adv_start"].astype(str) + "~" + df["adv_end"].astype(str)
    df["match_form_combined"] = df["basic_status"] + " / " + df["adv_status"]
    df["status_combined"] = df.apply(lambda row: "✅" if "人工處理" not in row["match_form_combined"] else "🔧", axis=1)

    df["word_or_phrase"] = df[col_word]
    return df
