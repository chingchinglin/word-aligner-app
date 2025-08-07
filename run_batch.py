import re
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import wordpunct_tokenize

lemmatizer = WordNetLemmatizer()

def normalize(word):
    return lemmatizer.lemmatize(word.lower())

def tokenize(text):
    return [normalize(w) for w in wordpunct_tokenize(text)]

def align_single_example(word_or_phrase, sentence, use_ai=False):
    phrase_tokens = tokenize(word_or_phrase)
    sentence_tokens = tokenize(sentence)

    phrase_len = len(phrase_tokens)
    sentence_len = len(sentence_tokens)

    for i in range(sentence_len - phrase_len + 1):
        window = sentence_tokens[i:i + phrase_len]
        if window == phrase_tokens:
            return i + 1, i + phrase_len, "匹配"  # 索引從 1 開始

    if use_ai:
        return "-", "-", "AI補足"
    else:
        return "-", "-", "人工處理"

def run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=False):
    basic_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_basic], use_ai),
        axis=1
    )
    adv_results = df.apply(
        lambda row: align_single_example(row[col_word], row[col_adv], use_ai),
        axis=1
    )

    df["basic_start"] = [r[0] for r in basic_results]
    df["basic_end"] = [r[1] for r in basic_results]
    df["status_basic"] = [r[2] for r in basic_results]

    df["adv_start"] = [r[0] for r in adv_results]
    df["adv_end"] = [r[1] for r in adv_results]
    df["status_adv"] = [r[2] for r in adv_results]

    df["index_combined"] = df.apply(lambda row: f"{row['basic_start']}-{row['basic_end']}, {row['adv_start']}-{row['adv_end']}", axis=1)
    df["match_form_combined"] = df.apply(lambda row: f"{row['status_basic']}, {row['status_adv']}", axis=1)

    def combine_status(row):
        if row["status_basic"] == row["status_adv"]:
            return row["status_basic"]
        else:
            return f"{row['status_basic']}/{row['status_adv']}"

    df["status_combined"] = df.apply(combine_status, axis=1)
    df["word_or_phrase"] = df[col_word]

    return df
