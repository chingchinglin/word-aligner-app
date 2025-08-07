import streamlit as st
import pandas as pd
from run_batch import process_file

st.set_page_config(page_title="單字與例句對齊工具", layout="wide")

# UI 顯示區塊
st.title("📚 單字與例句對齊工具")
st.markdown("請上傳包含單字與例句的 Excel 或 CSV 檔案，我們會自動標記出單字在例句中的位置。")

uploaded_file = st.file_uploader("請選擇檔案：", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # 自動判斷副檔名
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success("✅ 檔案已成功上傳，開始處理中⋯⋯")

        # 執行處理
        processed_df = process_file(df)

        # 顯示處理後結果
        st.markdown("### 🔍 標註結果預覽")
        st.dataframe(processed_df)

        # 提供下載連結
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8-sig')

        csv = convert_df(processed_df)
        st.download_button(
            label="📥 下載標註結果 (CSV)",
            data=csv,
            file_name="aligned_result.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
else:
    st.info("👈 請先上傳檔案開始處理。")
