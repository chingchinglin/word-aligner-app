import re

def tokenize(sentence):
    sentence = re.sub(r"[^\w\s]", "", sentence)
    sentence = re.sub(r"\’s|\‘s|'s", "", sentence)
    return sentence.strip().split()

def lemmatize(word):
    exceptions = {"ate": "eat", "went": "go", "ran": "run", "was": "be", "were": "be"}
    word = word.lower()
    if word in exceptions:
        return exceptions[word]
    if word.endswith("ies"):
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    if word.endswith("ed"):
        return word[:-2]
    if word.endswith("ing"):
        return word[:-3]
    return word

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
