import streamlit as st
import pandas as pd
import os
import io
import base64
import requests

from run_batch import run_alignment_batch  # 假設你有這個 function

st.set_page_config(page_title="單字對齊標記工具", layout="centered")

st.title("📘 單字例句對齊與檢查工具")

# --- 上傳檔案區塊 ---
uploaded_file = st.file_uploader("⬆️ 上傳你的 .csv 檔案", type=["csv"])
url_input = st.text_input("或貼上雲端檔案（Google Sheets、GitHub raw 等）URL")

# --- 下載與解析 CSV ---
def read_csv_file(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"❌ 無法讀取檔案: {e}")
        return None

def fetch_csv_from_url(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        return pd.read_csv(io.StringIO(res.text))
    except Exception as e:
        st.error(f"❌ 無法從網址取得檔案: {e}")
        return None

# --- 資料輸入與處理 ---
df = None
if uploaded_file:
    df = read_csv_file(uploaded_file)
elif url_input:
    df = fetch_csv_from_url(url_input)

if df is not None:
    st.success("✅ 成功讀取檔案！以下是預覽：")
    st.dataframe(df.head())

    if st.button("🚀 開始處理並標記對齊"):
        with st.spinner("處理中...請稍候"):
            try:
                result_df = run_alignment_batch(df)  # 假設此函數會回傳處理後 DataFrame

                st.success("✅ 處理完成！以下是部分結果：")
                st.dataframe(result_df.head())

                # 建立下載連結
                output = io.StringIO()
                result_df.to_csv(output, index=False)
                b64 = base64.b64encode(output.getvalue().encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="output_aligned.csv">📥 下載處理後檔案</a>'
                st.markdown(href, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ 執行失敗: {e}")
