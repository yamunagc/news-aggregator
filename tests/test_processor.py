import unittest

from classes.article import ScrapedArticle
from classes.processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = DataProcessor()

    def test_merge_and_dataframe_creation(self):
        articles = [
            ScrapedArticle(
                title="AI changes healthcare",
                description="desc",
                url="http://a.com",
                source="BBC News",
                published_at="2026-05-25",
                author="John Doe",
                category="health",
                content="AI is changing healthcare systems.",
            )
        ]

        self.processor.merge(articles)
        df = self.processor.get_data()

        self.assertEqual(len(df), 1)
        self.assertIn("title", df.columns)
        self.assertIn("content_length", df.columns)

    def test_remove_duplicates(self):
        articles = [
            ScrapedArticle(
                title="Same title",
                description="desc1",
                url="http://same.com",
                source="BBC",
                published_at="2026-05-25",
                author="A",
                category="general",
                content="content 1",
            ),
            ScrapedArticle(
                title="Same title",
                description="desc2",
                url="http://same.com",
                source="BBC",
                published_at="2026-05-25",
                author="B",
                category="general",
                content="content 2",
            ),
        ]

        self.processor.merge(articles)
        self.processor.remove_duplicates()
        df = self.processor.get_data()

        self.assertEqual(len(df), 1)

    def test_clean_invalid_author_becomes_unknown(self):
        articles = [
            ScrapedArticle(
                title="Ebola article",
                description="desc",
                url="http://bbc.com/example",
                source="BBC News",
                published_at="2026-05-25",
                author="1 day ago Share Save Add as preferred on Google Wedaeli Chibelushi and Thomas Naadi, BBC Africa",
                category="health",
                content="The article body is valid and long enough for testing.",
            )
        ]

        self.processor.merge(articles)
        self.processor.clean()
        cleaned = self.processor.get_articles()[0]

        self.assertEqual(cleaned.author, "Unknown")

    def test_clean_content_removes_noise(self):
        articles = [
            ScrapedArticle(
                title="News title",
                description="Short description",
                url="http://news.com",
                source="BBC News",
                published_at="2026-05-25",
                author="By John Doe",
                category="Health",
                content="Share Save Add as preferred on Google The outbreak is growing rapidly.",
            )
        ]

        self.processor.merge(articles)
        self.processor.clean()
        data = self.processor.get_articles()[0]

        self.assertEqual(data.category, "health")
        self.assertIn("The outbreak is growing rapidly.", data.content)
        self.assertNotIn("Share", data.content)

    def test_summary_generation(self):
        articles = [
            ScrapedArticle(
                title="Article one",
                description="desc",
                url="http://1.com",
                source="BBC",
                published_at="2026-05-25",
                author="Jane",
                category="health",
                content="content",
            ),
            ScrapedArticle(
                title="Article two",
                description="desc",
                url="http://2.com",
                source="CNN",
                published_at="2026-05-25",
                author="Jane",
                category="science",
                content="content",
            ),
        ]

        self.processor.merge(articles)
        self.processor.clean()
        summary = self.processor.get_summary()

        self.assertEqual(summary["total_articles"], 2)
        self.assertEqual(summary["unique_sources"], 2)
        self.assertEqual(summary["unique_categories"], 2)


if __name__ == "__main__":
    unittest.main()
