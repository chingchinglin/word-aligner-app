import sys
import pandas as pd
from aligner import process_dataframe

def main():
    if len(sys.argv) != 3:
        print("使用方法：python run_batch.py input.xlsx output.xlsx")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        df = pd.read_excel(input_file)

        if 'word_or_phrase' not in df.columns or 'sentence_type' not in df.columns or 'sentence' not in df.columns:
            print("❌ Excel 檔案缺少必要欄位：'word_or_phrase'、'sentence_type' 或 'sentence'")
            sys.exit(1)

        # 執行對齊處理
        processed_df = process_dataframe(df)

        # 加回 sentence_type 資訊（因為 process_dataframe 沒保留）
        processed_df['sentence_type'] = df['sentence_type'].values

        # 拆成 Basic 與 Advanced 兩組，重新命名欄位
        basic_df = processed_df[processed_df['sentence_type'] == 'Basic'].copy()
        basic_df = basic_df.rename(columns={
            'sentence': 'basic_sentence',
            'mark_start': 'basic_mark_start',
            'mark_end': 'basic_mark_end',
            'match_form': 'basic_match_form',
            'status': 'basic_status'
        }).drop(columns=['sentence_type'])

        advanced_df = processed_df[processed_df['sentence_type'] == 'Advanced'].copy()
        advanced_df = advanced_df.rename(columns={
            'sentence': 'advanced_sentence',
            'mark_start': 'advanced_mark_start',
            'mark_end': 'advanced_mark_end',
            'match_form': 'advanced_match_form',
            'status': 'advanced_status'
        }).drop(columns=['sentence_type'])

        # 合併成一行（以 word_or_phrase 為鍵）
        merged = pd.merge(basic_df, advanced_df, on='word_or_phrase', how='outer')

        # 儲存輸出
        merged.to_excel(output_file, index=False)
        print(f"✅ 處理完成，已合併並輸出為：{output_file}")

    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
