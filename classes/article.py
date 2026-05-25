from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class NewsArticle:
    title: str
    url: str
    source: str
    category: str = "general"
    published_at: Optional[str] = None
    article_type: str = field(default="base", init=False)

    def __post_init__(self):
        self.title = (self.title or "Untitled Article").strip()
        self.url = (self.url or "").strip()
        self.source = (self.source or "Unknown Source").strip()
        self.category = (self.category or "general").strip().lower()
        self.published_at = (self.published_at or "").strip() or None

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "category": self.category,
            "published_at": self.published_at,
            "type": self.article_type,
        }

    def summary(self):
        return f"{self.title} ({self.source})"

    def short_title(self, max_length: int = 90) -> str:
        if len(self.title) <= max_length:
            return self.title
        return self.title[: max_length - 3].rstrip() + "..."

    def has_meaningful_content(self) -> bool:
        return False


@dataclass
class APIArticle(NewsArticle):
    description: Optional[str] = None
    url_to_image: Optional[str] = None
    author: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        self.description = (self.description or "").strip() or None
        self.url_to_image = (self.url_to_image or "").strip() or None
        self.author = (self.author or "").strip() or None
        self.article_type = "api"

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "description": self.description,
            "url_to_image": self.url_to_image,
            "author": self.author,
        })
        return data


@dataclass
class ScrapedArticle(APIArticle):
    content: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        self.content = (self.content or "").strip() or None
        self.article_type = "scraped"

    def to_dict(self):
        data = super().to_dict()
        data.update({"content": self.content})
        return data

    def has_meaningful_content(self) -> bool:
        return len((self.content or "").strip()) >= 80
