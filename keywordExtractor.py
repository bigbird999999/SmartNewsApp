import streamlit as st
from keybert import KeyBERT

# Load KeyBERT model with caching
@st.cache_resource
def keyword_model():
    return KeyBERT(model='all-MiniLM-L6-v2')

kw_model = keyword_model()

# Extract keywords with caching
@st.cache_data(show_spinner=False)
def extract_keywords(text, top_n=5):
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 2), stop_words='english', top_n=top_n)
    return [kw[0] for kw in keywords]
