import streamlit as st
from transformers import pipeline
import streamlit as st

@st.cache_resource
def qa_model():
    return pipeline("text2text-generation", model="google/flan-t5-small")

qa=qa_model()
def questionAnswer(question,article):
    prompt = f"question: {question} context: {article}"
    output = qa(prompt, max_length=128, do_sample=False)
    return (output[0]["generated_text"])
