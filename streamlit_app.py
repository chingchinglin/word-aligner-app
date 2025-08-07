import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')


import re
import spacy
from nltk.stem import WordNetLemmatizer

nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()

def tokenize(text):
    # 移除所有標點與所有格
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\’s|\‘s|'s", "", text)
    return text.strip().split()

def lemmatize(word):
    return lemmatizer.lemmatize(word.lower())

def align_word_or_phrase(word_or_phrase, sentence):
    tokens = tokenize(sentence)
    lemma_tokens = [lemmatize(tok) for tok in tokens]

    target_tokens = [lemmatize(w) for w in tokenize(word_or_phrase)]
    n = len(target_tokens)

    for i in range(len(lemma_tokens) - n + 1):
        if lemma_tokens[i:i+n] == target_tokens:
            return i + 1, i + n  # 索引從 1 開始

    return "-", "-", "人工處理"

# 保留一個範例函式供 Streamlit 測試用（不影響主邏輯）
def get_example_alignment():
    return align_word_or_phrase("turn off", "Please turn off the light.")
