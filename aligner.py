import spacy
import pandas as pd

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError("spaCy 模型 'en_core_web_sm' 未安裝，請在本地或部署環境中手動安裝。")

def find_match_indices(word_or_phrase, sentence):
    def tokenize(text):
        return [token.text.lower() for token in nlp(text) if not token.is_punct and token.text.lower() != "'s"]

    target_tokens = tokenize(word_or_phrase)
    sentence_tokens = tokenize(sentence)

    for i in range(len(sentence_tokens) - len(target_tokens) + 1):
        if sentence_tokens[i:i+len(target_tokens)] == target_tokens:
            return i + 1, i + len(target_tokens)

    return "-", "-"
