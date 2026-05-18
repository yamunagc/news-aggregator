class NewsArticle:
    def __init__(self, title, url, source, category="general", published_at=None):
        self.title = title
        self.url = url
        self.source = source
        self.category = category
        self.published_at = published_at

    def to_dict(self):
        return {
            "title": self.title,
            "url": self.url,
            "source": self.source,
            "category": self.category,
            "published_at": self.published_at,
        }

    def __repr__(self):
        return f"{self.__class__.__name__}(title={self.title!r})"


class APIArticle(NewsArticle):
    def __init__(self, title, url, source, category="general",
                 published_at=None, description=None, url_to_image=None):
        super().__init__(title, url, source, category, published_at)
        self.description = description
        self.url_to_image = url_to_image

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "description": self.description,
            "url_to_image": self.url_to_image,
            "type": "api",
        })
        return data


class ScrapedArticle(NewsArticle):
    def __init__(self, title, url, source, category="general",
                 published_at=None, author=None, content=None):
        super().__init__(title, url, source, category, published_at)
        self.author = author
        self.content = content

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "author": self.author,
            "content": self.content,
            "type": "scraped",
        })
        return data