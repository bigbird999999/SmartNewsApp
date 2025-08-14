import streamlit as st
import scraper
import summarization
import keywordExtractor
import qa
import nltk
nltk.download('punkt')



st.title("Smart News Application")
st.header(f"Top News Articles at this time")

with st.spinner(f"Fetching articles..."):
    links = scraper.get_article_links()
    for link in links:
        article_data = scraper.extract_article_data(link)
        if article_data["title"] != "Error":
            st.subheader(article_data["title"])
            if article_data["top_image"]:
                st.image(article_data["top_image"],  use_container_width=True)
            st.write(article_data["text"][:500] + "...")
            st.markdown(f"[Read full article]({article_data['url']})")
            with st.expander(" More Tools"):
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Summarize - {article_data['title']}", key=link+"sum"):
                        summary = summarization.summarize_article(article_data["text"])
                        st.markdown("** Summary:**")
                        st.write(summary)
                with col2:
                    if st.button(f"Extract Keywords - {article_data['title']}", key=link+"kw"):
                        keywords = keywordExtractor.extract_keywords(article_data["text"])
                        st.markdown("** Keywords:**")
                        st.write(", ".join(keywords))
                question = st.text_input(f"❓ Ask a question about this article", key=link+"qa")
                if question:
                    answer = qa.questionAnswer(question,article_data["text"])
                    st.markdown("** Answer:**")
                    st.write(answer)
        else:
            st.warning(f"Could not load article: {article_data['url']}")