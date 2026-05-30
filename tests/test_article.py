import unittest

from classes.article import APIArticle, NewsArticle, ScrapedArticle


class TestNewsArticle(unittest.TestCase):
    def test_news_article_defaults(self):
        article = NewsArticle(title=None, url="https://example.com", source=None)
        self.assertEqual(article.title, "Untitled Article")
        self.assertEqual(article.source, "Unknown Source")

    def test_api_article_type(self):
        article = APIArticle(title="A", url="https://example.com", source="BBC")
        self.assertEqual(article.to_dict()["type"], "api")

    def test_scraped_article_type(self):
        article = ScrapedArticle(title="A", url="https://example.com", source="BBC")
        self.assertEqual(article.to_dict()["type"], "scraped")
