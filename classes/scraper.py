import requests
from bs4 import BeautifulSoup
from .article import ScrapedArticle

class Scraper:

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    def scrape_article(self, article):
        try:
            response = requests.get(
                article.url, headers=self.HEADERS, timeout=10
            )
            soup = BeautifulSoup(response.text, "lxml")

            # extract author (multiple fallback strategies)
            author = None

            # try 1: meta tag
            tag = soup.find("meta", {"name": "author"})
            if tag:
                author = tag.get("content")

            # try 2: meta property
            if not author:
                tag = soup.find("meta", {"property": "article:author"})
                if tag:
                    author = tag.get("content")

            # try 3: common class names
            if not author:
                for selector in ["author", "byline", "article-author",
                                  "post-author", "entry-author"]:
                    tag = soup.find(class_=selector)
                    if tag:
                        author = tag.get_text(strip=True)
                        break

            # try 4: rel="author" link
            if not author:
                tag = soup.find("a", {"rel": "author"})
                if tag:
                    author = tag.get_text(strip=True)

            # --- extract content (multiple fallback strategies) ---
            content = None

            # try 1: <article> tag
            tag = soup.find("article")
            if tag:
                content = tag.get_text(separator=" ", strip=True)[:2000]

            # try 2: <main> tag
            if not content:
                tag = soup.find("main")
                if tag:
                    content = tag.get_text(separator=" ", strip=True)[:2000]

            # try 3: common content class names
            if not content:
                for selector in ["article-body", "post-content",
                                  "entry-content", "story-body",
                                  "article-content"]:
                    tag = soup.find(class_=selector)
                    if tag:
                        content = tag.get_text(separator=" ", strip=True)[:2000]
                        break

            # try 4: grab all paragraphs as last resort
            if not content:
                paragraphs = soup.find_all("p")
                if paragraphs:
                    content = " ".join(
                        p.get_text(strip=True) for p in paragraphs[:10]
                    )[:2000]

            return ScrapedArticle(
                title=article.title,
                url=article.url,
                source=article.source,
                category=article.category,
                published_at=article.published_at,
                author=author,
                content=content
            )

        except Exception as e:
            print(f"Could not scrape {article.url}: {e}")
            return None

    def scrape_all(self, articles):
        scraped = []
        for article in articles:
            result = self.scrape_article(article)
            if result:
                scraped.append(result)
        return scraped