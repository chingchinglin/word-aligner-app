import spacy
import nltk

# 自動下載必要 nltk 資源（避免 LookupError）
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

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


lemmatizer = WordNetLemmatizer()
nlp = spacy.load("en_core_web_sm")

def normalize(word):
    return lemmatizer.lemmatize(word.lower())

def tokenize(text):
    return [normalize(w) for w in word_tokenize(text)]

def find_match_indices(word, sentence):
    """
    傳入單字/片語（word）和句子（sentence），回傳開始與結束的索引（1-based）
    若找不到，則回傳 (-, -)
    """
    tokens = tokenize(sentence)
    word_tokens = tokenize(word)

    for i in range(len(tokens) - len(word_tokens) + 1):
        if tokens[i:i + len(word_tokens)] == word_tokens:
            # 回傳 1-based 索引值
            return i + 1, i + len(word_tokens)
    
    return "-", "-"
