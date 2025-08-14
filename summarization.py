from transformers import pipeline
import textwrap
import streamlit as st
#Load summarizer
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()
# Function to chunk long text
def split_text(text, max_chunk=1000):
    paragraphs = text.split('\n')
    current_chunk = ""
    chunks = []
    
    for paragraph in paragraphs:
        if len(current_chunk.split()) + len(paragraph.split()) <= max_chunk:
            current_chunk += " " + paragraph
        else:
            chunks.append(current_chunk.strip())
            current_chunk = paragraph
    chunks.append(current_chunk.strip())  # Add final chunk
    return chunks

# Summarize full article
@st.cache_data(show_spinner=False)
def summarize_article(text):
    chunks = split_text(text)
    print(f"Splitting into {len(chunks)} chunk(s)")

    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarizer(chunk, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)

    #summarize the combined summary
    final_input = " ".join(summaries)
    if len(final_input.split()) > 1000:
        final_input = " ".join(summaries[:2])  # Keep it short enough
    final_summary = summarizer(final_input, max_length=150, min_length=40, do_sample=False)[0]['summary_text']
    return final_summary

