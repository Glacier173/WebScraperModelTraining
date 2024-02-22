import yfinance as yf
import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk

def preprocess_article(article_text):
    article_text = article_text.lower()
    article_text = re.sub(r'http\S+|www\.\S+', '', article_text)
    article_text = re.sub(r'\d+', '', article_text)
    article_text = re.sub(r'\W+', ' ', article_text)
    tokens = word_tokenize(article_text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_text = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    preprocessed_text = ' '.join(lemmatized_text)
    return preprocessed_text

def scrape_stock_news(ticker):
    headlines = []
    url = f'https://finance.yahoo.com/quote/{ticker}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        h3_tags = soup.find_all('h3')
        for h3 in h3_tags:
            a_tag = h3.find('a')
            if a_tag and a_tag.text:
                headlines.append(a_tag.text)
        if len(headlines) > 7:
            headlines = headlines[6:-1]
    return headlines

def scrape_stock_news_articles(ticker):
    articles = []
    url = f'https://finance.yahoo.com/quote/{ticker}'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        h3_tags = soup.find_all('h3')
        for h3 in h3_tags:
            a_tag = h3.find('a')
            if a_tag and 'href' in a_tag.attrs:
                article_url = 'https://finance.yahoo.com' + a_tag.attrs['href']
                articles.append((a_tag.text, article_url))
        if len(articles) > 7:
            articles = articles[6:-1]
    return articles

def fetch_full_article(article_url):
    response = requests.get(article_url)
    article_text = ''
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            article_text += p.text + ' '
    return article_text.strip()

def preprocess_headlines(headlines):
    cleaned_headlines = []
    for headline in headlines:
        cleaned_headline = headline.replace('\n', ' ').strip()
        cleaned_headlines.append(cleaned_headline)
    return cleaned_headlines

def main():
    symbol = input("Enter stock symbol: ").upper()
    headlines = scrape_stock_news(symbol)
    print("Recent News Headlines:")
    for headline in headlines:
        print("-", headline)
if __name__ == "__main__":
    main()