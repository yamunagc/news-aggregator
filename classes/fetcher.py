from __future__ import annotations

import os
import time
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from newsapi import NewsApiClient

from classes.article import APIArticle


class NewsFetcher:
    VALID_CATEGORIES = [
        "business",
        "entertainment",
        "general",
        "health",
        "science",
        "sports",
        "technology",
    ]

    def __init__(self, cache_ttl: int = 300):
        load_dotenv()
        self.api_key = os.getenv("NEWS_API_KEY", "").strip()
        self.client = NewsApiClient(api_key=self.api_key) if self.api_key else None
        self.cache_ttl = cache_ttl
        self._cache: Dict[Tuple[str, str, int], Tuple[float, List[APIArticle]]] = {}

    def _get_cached(self, key):
        cached = self._cache.get(key)
        if not cached:
            return None
        ts, data = cached
        if time.time() - ts <= self.cache_ttl:
            return data
        self._cache.pop(key, None)
        return None

    def _set_cache(self, key, data):
        self._cache[key] = (time.time(), data)

    def _to_articles(self, payload: dict, category: str) -> List[APIArticle]:
        results = []
        for item in payload.get("articles", []):
            title = (item.get("title") or "").strip()
            if not title:
                continue
            source = (item.get("source") or {}).get("name") or "Unknown"
            article = APIArticle(
                title=title,
                description=(item.get("description") or "").strip(),
                url=(item.get("url") or "").strip(),
                source=source,
                published_at=(item.get("publishedAt") or "").strip(),
                author=(item.get("author") or "").strip(),
                category=category,
            )
            results.append(article)
        return results

    def fetch_headlines(self, category: str = "general", page_size: int = 10) -> List[APIArticle]:
        category = (category or "general").lower()
        if category not in self.VALID_CATEGORIES:
            category = "general"
        page_size = max(1, min(int(page_size), 50))

        key = ("top", category, page_size)
        cached = self._get_cached(key)
        if cached is not None:
            return cached

        if not self.client:
            raise RuntimeError("NEWS_API_KEY is missing. Please add it to the .env file.")

        try:
            payload = self.client.get_top_headlines(
                language="en",
                category=category,
                page_size=page_size,
            )
            data = self._to_articles(payload, category)
            if not data:
                raise RuntimeError(f"No articles returned for category '{category}'.")
        except Exception as exc:
            raise RuntimeError(f"Failed to fetch news from NewsAPI: {exc}")

        self._set_cache(key, data)
        return data

    def fetch_all_categories(self, total_limit: int = 10) -> List[APIArticle]:
        total_limit = max(1, int(total_limit))
        categories = list(self.VALID_CATEGORIES)
        per_category = max(1, total_limit // len(categories))

        collected: List[APIArticle] = []
        for category in categories:
            try:
                collected.extend(self.fetch_headlines(category=category, page_size=per_category))
            except RuntimeError:
                continue

        if not collected:
            raise RuntimeError("No articles could be fetched from any category.")

        idx = 0
        while len(collected) < total_limit and idx < len(categories):
            try:
                collected.extend(self.fetch_headlines(category=categories[idx], page_size=per_category + 1))
            except RuntimeError:
                pass
            idx += 1

        unique = []
        seen = set()
        for article in collected:
            key = ((article.url or "").strip().lower(), (article.title or "").strip().lower())
            if key in seen:
                continue
            seen.add(key)
            unique.append(article)

        return unique[:total_limit]
