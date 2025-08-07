import nltk

# 自動下載 punkt（如果還沒下載的話）
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# 另外也補一個 wordnet（避免其他元件也找不到）
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')


import re
import pandas as pd
from nltk.stem import WordNetLemmatizer
import spacy

# 載入 spaCy 的英文模型（第一次需用: python -m spacy download en_core_web_sm）
nlp = spacy.load("en_core_web_sm")
lemmatizer = WordNetLemmatizer()

def clean_and_tokenize(sentence):
    # 移除所有格 's
    sentence = re.sub(r"\b(\w+)'s\b", r"\1", sentence)
    # 移除標點
    sentence = re.sub(r"[^\w\s]", "", sentence)
    # 分詞
    tokens = sentence.split()
    return tokens

def lemmatize_phrase(phrase):
    # 同時用 spaCy 和 WordNet 雙重詞形還原
    doc = nlp(phrase.lower())
    lemmatized = [lemmatizer.lemmatize(token.lemma_) for token in doc]
    return lemmatized

def find_match_indices(word_or_phrase, sentence):
    tokens = clean_and_tokenize(sentence)
    lemmatized_sentence = lemmatize_phrase(" ".join(tokens))
    lemmatized_phrase = lemmatize_phrase(word_or_phrase)

    len_phrase = len(lemmatized_phrase)

    for i in range(len(lemmatized_sentence) - len_phrase + 1):
        if lemmatized_sentence[i:i + len_phrase] == lemmatized_phrase:
            start = i + 1  # 索引從 1 開始
            end = i + len_phrase
            matched_form = " ".join(tokens[i:i + len_phrase])
            return start, end, matched_form, "OK"

    return "-", "-", "-", "人工處理"

def process_dataframe(df):
    results = []

    for _, row in df.iterrows():
        word = row['word_or_phrase']
        sentence = row['sentence']
        start, end, match_form, status = find_match_indices(word, sentence)

        results.append({
            'word_or_phrase': word,
            'sentence': sentence,
            'mark_start': start,
            'mark_end': end,
            'match_form': match_form,
            'status': status
        })

    return pd.DataFrame(results)
