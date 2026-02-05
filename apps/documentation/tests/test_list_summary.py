import json
from unittest.mock import Mock, patch

from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class ListSummaryResponsesTestCase(TestCase):
    """
    Verifies list endpoints return summary items by default,
    and `?expand=full` returns full documents.
    """

    @patch("apps.documentation.api.v1.pages_views.get_pages_service")
    def test_api_v1_pages_list_summary_default_and_expand_full(self, mock_get_pages_service):
        mock_service = Mock()
        mock_get_pages_service.return_value = mock_service
        mock_service.list_pages.return_value = {
            "pages": [
                {"page_id": "page1", "page_type": "docs", "metadata": {"title": "T1", "status": "published"}},
                {"page_id": "page2", "page_type": "docs", "metadata": {"title": "T2", "status": "draft"}},
            ],
            "total": 2,
        }

        # Default: summary items
        resp = self.client.get("/api/v1/pages/")
        self.assertEqual(resp.status_code, 200)
        payload = json.loads(resp.content)
        self.assertIn("pages", payload)
        self.assertEqual(len(payload["pages"]), 2)
        self.assertIn("page_id", payload["pages"][0])
        self.assertNotIn("metadata", payload["pages"][0])

        # expand=full: full documents
        resp_full = self.client.get("/api/v1/pages/?expand=full")
        self.assertEqual(resp_full.status_code, 200)
        payload_full = json.loads(resp_full.content)
        self.assertIn("metadata", payload_full["pages"][0])

    @patch("apps.documentation.api.v1.core.get_pages_service")
    def test_docs_dashboard_pages_summary_default_and_expand_full(self, mock_get_pages_service):
        # Dashboard list is now /api/v1/dashboard/pages/ (response: success, data, meta.pagination).
        user = User.objects.create(username="testuser")
        self.client.force_login(user)

        mock_service = Mock()
        mock_get_pages_service.return_value = mock_service
        mock_service.list_pages.return_value = {
            "pages": [
                {"page_id": "page1", "page_type": "docs", "metadata": {"title": "T1", "status": "published"}},
            ],
            "total": 1,
            "source": "local",
        }

        # Default: summary items (API v1 returns data + meta.pagination)
        resp = self.client.get("/api/v1/dashboard/pages/?page=1&page_size=20")
        self.assertEqual(resp.status_code, 200)
        payload = json.loads(resp.content)
        self.assertIn("data", payload)
        self.assertIn("meta", payload)
        self.assertIn("pagination", payload["meta"])
        self.assertEqual(len(payload["data"]), 1)
        self.assertIn("page_id", payload["data"][0])
        self.assertNotIn("metadata", payload["data"][0])

        # expand=full: full documents
        resp_full = self.client.get("/api/v1/dashboard/pages/?page=1&page_size=20&expand=full")
        self.assertEqual(resp_full.status_code, 200)
        payload_full = json.loads(resp_full.content)
        self.assertIn("data", payload_full)
        self.assertIn("metadata", payload_full["data"][0])

