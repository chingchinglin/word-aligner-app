
from aligner import process_row
import pandas as pd

def run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=False):
    results = []

    for _, row in df.iterrows():
        word = row[col_word]
        basic_result = process_row(word, row[col_basic], use_ai)
        adv_result = process_row(word, row[col_adv], use_ai)

        results.append({
            'word_or_phrase': word,
            col_basic: row[col_basic],
            col_adv: row[col_adv],
            "index_combined": f"{basic_result['mark_start']} / {adv_result['mark_start']}",
            "match_form_combined": f"{basic_result['match_form']} / {adv_result['match_form']}",
            "status_combined": f"{basic_result['status']} / {adv_result['status']}",
        })

    return pd.DataFrame(results)
