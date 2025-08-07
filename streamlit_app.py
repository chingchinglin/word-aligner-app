import streamlit as st
from aligner import get_example_alignment

st.title("🔍 Word Aligner (Safe Version)")
start, end = get_example_alignment()
st.write(f"測試對齊結果：start={start}, end={end}")

