import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re

# 嘗試載入 spaCy 模型
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise OSError("❌ 找不到 spaCy 模型 'en_core_web_sm'。請確認 requirements.txt 已包含模型下載連結，並重新部署 App。")

lemmatizer = WordNetLemmatizer()

# 匹配範圍正規化用（忽略標點與所有格）
def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower().replace("'s", ""))

def lemmatize_word(word, pos_tag):
    pos = get_wordnet_pos(pos_tag)
    return lemmatizer.lemmatize(word, pos=pos) if pos else word

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

def find_match_indices(sentence, target_phrase):
    doc = nlp(sentence)
    tokens = [token.text for token in doc]
    tokens_lemma = [lemmatize_word(token.text, token.tag_) for token in doc]

    # 處理目標單字或片語
    phrase_doc = nlp(target_phrase)
    phrase_tokens = [token.text for token in phrase_doc]
    phrase_lemmas = [lemmatize_word(token.text, token.tag_) for token in phrase_doc]

    phrase_len = len(phrase_lemmas)

    for i in range(len(tokens_lemma) - phrase_len + 1):
        if tokens_lemma[i:i+phrase_len] == phrase_lemmas:
            return i + 1, i + phrase_len  # index from 1

    # 若找不到，回傳 None，代表需人工處理
    return None, None
