import spacy
import nltk
import pandas as pd
from nltk.stem import WordNetLemmatizer

# 確保 NLTK 的詞形還原器資源已下載
nltk.download("wordnet", quiet=True)
lemmatizer = WordNetLemmatizer()

# 直接 import 已安裝的模型，不要用 subprocess 安裝
try:
    nlp = spacy.load("en_core_web_sm")
except:
    raise RuntimeError("❌ spaCy 模型未安裝。請確認 requirements.txt 已包含模型下載網址")

def lemmatize(word):
    return lemmatizer.lemmatize(word.lower())

def find_match_indices(word_or_phrase, sentence):
    doc = nlp(sentence)
    tokens = [token.text.lower() for token in doc]
    lemmas = [lemmatize(token) for token in tokens]

    # 詞形還原輸入的 word_or_phrase（單字或片語）
    target_tokens = word_or_phrase.lower().split()
    target_lemmas = [lemmatize(token) for token in target_tokens]
    target_len = len(target_lemmas)

    for i in range(len(lemmas) - target_len + 1):
        if lemmas[i:i + target_len] == target_lemmas:
            return i + 1, i + target_len  # 索引從 1 開始

    return "-", "-"
