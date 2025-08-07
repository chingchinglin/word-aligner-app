import streamlit as st
import pandas as pd
import os
from aligner import process_alignment

st.set_page_config(page_title="Word Aligner App", layout="wide")
st.title("🧠 Vocabulary Aligner")
st.markdown("上傳含有英文單字與例句的 Excel/CSV 檔案，系統會自動標註單字在句子中的出現位置。")

uploaded_file = st.file_uploader("📤 請上傳檔案（支援 .xlsx, .csv）", type=["xlsx", "csv"])

if uploaded_file:
    st.write("📥 檔案已上傳：", uploaded_file.name)

    with st.spinner("🔄 正在處理資料，請稍候..."):
        # 儲存上傳檔案
        temp_path = os.path.join("/tmp", uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        try:
            # 判斷檔案格式並讀取
            if uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(temp_path)
            else:
                df = pd.read_csv(temp_path)

            # 執行對齊處理
            result_df = process_alignment(df)

            # 顯示部分結果預覽
            st.success("✅ 處理完成！以下為前 10 筆結果預覽：")
            st.dataframe(result_df.head(10))

            # 提供下載
            csv = result_df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📥 下載完整結果 CSV",
                data=csv,
                file_name="aligned_result.csv",
                mime="text/csv"
            )

        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
else:
    st.info("請先上傳檔案以開始處理。")
