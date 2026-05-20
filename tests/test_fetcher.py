import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.fetcher import NewsFetcher

class TestNewsFetcher(unittest.TestCase):

    def setUp(self):
        self.fetcher = NewsFetcher()

    def test_valid_categories_has_seven(self):
        self.assertEqual(len(NewsFetcher.VALID_CATEGORIES), 7)

    def test_technology_is_valid_category(self):
        self.assertIn("technology", NewsFetcher.VALID_CATEGORIES)

    def test_sports_is_valid_category(self):
        self.assertIn("sports", NewsFetcher.VALID_CATEGORIES)

    def test_fetcher_has_api_key(self):
        self.assertIsNotNone(self.fetcher.api_key)

    def test_fetcher_has_base_url(self):
        self.assertIn("newsapi.org", self.fetcher.base_url)

if __name__ == "__main__":
    unittest.main()