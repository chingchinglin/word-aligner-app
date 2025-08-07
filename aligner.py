# aligner.py

import spacy

# 1. 載入模型：若沒安裝就立刻報錯，避免後面 subprocess download 失敗
try:
    nlp = spacy.load("en_core_web_sm")
except OSError as e:
    raise RuntimeError(
        "❌ 找不到 spaCy 模型 en_core_web_sm。"
        " 請確認你的 requirements.txt 已包含：\n"
        "    en-core-web-sm @ "
        "https://github.com/explosion/spacy-models/"
        "releases/download/en_core_web_sm-3.7.1/"
        "en_core_web_sm-3.7.1.tar.gz\n"
        "然後重新部署後再執行。"
    ) from e

def find_match_indices(word: str, sentence: str):
    """
    基於 spaCy 斷詞與詞形還原，找出 word 在 sentence 中的 start/end 位置（以 token index 計）。
    若比對不到，回傳空 list，呼叫端可轉為「人工處理」。
    """
    doc = nlp(sentence)
    word_lower = word.lower()
    results = []

    for token in doc:
        # 比對 lemma 或原形
        if token.lemma_.lower() == word_lower:
            results.append((token.i + 1, token.i + 1))  # spaCy token.i 從 0 開始，+1 改成 1-based

    # 如果是 multi-token phrase，可額外擴充連續比對 (略)
    return results

# 如果你有多個 function，也通通放在這裡
# def another_helper(...):
#     ...

