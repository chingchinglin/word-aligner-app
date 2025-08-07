import streamlit as st
import pandas as pd
import nltk

# 自動下載 punkt tokenizer（雲端首次使用需要）
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from run_batch import run_alignment_batch

st.set_page_config(page_title="Word‑Example Aligner Tool (Gemini 版)")
st.title("📚 Word‑Example Aligner Tool (Gemini 模式)")

upload = st.file_uploader("📎 上傳 CSV 或 Excel 檔案", type=["csv", "xlsx"])
if upload:
    if upload.name.endswith(".csv"):
        df = pd.read_csv(upload)
    else:
        df = pd.read_excel(upload)

    st.write("🔍 原始資料預覽：")
    st.dataframe(df.head())

    col_word = st.selectbox("🔤 選擇「單字或片語」欄位", df.columns)
    col_basic = st.selectbox("🟢 選擇「基礎例句」欄位", df.columns)
    col_adv = st.selectbox("🔵 選擇「進階例句」欄位", df.columns)
    use_ai = st.checkbox("🤖 啟用 Gemini 模式（NLP 無法處理時，自動補足）", value=True)

    if st.button("🚀 執行對齊"):
        with st.spinner("正在處理，請稍候..."):
            result = run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=use_ai)
        st.success("✅ 處理完成！")

        st.dataframe(result[[
            "word_or_phrase", col_basic, col_adv,
            "index_combined", "match_form_combined", "status_combined"
        ]].head(20))

        csv = result.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ 下載對齊結果 CSV", csv, "aligned_result.csv", "text/csv")
