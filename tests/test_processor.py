import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.processor import DataProcessor
from classes.article import APIArticle, ScrapedArticle

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = DataProcessor()
        self.sample_articles = [
            ScrapedArticle(title="Article 1", url="https://a.com",
                          source="BBC", category="technology", author="Jane"),
            ScrapedArticle(title="Article 2", url="https://b.com",
                          source="CNN", category="sports", author="John"),
            ScrapedArticle(title="Article 1", url="https://a.com",
                          source="BBC", category="technology", author="Jane"),
        ]

    def test_initial_dataframe_is_empty(self):
        self.assertTrue(self.processor.dataframe.empty)

    def test_merge_creates_dataframe(self):
        self.processor.merge(self.sample_articles)
        self.assertFalse(self.processor.dataframe.empty)

    def test_merge_correct_row_count(self):
        self.processor.merge(self.sample_articles)
        self.assertEqual(len(self.processor.dataframe), 3)

    def test_remove_duplicates(self):
        self.processor.merge(self.sample_articles)
        self.processor.remove_duplicates()
        self.assertEqual(len(self.processor.dataframe), 2)

    def test_clean_fills_missing_title(self):
        articles = [ScrapedArticle(title=None, url="https://c.com", source="BBC")]
        self.processor.merge(articles)
        self.processor.clean()
        self.assertEqual(self.processor.dataframe["title"][0], "No title")

    def test_get_data_returns_dataframe(self):
        self.processor.merge(self.sample_articles)
        import pandas as pd
        self.assertIsInstance(self.processor.get_data(), pd.DataFrame)

if __name__ == "__main__":
    unittest.main()