import unittest
from unittest.mock import Mock, patch

from classes.article import APIArticle
from classes.scraper import Scraper


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = Scraper()

    def test_clean_author_rejects_dirty_byline(self):
        dirty = "1 day ago Share Save Add as preferred on Google Wedaeli Chibelushi and Thomas Naadi, BBC Africa"
        cleaned = self.scraper._clean_author(dirty)

        self.assertNotIn("Share", cleaned)
        self.assertNotIn("Google", cleaned)

    def test_choose_best_content_uses_fallback_message(self):
        result = self.scraper._choose_best_content("", "Short API description")
        self.assertIn("Short API description", result)
        self.assertIn("Full article content is unavailable", result)

    @patch("classes.scraper.requests.get")
    def test_scrape_article_uses_api_fallback_when_scrape_fails(self, mock_get):
        mock_get.side_effect = Exception("Network error")

        article = APIArticle(
            title="Fallback test",
            url="http://example.com",
            source="BBC",
            category="general",
            published_at="2026-05-25",
            description="API summary here",
            author="",
            url_to_image=None,
        )

        result = self.scraper.scrape_article(article)

        self.assertEqual(result.title, "Fallback test")
        self.assertIn("API summary here", result.content)

    @patch("classes.scraper.requests.get")
    def test_scrape_article_extracts_clean_paragraphs(self, mock_get):
        html = """
        <html>
            <body>
                <article>
                    <p>Share Save Add as preferred on Google</p>
                    <p>This is the first proper paragraph of the article with enough length.</p>
                    <p>This is the second proper paragraph with useful story content.</p>
                </article>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        article = APIArticle(
            title="Scrape test",
            url="http://example.com",
            source="BBC",
            category="general",
            published_at="2026-05-25",
            description="API summary",
            author="",
            url_to_image=None,
        )

        result = self.scraper.scrape_article(article)

        self.assertIn("first proper paragraph", result.content.lower())
        self.assertNotIn("Add as preferred on Google", result.content)


if __name__ == "__main__":
    unittest.main()
