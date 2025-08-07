import spacy
import pandas as pd
import subprocess

# 嘗試載入 spaCy 模型，如果沒安裝就自動安裝
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

def find_match_indices(word_or_phrase, sentence):
    def tokenize(text):
        return [
            token.text.lower()
            for token in nlp(text)
            if not token.is_punct and token.text.lower() != "'s"
        ]

    target_tokens = tokenize(word_or_phrase)
    sentence_tokens = tokenize(sentence)

    for i in range(len(sentence_tokens) - len(target_tokens) + 1):
        if sentence_tokens[i : i + len(target_tokens)] == target_tokens:
            return i + 1, i + len(target_tokens)

    return "-", "-"
