import os
import requests
from dotenv import load_dotenv
from .article import APIArticle

load_dotenv()

class NewsFetcher:

    VALID_CATEGORIES = [
        "business", "entertainment", "general",
        "health", "science", "sports", "technology"
    ]

    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2"

    def fetch_headlines(self, category="general", page_size=20):
        url = f"{self.base_url}/top-headlines"
        params = {
            "category": category,
            "pageSize": page_size,
            "language": "en",
            "apiKey": self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        articles = []
        for item in data.get("articles", []):
            article = APIArticle(
                title=item.get("title"),
                url=item.get("url"),
                source=item.get("source", {}).get("name"),
                category=category,
                published_at=item.get("publishedAt"),
                description=item.get("description"),
                url_to_image=item.get("urlToImage")
            )
            articles.append(article)
        return articles

    def fetch_by_source(self, source, page_size=20):
        url = f"{self.base_url}/top-headlines"
        params = {
            "sources": source,
            "pageSize": page_size,
            "apiKey": self.api_key
        }
        response = requests.get(url, params=params)
        data = response.json()

        articles = []
        for item in data.get("articles", []):
            article = APIArticle(
                title=item.get("title"),
                url=item.get("url"),
                source=item.get("source", {}).get("name"),
                published_at=item.get("publishedAt"),
                description=item.get("description"),
                url_to_image=item.get("urlToImage")
            )
            articles.append(article)
        return articles
    
    def fetch_all_categories(self, page_size=5):
        all_articles = []
        for category in self.VALID_CATEGORIES:
            try:
                articles = self.fetch_headlines(category, page_size)
                all_articles.extend(articles)
            except Exception as e:
                print(f"Could not fetch {category}: {e}")
        return all_articles