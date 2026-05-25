from __future__ import annotations

import re
from typing import Iterable, List

import pandas as pd

from classes.article import NewsArticle


class DataProcessor:
    def __init__(self):
        self._articles: List[NewsArticle] = []
        self._df = pd.DataFrame()

    def merge(self, articles: Iterable[NewsArticle]) -> None:
        if not articles:
            return
        self._articles.extend(list(articles))
        self._refresh_dataframe()

    def clear(self) -> None:
        self._articles = []
        self._df = pd.DataFrame()

    def remove_duplicates(self) -> None:
        seen = set()
        unique_articles = []

        for article in self._articles:
            title = self._clean_text(article.title).lower()
            url = (article.url or "").strip().lower()
            key = (title, url)

            if key in seen:
                continue
            seen.add(key)
            unique_articles.append(article)

        self._articles = unique_articles
        self._refresh_dataframe()

    def clean(self) -> None:
        cleaned_articles = []

        for article in self._articles:
            article.title = self._clean_text(article.title)
            article.description = self._clean_text(article.description)
            article.content = self._clean_content(article.content or article.description)
            article.source = self._clean_source(article.source)
            article.author = self._clean_author(article.author)
            article.category = self._clean_category(article.category)
            article.published_at = self._clean_text(article.published_at)
            article.url = (article.url or "").strip()

            if not article.title:
                continue

            cleaned_articles.append(article)

        self._articles = cleaned_articles
        self._refresh_dataframe()

    def get_articles(self) -> List[NewsArticle]:
        return list(self._articles)

    def get_data(self) -> pd.DataFrame:
        return self._df.copy()

    def get_summary(self) -> dict:
        if self._df.empty:
            return {
                "total_articles": 0,
                "unique_sources": 0,
                "unique_categories": 0,
                "top_source": "N/A",
                "top_category": "N/A",
            }

        top_source = self._df["source"].value_counts().idxmax() if "source" in self._df.columns else "N/A"
        top_category = self._df["category"].value_counts().idxmax() if "category" in self._df.columns else "N/A"

        return {
            "total_articles": int(len(self._df)),
            "unique_sources": int(self._df["source"].nunique()) if "source" in self._df.columns else 0,
            "unique_categories": int(self._df["category"].nunique()) if "category" in self._df.columns else 0,
            "top_source": top_source,
            "top_category": top_category,
        }

    def _refresh_dataframe(self) -> None:
        rows = []
        for article in self._articles:
            rows.append(
                {
                    "title": article.title,
                    "description": article.description,
                    "content": article.content,
                    "source": article.source,
                    "author": article.author,
                    "category": article.category,
                    "published_at": article.published_at,
                    "url": article.url,
                    "content_length": len((article.content or "").strip()),
                    "title_word_count": len((article.title or "").split()),
                }
            )

        self._df = pd.DataFrame(rows)

    def _clean_text(self, text: str | None) -> str:
        if not text:
            return ""
        text = text.replace("\xa0", " ")
        text = " ".join(str(text).split())
        return text.strip()

    def _clean_source(self, source: str | None) -> str:
        source = self._clean_text(source)
        return source if source else "Unknown"

    def _clean_author(self, author: str | None) -> str:
        author = self._clean_text(author)
        if not author:
            return "Unknown"

        author = re.sub(r"^By\s+", "", author, flags=re.I)
        author = re.sub(r"\s+", " ", author).strip(" ,:-")

        bad_patterns = [
            r"\bshare\b",
            r"\bsave\b",
            r"\bgoogle\b",
            r"\bcomment\b",
            r"\badvertisement\b",
            r"\bmost read\b",
            r"\brelated topics\b",
            r"\bgetty\b",
            r"\bphoto\b",
            r"\bbbc africa\b",
            r"\b\d+\s+day[s]?\s+ago\b",
            r"\b\d+\s+hour[s]?\s+ago\b",
            r"\b\d+\s+minute[s]?\s+ago\b",
        ]

        lowered = author.lower()
        for pattern in bad_patterns:
            if re.search(pattern, lowered, flags=re.I):
                return "Unknown"

        news_org_only = [
            "reuters",
            "associated press",
            "bbc news",
            "cnn",
            "the washington post",
        ]
        if lowered in news_org_only:
            return "Unknown"

        if len(author) > 80:
            return "Unknown"

        word_count = len(author.split())
        if word_count > 10:
            return "Unknown"

        letters_only = re.sub(r"[^A-Za-z ,.'-]", "", author).strip()
        if not letters_only:
            return "Unknown"

        if sum(ch.isalpha() for ch in letters_only) < 3:
            return "Unknown"

        return letters_only if letters_only else "Unknown"

    def _clean_category(self, category: str | None) -> str:
        category = self._clean_text(category).lower()
        return category if category else "general"

    def _clean_content(self, content: str | None) -> str:
        if not content:
            return "No content available."

        text = str(content).replace("\r\n", "\n").replace("\r", "\n")
        text = text.replace("\xa0", " ")
        text = "\n".join(line.strip() for line in text.split("\n"))
        text = "\n".join(line for line in text.split("\n") if line)

        noise_patterns = [
            r"\bShare\b",
            r"\bSave\b",
            r"\bAdd as preferred on Google\b",
            r"\bAdvertisement\b",
            r"\bRead more\b",
            r"\bMost read\b",
            r"\bRelated topics\b",
            r"\bComment\b",
            r"\b\d+\s+day[s]?\s+ago\b",
            r"\b\d+\s+hour[s]?\s+ago\b",
            r"\bGetty Images\b",
            r"\bAFP via Getty Images\b",
            r"\bAP via Getty Images\b",
        ]

        cleaned_lines = []
        for line in text.split("\n"):
            current = line
            for pattern in noise_patterns:
                current = re.sub(pattern, "", current, flags=re.I)
            current = re.sub(r"\s+", " ", current).strip(" -,:;|")
            if len(current) >= 20:
                cleaned_lines.append(current)

        cleaned_lines = self._deduplicate_lines(cleaned_lines)
        cleaned = "\n\n".join(cleaned_lines).strip()

        return cleaned if cleaned else "Full article content is unavailable for this source."

    def _deduplicate_lines(self, lines: List[str]) -> List[str]:
        seen = set()
        result = []

        for line in lines:
            key = line.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            result.append(line.strip())

        return result
