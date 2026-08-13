import unittest
from unittest.mock import patch

from main import app


class SearchRoutesTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_query_search_redirects_to_keyword_page(self):
        response = self.client.get("/search?keyword=java")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/search/java")

    def test_query_search_redirects_unknown_keyword_to_not_found(self):
        response = self.client.get("/search?keyword=ruby")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/not-found")

    @patch("main.Scraper")
    def test_keyword_page_groups_results_by_site(self, scraper_class):
        scraper_class.return_value.search.side_effect = [
            [
                {
                    "title": "Java Developer",
                    "company_name": "Acme",
                    "job_url": "https://example.com/berlin",
                }
            ],
            [
                {
                    "title": "Backend Engineer",
                    "company_name": "Orbit",
                    "job_url": "https://example.com/web3",
                }
            ],
            [],
        ]

        response = self.client.get("/search/java")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(scraper_class.call_count, 3)
        scraper_class.assert_any_call("java", "berlinstartupjobs")
        scraper_class.assert_any_call("java", "web3career")
        scraper_class.assert_any_call("java", "weworkremotely")
        self.assertNotIn(b'Recruting Site', response.data)
        self.assertIn("총 2개의 채용공고".encode(), response.data)
        self.assertIn(b"Berlin Startup Jobs", response.data)
        self.assertIn(b"Web3 Career", response.data)
        self.assertIn(b"WeWorkRemotely", response.data)
        self.assertIn(b"https://example.com/berlin", response.data)
        self.assertIn(b"https://example.com/web3", response.data)


if __name__ == "__main__":
    unittest.main()
