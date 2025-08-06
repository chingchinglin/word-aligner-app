import re
from nltk.stem import WordNetLemmatizer

def normalize_sentence(sent):
    # 去除標點與所有格 ’s/'s
    text = re.sub(r"[,.?;:!\"\'\(\)\[\]\{\}\-–—…]", " ", sent)
    text = re.sub(r"\b(\w+)'s\b", r"\1", text)
    tokens = text.lower().split()
    return tokens

def find_span(target_tokens, sent_tokens):
    n = len(target_tokens)
    for i in range(len(sent_tokens) - n + 1):
        window = sent_tokens[i:i+n]
        if window == target_tokens:
            return i+1, i+n  # 1-based index
    return None

def process_row(word, sent):
    lemmatizer = WordNetLemmatizer()
    # normalize
    wtoks = [lemmatizer.lemmatize(t) for t in normalize_sentence(word)]
    stoks = normalize_sentence(sent)
    # lemmatize all
    stoks_lem = [lemmatizer.lemmatize(t) for t in stoks]
    span = find_span(wtoks, stoks_lem)
    if span:
        s,e = span
        matched = " ".join(stoks[s-1:e])
        return s, e, matched, "OK"
    else:
        return "-", "-", "-", "人工處理"

def run_alignment_batch(df, col_word, col_basic, col_adv):
    # 初始化結果欄位
    df["index_combined"] = ""
    df["match_form_combined"] = ""
    df["status_combined"] = ""
    
    for i, row in df.iterrows():
        ws = str(row.get(col_word, "")).strip()
        basic = str(row.get(col_basic, "")).strip()
        adv = str(row.get(col_adv, "")).strip()
        
        b_idx, b_end, b_match, b_stat = process_row(ws, basic) if basic else ("-", "-", "-", "人工處理")
        a_idx, a_end, a_match, a_stat = process_row(ws, adv) if adv else ("-", "-", "-", "人工處理")
        
        idx_comb = f"Basic: {b_idx}-{b_end} | Adv: {a_idx}-{a_end}"
        match_comb = f"Basic: {b_match} | Adv: {a_match}"
        stat_comb = f"Basic: {b_stat} | Adv: {a_stat}"
        
        df.at[i, "index_combined"] = idx_comb
        df.at[i, "match_form_combined"] = match_comb
        df.at[i, "status_combined"] = stat_comb
    return df
