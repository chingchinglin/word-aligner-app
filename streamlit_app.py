import streamlit as st
import pandas as pd
from run_batch import run_alignment_batch

st.set_page_config(page_title="Word Aligner", layout="centered")
st.title("📘 Word‑Example Aligner Tool (Gemini 版)")

upload = st.file_uploader("📤 上傳 CSV 或 Excel 檔案", type=["csv", "xlsx"])
if upload:
    if upload.name.endswith(".csv"):
        df = pd.read_csv(upload)
    else:
        df = pd.read_excel(upload)

    st.subheader("📑 原始資料預覽")
    st.dataframe(df.head())

    col_word = st.selectbox("🔤 選擇「單字或片語」欄位", df.columns)
    col_basic = st.selectbox("📘 選擇「基礎例句」欄位", df.columns)
    col_adv = st.selectbox("📗 選擇「進階例句」欄位", df.columns)
    use_ai = st.checkbox("✅ 啟用 Gemini 模式（當 NLP 無法對齊時，自動補足）", value=True)

    if st.button("🚀 執行對齊"):
        with st.spinner("⏳ 處理中，請稍候..."):
            try:
                result = run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=use_ai)
                st.success("🎉 對齊完成！")

                st.subheader("📋 對齊結果預覽")
                st.dataframe(result[["word_or_phrase", col_basic, col_adv,
                                     "index_combined", "match_form_combined", "status_combined"]].head(10))

                csv = result.to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ 下載對齊結果 CSV", csv, "aligned_result.csv", "text/csv")

            except Exception as e:
                st.error("❌ 執行時發生錯誤")
                st.exception(e)
