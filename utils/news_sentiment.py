# utils/news_sentiment.py
import requests
from textblob import TextBlob

NEWS_API_KEY = "your_news_api_key"  # Replace this

def fetch_market_news():
    url = f"https://newsapi.org/v2/everything?q=stock market&language=en&sortBy=publishedAt&pageSize=15&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    return articles

def analyze_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"
