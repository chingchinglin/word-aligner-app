import spacy
import pandas as pd
import re

try:
    nlp = spacy.load("en_core_web_sm")
except OSError as e:
    raise RuntimeError(
        "spaCy 模型 'en_core_web_sm' 尚未安裝。請確認 requirements.txt 中包含 .whl 格式的模型安裝路徑。"
    ) from e


def find_match_indices(word_or_phrase, sentence):
    def normalize(text):
        text = re.sub(r"[^\w\s]", "", text)  # 移除標點
        text = re.sub(r"'s\b", "", text)  # 移除所有格
        return text.lower().split()

    lemma_target = [token.lemma_ for token in nlp(word_or_phrase)]
    sentence_tokens = nlp(sentence)

    words = []
    for token in sentence_tokens:
        if token.text not in ".,!?;:\"'()[]{}-–—…":
            words.append(token)

    lemmas = [token.lemma_.lower() for token in words]

    for i in range(len(lemmas) - len(lemma_target) + 1):
        if lemmas[i : i + len(lemma_target)] == lemma_target:
            return i + 1, i + len(lemma_target)  # 1-based indexing

    return "-", "-"
