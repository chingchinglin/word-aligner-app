import re
import spacy

nlp = spacy.blank("en")

def tokenize(sentence):
    sentence = re.sub(r"[^\w\s]", "", sentence)
    sentence = re.sub(r"\’s|\‘s|'s", "", sentence)
    return sentence.strip().split()

def lemmatize(word):
    doc = nlp(word)
    return doc[0].lemma_ if doc else word.lower()

def align_word_in_sentence(word_or_phrase, sentence):
    tokens = tokenize(sentence)
    lemma_tokens = [lemmatize(tok) for tok in tokens]

    target_tokens = [lemmatize(w) for w in word_or_phrase.strip().split()]
    n = len(target_tokens)

    for i in range(len(lemma_tokens) - n + 1):
        if lemma_tokens[i:i+n] == target_tokens:
            return i + 1, i + n

    return "-", "-", "人工處理"

def get_example_alignment():
    return align_word_in_sentence("apple", "I ate two apples.")
