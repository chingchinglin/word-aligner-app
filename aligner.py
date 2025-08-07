import nltk
import spacy
import subprocess

# 自動下載必要 nltk 資源
nltk_dependencies = [
    ("tokenizers/punkt", "punkt"),
    ("taggers/averaged_perceptron_tagger", "averaged_perceptron_tagger"),
    ("corpora/wordnet", "wordnet"),
]

for path, pkg in nltk_dependencies:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(pkg, quiet=True)

# 自動下載 spaCy 模型（如未安裝）
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    nlp = spacy.load("en_core_web_sm")

def find_match_indices(word_or_phrase, sentence):
    tokens = nltk.word_tokenize(sentence)
    word_list = nltk.word_tokenize(word_or_phrase)

    for i in range(len(tokens) - len(word_list) + 1):
        if tokens[i:i + len(word_list)] == word_list:
            return i + 1, i + len(word_list)  # 索引從 1 開始

    return -1, -1
