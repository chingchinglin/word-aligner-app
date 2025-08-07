import pandas as pd
import re
import nltk
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()


def normalize(word):
    return lemmatizer.lemmatize(word.lower())


def tokenize(text):
    return [normalize(w) for w in nltk.word_tokenize(re.sub(r"[^\w\s]", "", text))]


def find_span(tokens, target_tokens):
    for i in range(len(tokens) - len(target_tokens) + 1):
        if tokens[i:i+len(target_tokens)] == target_tokens:
            return i + 1, i + len(target_tokens)  # 1-based indexing
    return None, None


def align_single_example(word_or_phrase, sentence, use_ai=False):
    if not isinstance(word_or_phrase, str) or not isinstance(sentence, str):
        return "-", "-", "人工處理"

    phrase_tokens = tokenize(word_or_phrase)
    sentence_tokens = tokenize(sentence)

    start, end = find_span(sentence_tokens, phrase_tokens)

    if start is not None:
        return str(start), str(end), "OK"
    elif use_ai:
        # 模擬 Gemini 模式：找第一個出現的詞，當作 backup
        for token in phrase_tokens:
            if token in sentence_tokens:
                idx = sentence_tokens.index(token)
                return str(idx + 1), str(idx + 1), "AI補齊"
        return "-", "-", "AI補齊失敗"
    else:
        return "-", "-", "人工處理"


def run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=False):
    index_basic_list, status_basic_list, match_basic_list = [], [], []
    index_adv_list, status_adv_list, match_adv_list = [], [], []

    for _, row in df.iterrows():
        word = row[col_word]

        # 基礎例句
        start, end, status = align_single_example(word, row[col_basic], use_ai)
        index_basic_list.append(f"{start}~{end}" if start != "-" else "-")
        status_basic_list.append(status)
        match_basic_list.append(row[col_basic])

        # 進階例句
        start, end, status = align_single_example(word, row[col_adv], use_ai)
        index_adv_list.append(f"{start}~{end}" if start != "-" else "-")
        status_adv_list.append(status)
        match_adv_list.append(row[col_adv])

    df["index_combined"] = [f"{b}|{a}" for b, a in zip(index_basic_list, index_adv_list)]
    df["status_combined"] = [f"{b}|{a}" for b, a in zip(status_basic_list, status_adv_list)]
    df["match_form_combined"] = [f"{b}|{a}" for b, a in zip(match_basic_list, match_adv_list)]
    df["word_or_phrase"] = df[col_word]

    return df
