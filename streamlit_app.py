import streamlit as st
import pandas as pd
import spacy
import os
from aligner import align_word_or_phrase

# Load SpaCy model
@st.cache_resource
def load_model():
    return spacy.load("en_core_web_sm")
nlp = load_model()

st.title("🧠 Word/Phrase Position Aligner")
st.markdown("Upload an Excel or CSV file with the following columns:")
st.code("Word or Phrase | Basic Sentence | Advanced Sentence")

uploaded_file = st.file_uploader("Upload your file", type=["xlsx", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        required_columns = ["Word or Phrase", "Basic Sentence", "Advanced Sentence"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"❗ Missing required columns: {', '.join(missing_columns)}")
        else:
            basic_starts, basic_ends = [], []
            adv_starts, adv_ends = [], []

            for _, row in df.iterrows():
                word = row["Word or Phrase"]
                basic_sentence = row["Basic Sentence"]
                adv_sentence = row["Advanced Sentence"]

                basic_start, basic_end = align_word_or_phrase(word, basic_sentence, nlp)
                adv_start, adv_end = align_word_or_phrase(word, adv_sentence, nlp)

                basic_starts.append(basic_start)
                basic_ends.append(basic_end)
                adv_starts.append(adv_start)
                adv_ends.append(adv_end)

            df["Basic Start"] = basic_starts
            df["Basic End"] = basic_ends
            df["Advanced Start"] = adv_starts
            df["Advanced End"] = adv_ends

            st.success("✅ Alignment complete!")
            st.dataframe(df)

            # Download result
            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="Download Result as CSV",
                data=csv,
                file_name="aligned_output.csv",
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
