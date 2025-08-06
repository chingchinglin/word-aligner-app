import re
import pandas as pd
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

def clean_and_tokenize(sentence):
    sentence = re.sub(r"\b(\w+)'s\b", r"\1", sentence)
    sentence = re.sub(r"[^\w\s]", "", sentence)
    tokens = sentence.split()
    return tokens

def lemmatize_token(token):
    return lemmatizer.lemmatize(token.lower())

def find_match_indices(word_or_phrase, sentence):
    tokens = clean_and_tokenize(sentence)
    phrase_tokens = clean_and_tokenize(word_or_phrase)

    lemmatized_tokens = [lemmatize_token(t) for t in tokens]
    lemmatized_phrase = [lemmatize_token(p) for p in phrase_tokens]
    phrase_len = len(lemmatized_phrase)

    for i in range(len(lemmatized_tokens) - phrase_len + 1):
        if lemmatized_tokens[i:i + phrase_len] == lemmatized_phrase:
            return i + 1, i + phrase_len, " ".join(tokens[i:i + phrase_len]), "OK"

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
