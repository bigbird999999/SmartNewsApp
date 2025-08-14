import requests
from bs4 import BeautifulSoup
from newspaper import Article
from urllib.parse import urljoin
import streamlit as st

# Categories and URLs
categories = {
    "India": "https://timesofindia.indiatimes.com/india",
    "World": "https://timesofindia.indiatimes.com/world",
    "Business": "https://timesofindia.indiatimes.com/business",
    "Technology": "https://timesofindia.indiatimes.com/technology",
    "Sports": "https://timesofindia.indiatimes.com/sports"
}

domain_keywords = ["/india","/city", "/elections", "/world", "/business", "/technology","/cricket"]

# Article link fetcher
def get_article_links():
    for category, url in categories.items():
        session = requests.Session()
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            st.error(f"Error fetching {url}: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        article_links = set()

        for tag in soup.find_all('a', href=True):
            link = tag['href']
            if "articleshow" in link and any(kw in link for kw in domain_keywords):
                full_link = urljoin("https://timesofindia.indiatimes.com", link)
                article_links.add(full_link)
    return list(article_links)[:25]

# Article extractor
def extract_article_data(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return {
            "title": article.title,
            "text": article.text,
            "top_image": article.top_image,
            "url": url
        }
    except Exception as e:
        return {"title": "Error", "text": str(e), "top_image": "", "url": url}