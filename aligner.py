
import os
from dotenv import load_dotenv
load_dotenv()

import re
import google.generativeai as genai
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def clean_and_tokenize(sentence):
    sentence = re.sub(r"\b(\w+)'s\b", r"\1", sentence)
    sentence = re.sub(r"[^\w\s]", "", sentence)
    tokens = sentence.split()
    return tokens

def lemmatize_token(token):
    return lemmatizer.lemmatize(token.lower())

def gemini_fallback(word_or_phrase, sentence):
    prompt = f"""
請根據以下規則，找出給定單字或片語在句子中的詞索引位置（從 1 開始）：
1. 忽略標點與 's 所有格
2. 支援詞形變化，如 go/went、run/ran 等
3. 僅標記連續詞（multi-token phrase）
4. 輸出格式：start=X, end=Y, match_form="...", status=Gemini

單字或片語: {word_or_phrase}
句子: {sentence}
"""
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        reply = response.text
        match = re.search(r"start=(\d+), end=(\d+), match_form=\"(.+?)\"", reply)
        if match:
            return int(match.group(1)), int(match.group(2)), match.group(3), "Gemini"
    except Exception as e:
        print("Gemini fallback failed:", e)

    return "-", "-", "-", "人工處理"

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

def process_row(word, sentence, use_ai=False):
    start, end, match_form, status = find_match_indices(word, sentence)
    if status == "人工處理" and use_ai:
        start, end, match_form, status = gemini_fallback(word, sentence)
    return {
        'word_or_phrase': word,
        'sentence': sentence,
        'mark_start': start,
        'mark_end': end,
        'match_form': match_form,
        'status': status
    }
