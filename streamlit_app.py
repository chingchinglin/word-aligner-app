# streamlit_app.py

import streamlit as st
import pandas as pd
import nltk
import traceback

# -----------------------------------------------------------------------------
# Streamlit 頁面設定：必須在所有 st.* 之前呼叫
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Word-Example Aligner Tool (Gemini 版)")

# -----------------------------------------------------------------------------
# 下載 NLTK punkt tokenizer（只會在雲端第一次執行時跑）
# -----------------------------------------------------------------------------
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# -----------------------------------------------------------------------------
# 核心函式：批次對齊
# -----------------------------------------------------------------------------
from run_batch import run_alignment_batch

# -----------------------------------------------------------------------------
# 主程式邏輯
# -----------------------------------------------------------------------------
def main():
    st.title("📚 Word-Example Aligner Tool (Gemini 模式)")
    upload = st.file_uploader("📎 上傳 CSV 或 Excel 檔案", type=["csv", "xlsx"])
    if not upload:
        return

    # 讀檔
    if upload.name.endswith(".csv"):
        df = pd.read_csv(upload)
    else:
        df = pd.read_excel(upload)

    st.write("🔍 原始資料預覽：")
    st.dataframe(df.head())

    # 欄位選擇
    col_word = st.selectbox("🔤 選擇「單字或片語」欄位", df.columns)
    col_basic = st.selectbox("🟢 選擇「基礎例句」欄位", df.columns)
    col_adv = st.selectbox("🔵 選擇「進階例句」欄位", df.columns)
    use_ai = st.checkbox("🤖 啟用 Gemini 模式（NLP 無法處理時，自動補足）", value=True)

    # 執行按鈕
    if st.button("🚀 執行對齊"):
        with st.spinner("正在處理，請稍候..."):
            result = run_alignment_batch(df, col_word, col_basic, col_adv, use_ai=use_ai)

        st.success("✅ 處理完成！")
        st.dataframe(
            result[
                [
                    "word_or_phrase",
                    col_basic,
                    col_adv,
                    "index_combined",
                    "match_form_combined",
                    "status_combined",
                ]
            ].head(20)
        )

        csv = result.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ 下載對齊結果 CSV",
            csv,
            "aligned_result.csv",
            "text/csv",
        )

# -----------------------------------------------------------------------------
# Entry point：攔截所有 Exception，並印出 Traceback
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        main()
    except Exception:
        st.error("🚨 應用程式執行錯誤，請檢查下面的詳細資訊：")
        st.text(traceback.format_exc())
        st.stop()
