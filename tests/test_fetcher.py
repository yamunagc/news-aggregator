import unittest
from unittest.mock import MagicMock

from classes.fetcher import NewsFetcher


class TestNewsFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = NewsFetcher()
        self.fetcher.client = MagicMock()

    def test_fetch_headlines_normalizes_invalid_category(self):
        self.fetcher.client.get_top_headlines.return_value = {
            "articles": [
                {
                    "title": "Sample title",
                    "description": "Sample description",
                    "url": "http://example.com",
                    "source": {"name": "Example Source"},
                    "publishedAt": "2026-05-25T10:00:00Z",
                    "author": "Author Name",
                }
            ]
        }

        articles = self.fetcher.fetch_headlines(category="invalid-category", page_size=5)

        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].category, "general")

    def test_fetch_headlines_raises_when_no_client(self):
        self.fetcher.client = None
        with self.assertRaises(RuntimeError):
            self.fetcher.fetch_headlines()

    def test_fetch_headlines_uses_cache(self):
        self.fetcher.client.get_top_headlines.return_value = {
            "articles": [
                {
                    "title": "Cached title",
                    "description": "Cached description",
                    "url": "http://example.com/1",
                    "source": {"name": "Example Source"},
                    "publishedAt": "2026-05-25T10:00:00Z",
                    "author": "Author Name",
                }
            ]
        }

        first = self.fetcher.fetch_headlines(category="general", page_size=5)
        second = self.fetcher.fetch_headlines(category="general", page_size=5)

        self.assertEqual(len(first), 1)
        self.assertEqual(len(second), 1)
        self.fetcher.client.get_top_headlines.assert_called_once()

    def test_fetch_all_categories_returns_unique_articles(self):
        self.fetcher.fetch_headlines = MagicMock(side_effect=[
            [MagicMock(title="A", url="u1"), MagicMock(title="B", url="u2")],
            [MagicMock(title="A", url="u1")],
            [],
            [],
            [],
            [],
            [],
        ])

        articles = self.fetcher.fetch_all_categories(total_limit=3)

        unique_keys = {(a.url, a.title) for a in articles}
        self.assertEqual(len(unique_keys), len(articles))


if __name__ == "__main__":
    unittest.main()
