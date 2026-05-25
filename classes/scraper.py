from __future__ import annotations

import re
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup

from classes.article import APIArticle, ScrapedArticle


class Scraper:
    def __init__(self, timeout: int = 12):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

    def scrape_article(self, api_article: APIArticle) -> ScrapedArticle:
        text = ""
        author = api_article.author or ""
        published_at = api_article.published_at or ""

        if api_article.url:
            try:
                response = requests.get(api_article.url, headers=self.headers, timeout=self.timeout)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")

                if not author:
                    author = self._extract_author(soup)
                if not published_at:
                    published_at = self._extract_published_date(soup)

                text = self._extract_article_text(soup)
            except Exception:
                text = ""

        final_text = self._choose_best_content(text, api_article.description)

        return ScrapedArticle(
            title=api_article.title,
            description=api_article.description,
            url=api_article.url,
            source=api_article.source,
            published_at=published_at,
            author=author or "Unknown",
            category=api_article.category,
            content=final_text,
        )

    def scrape_all(self, api_articles: Iterable[APIArticle], limit: int | None = None) -> List[ScrapedArticle]:
        results: List[ScrapedArticle] = []
        items = list(api_articles)
        if limit is not None:
            items = items[:limit]
        for article in items:
            results.append(self.scrape_article(article))
        return results

    def _extract_author(self, soup: BeautifulSoup) -> str:
        selectors = [
            'meta[name="author"]',
            'meta[property="article:author"]',
            '[rel="author"]',
            '.author',
            '.byline',
            '[data-component="byline-block"]',
            '[data-testid="byline"]',
        ]

        for selector in selectors:
            node = soup.select_one(selector)
            if not node:
                continue

            if node.name == "meta":
                value = (node.get("content") or "").strip()
            else:
                value = " ".join(node.get_text(" ", strip=True).split())

            value = self._clean_author(value)
            if self._is_valid_author(value):
                return value

        return ""

    def _extract_published_date(self, soup: BeautifulSoup) -> str:
        selectors = [
            'meta[property="article:published_time"]',
            'meta[name="pubdate"]',
            'meta[name="publish-date"]',
            'time[datetime]',
        ]
        for selector in selectors:
            node = soup.select_one(selector)
            if not node:
                continue
            if node.name == "meta":
                value = (node.get("content") or "").strip()
            else:
                value = (node.get("datetime") or node.get_text(" ", strip=True) or "").strip()
            if value:
                return value
        return ""

    def _extract_article_text(self, soup: BeautifulSoup) -> str:
        selectors = [
            'article p',
            'main article p',
            '[data-component="text-block"] p',
            '[data-testid="story-body"] p',
            '.story-body__inner p',
            'main p',
        ]

        paragraphs: List[str] = []
        for selector in selectors:
            nodes = soup.select(selector)
            candidate_paragraphs = []
            for node in nodes:
                text = self._clean_article_text(node.get_text(" ", strip=True))
                if self._is_good_paragraph(text):
                    candidate_paragraphs.append(text)
            if len(candidate_paragraphs) >= 2:
                paragraphs = candidate_paragraphs
                break
            if candidate_paragraphs and not paragraphs:
                paragraphs = candidate_paragraphs

        if not paragraphs:
            fallback_nodes = soup.find_all(["p"])
            for node in fallback_nodes:
                text = self._clean_article_text(node.get_text(" ", strip=True))
                if self._is_good_paragraph(text):
                    paragraphs.append(text)

        paragraphs = self._deduplicate_preserve_order(paragraphs)
        paragraphs = self._drop_noisy_leading_paragraphs(paragraphs)

        return "\n\n".join(paragraphs).strip()

    def _choose_best_content(self, scraped_text: str, api_description: str | None) -> str:
        scraped_text = self._clean_article_text(scraped_text)
        api_description = self._clean_article_text(api_description or "")

        if scraped_text and len(scraped_text) > 300:
            return scraped_text
        if scraped_text and len(scraped_text) > 80 and api_description and api_description.lower() not in scraped_text.lower():
            return f"{api_description}\n\n{scraped_text}"
        if api_description:
            return f"{api_description}\n\nFull article content is unavailable for this source. Open the source link to read more."
        if scraped_text:
            return scraped_text
        return "Full article content is unavailable for this source. Open the source link to read more."

    def _clean_author(self, text: str) -> str:
        text = " ".join((text or "").split()).strip()
        text = re.sub(r"^By\s+", "", text, flags=re.I)

        text = re.sub(r"\bShare\b", "", text, flags=re.I)
        text = re.sub(r"\bSave\b", "", text, flags=re.I)
        text = re.sub(r"\bAdd as preferred on Google\b", "", text, flags=re.I)
        text = re.sub(r"\b\d+\s+day[s]?\s+ago\b", "", text, flags=re.I)
        text = re.sub(r"\b\d+\s+hour[s]?\s+ago\b", "", text, flags=re.I)
        text = re.sub(r"\b\d+\s+minute[s]?\s+ago\b", "", text, flags=re.I)
        text = re.sub(r"\bBBC Africa\b", "", text, flags=re.I)
        text = re.sub(r"\bBBC News\b", "", text, flags=re.I)
        text = re.sub(r"\bReuters\b", "", text, flags=re.I)
        text = re.sub(r"\s+", " ", text).strip(" ,:-")
        return text

    def _is_valid_author(self, text: str) -> bool:
        if not text:
            return False

        lowered = text.lower()
        bad_tokens = [
            "share", "save", "google", "advertisement", "comment", "photo",
            "getty", "day ago", "hour ago", "minute ago", "most read"
        ]
        if any(token in lowered for token in bad_tokens):
            return False

        if len(text) > 80:
            return False

        if len(text.split()) > 10:
            return False

        alpha_count = sum(ch.isalpha() for ch in text)
        return alpha_count >= 3

    def _clean_article_text(self, text: str) -> str:
        if not text:
            return ""

        text = text.replace("\xa0", " ")
        text = " ".join(text.split())

        noise_phrases = [
            "Share",
            "Save",
            "Add as preferred on Google",
            "Comment",
            "Advertisement",
            "Read more",
            "Most read",
            "Related topics",
            "Skip to content",
            "Live",
        ]
        for phrase in noise_phrases:
            text = re.sub(rf"\b{re.escape(phrase)}\b", "", text, flags=re.I)

        patterns = [
            r"\b\d+\s+day[s]?\s+ago\b",
            r"\b\d+\s+hour[s]?\s+ago\b",
            r"\b\d+\s+minute[s]?\s+ago\b",
            r"\bAFP via Getty Images\b",
            r"\bAP via Getty Images\b",
            r"\bGetty Images\b",
            r"\bBBC News,?\b",
            r"\bPhoto caption,?\b",
            r"\bImage source,?\b",
        ]
        for pattern in patterns:
            text = re.sub(pattern, "", text, flags=re.I)

        text = re.sub(r"\s+", " ", text).strip(" -,:;|")
        return text

    def _is_good_paragraph(self, text: str) -> bool:
        if not text or len(text) < 40:
            return False

        lowered = text.lower()
        noisy_tokens = [
            "share save",
            "add as preferred on google",
            "most read",
            "related topics",
            "advertisement",
            "cookie",
            "subscribe",
            "sign up",
            "newsletter",
        ]
        if any(token in lowered for token in noisy_tokens):
            return False

        alpha_count = sum(ch.isalpha() for ch in text)
        return alpha_count >= 25

    def _drop_noisy_leading_paragraphs(self, paragraphs: List[str]) -> List[str]:
        cleaned = list(paragraphs)
        while cleaned:
            first = cleaned[0].lower()
            if any(token in first for token in ["share", "save", "google", "getty images", "photo caption", "most read"]):
                cleaned.pop(0)
            else:
                break
        return cleaned

    def _deduplicate_preserve_order(self, items: List[str]) -> List[str]:
        seen = set()
        result = []
        for item in items:
            key = item.strip().lower()
            if not key or key in seen:
                continue
            seen.add(key)
            result.append(item.strip())
        return result
