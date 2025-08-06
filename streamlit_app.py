import streamlit as st
import pandas as pd
import nltk
from run_batch import run_alignment_batch  # 確保 run_batch.py 有這個 function

# 下載 WordNet 資源
nltk.download('wordnet')
nltk.download('omw-1.4')

st.title("Word Aligner App")

# 上傳或輸入網址
upload_option = st.radio("選擇輸入方式：", ("上傳檔案", "輸入 URL"))

if upload_option == "上傳檔案":
    uploaded_file = st.file_uploader("上傳 CSV 或 Excel 檔案", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
elif upload_option == "輸入 URL":
    url = st.text_input("輸入檔案的 URL")
    if url:
        try:
            if url.endswith(".csv"):
                df = pd.read_csv(url)
            else:
                df = pd.read_excel(url)
        except Exception as e:
            st.error(f"讀取檔案失敗: {e}")
            df = None
else:
    df = None

if 'df' in locals() and df is not None:
    st.write("原始資料：", df.head())

    if st.button("執行對齊"):
        try:
            result_df = run_alignment_batch(df)
            st.success("對齊完成！")
            st.dataframe(result_df)

            # 提供下載
            csv = result_df.to_csv(index=False).encode('utf-8')
            st.download_button("下載結果 CSV", csv, "aligned_result.csv", "text/csv")
        except Exception as e:
            st.error(f"處理失敗: {e}")
