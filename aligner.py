import spacy
import pandas as pd

try:
    # 嘗試載入 spaCy 模型
    nlp = spacy.load("en_core_web_sm")
except OSError as e:
    raise RuntimeError("❗️spaCy 模型 'en_core_web_sm' 尚未安裝。請確認 requirements.txt 中有正確的 tar.gz 下載連結。") from e

def find_match_indices(word_or_phrase, sentence):
    """
    根據輸入的單字或片語，在句子中找到詞彙起始與結束的索引位置（從1開始計數）。
    若找不到，則回傳 -1, -1。
    """

    def normalize(text):
        return text.lower().replace("’s", "").replace("'s", "").replace("’", "").replace("'", "")

    # 預處理：標點符號與所有格處理
    exclude_tokens = {",", ".", "?", "!", ";", ":", "\"", "'", "(", ")", "[", "]", "{", "}", "-", "–", "—", "…"}
    doc = nlp(sentence)
    tokens = [token.text for token in doc if token.text not in exclude_tokens]

    # 詞彙還原
    lemma_tokens = [token.lemma_.lower() for token in doc if token.text not in exclude_tokens]
    lemma_target = [token.lemma_.lower() for token in nlp(word_or_phrase)]

    # 滑動視窗找片語
    for i in range(len(lemma_tokens) - len(lemma_target) + 1):
        window = lemma_tokens[i:i + len(lemma_target)]
        if window == lemma_target:
            start = i + 1  # 索引從1開始
            end = start + len(lemma_target) - 1
            return start, end

    return -1, -1  # 若找不到則回傳 -1
