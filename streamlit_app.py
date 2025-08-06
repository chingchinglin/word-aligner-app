import streamlit as st
import pandas as pd
import nltk
from run_batch import run_alignment_batch

nltk.download('wordnet')
nltk.download('omw-1.4')

st.title("Word‑Example Aligner Tool")

upload = st.file_uploader("上傳 CSV 或 Excel 檔案", type=["csv","xlsx"])
if upload:
    if upload.name.endswith(".csv"):
        df = pd.read_csv(upload)
    else:
        df = pd.read_excel(upload)

    st.write("原始資料預覽：")
    st.dataframe(df.head())

    col_word = st.selectbox("選擇「單字或片語」欄位", df.columns)
    col_basic = st.selectbox("選擇「基礎例句」欄位", df.columns)
    col_adv = st.selectbox("選擇「進階例句」欄位", df.columns)

    if st.button("執行對齊"):
        with st.spinner("處理中..."):
            result = run_alignment_batch(df, col_word, col_basic, col_adv)
        st.success("完成 ✅")
        st.dataframe(result[["word_or_phrase", col_basic, col_adv,
                             "index_combined", "match_form_combined", "status_combined"]].head(10))
        csv = result.to_csv(index=False).encode("utf-8")
        st.download_button("下載對齊結果 CSV", csv, "aligned_result.csv", "text/csv")
