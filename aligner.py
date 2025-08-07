# aligner.py

import spacy

# -----------------------------------------------------------------------------
# 1. 載入 spaCy 模型（請務必透過 requirements.txt 事先安裝 en-core-web-sm）
# -----------------------------------------------------------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError as e:
    raise RuntimeError(
        "❌ 找不到 spaCy 模型 en_core_web_sm！\n"
        "請確認 requirements.txt 已包含：\n"
        "    en-core-web-sm @ "
        "https://github.com/explosion/spacy-models/"
        "releases/download/en_core_web_sm-3.7.1/"
        "en_core_web_sm-3.7.1.tar.gz\n"
        "然後重新部署。"
    ) from e

# -----------------------------------------------------------------------------
# 2. 定義 find_match_indices(word, sentence)
#    回傳 (start, end, match_form, status)
#    - start/end: 1-based token index
#    - match_form: spaCy 抓到的原文切片
#    - status: "NLP" 或 "人工處理"
# -----------------------------------------------------------------------------
def find_match_indices(word: str, sentence: str):
    """
    找出 word_or_phrase 在 sentence 中的起訖索引（1-based），
    若找不到就回 ("", "", "", "人工處理")。
    """
    doc = nlp(sentence)
    word_lower = word.lower().strip()
    tokens = [token for token in doc]

    # ---- 1) 詞形還原單字匹配 ----
    for token in tokens:
        if token.lemma_.lower() == word_lower or token.text.lower() == word_lower:
            start = token.i + 1
            end = start
            return start, end, token.text, "NLP"

    # ---- 2) 片語連續匹配 ----
    phrase = word_lower.split()
    length = len(phrase)
    for i in range(len(tokens) - length + 1):
        lemmas = [tk.lemma_.lower() for tk in tokens[i : i + length]]
        if lemmas == phrase:
            start = i + 1
            end = i + length
            match_form = " ".join([tk.text for tk in tokens[i : i + length]])
            return start, end, match_form, "NLP"

    # ---- 3) 都找不到，回傳人工處理 ----
    return "", "", "", "人工處理"
