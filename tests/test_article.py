import unittest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.article import NewsArticle, APIArticle, ScrapedArticle

class TestNewsArticle(unittest.TestCase):

    def test_newsarticle_stores_title(self):
        a = NewsArticle(title="Test", url="https://x.com", source="BBC")
        self.assertEqual(a.title, "Test")

    def test_newsarticle_to_dict_has_all_keys(self):
        a = NewsArticle(title="Test", url="https://x.com", source="BBC")
        d = a.to_dict()
        self.assertIn("title", d)
        self.assertIn("url", d)
        self.assertIn("source", d)

    def test_api_article_inherits_newsarticle(self):
        a = APIArticle(title="API", url="https://x.com", source="CNN")
        self.assertIsInstance(a, NewsArticle)

    def test_api_article_type_is_api(self):
        a = APIArticle(title="API", url="https://x.com", source="CNN")
        self.assertEqual(a.to_dict()["type"], "api")

    def test_scraped_article_inherits_newsarticle(self):
        a = ScrapedArticle(title="Scraped", url="https://y.com", source="BBC")
        self.assertIsInstance(a, NewsArticle)

    def test_scraped_article_type_is_scraped(self):
        a = ScrapedArticle(title="Scraped", url="https://y.com", source="BBC")
        self.assertEqual(a.to_dict()["type"], "scraped")

    def test_scraped_article_stores_author(self):
        a = ScrapedArticle(title="T", url="https://y.com",
                           source="BBC", author="Jane Doe")
        self.assertEqual(a.author, "Jane Doe")

if __name__ == "__main__":
    unittest.main()