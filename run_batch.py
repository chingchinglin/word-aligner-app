from nltk.stem import WordNetLemmatizer

def align_words(word, sentence):
    lemmatizer = WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word.lower())
    return lemma in sentence.lower()

def process_dataframe(df, word_col, sentence_cols):
    for col in sentence_cols:
        new_col_name = f"{col}_matched"
        df[new_col_name] = df.apply(lambda row: align_words(str(row[word_col]), str(row[col])), axis=1)
    return df

def run_alignment_batch(df, word_col, sentence_cols):
    return process_dataframe(df, word_col, sentence_cols)
