"""
Integration tests for mounted ``/api/v1/*`` JSON routes (Lambda-parity + DRF dashboard).

Uses URLs and response shapes from ``apps.documentation.api.v1.*`` — not the unused
``api/v1/core.py`` helpers (those are legacy/unmounted).
"""

from __future__ import annotations

import json
from unittest.mock import Mock, patch

from django.test import Client, TestCase
from django.urls import reverse

from apps.documentation.tests.helpers import create_test_user


class V1PublicRoutesTests(TestCase):
    """Health and service_info allow unauthenticated GET."""

    def setUp(self) -> None:
        self.client = Client()

    def test_service_info(self) -> None:
        r = self.client.get(reverse("api_v1:service_info"))
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data.get("status"), "ok")
        self.assertIn("service", data)

    def test_health_summary(self) -> None:
        r = self.client.get(reverse("api_v1:health"))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json().get("status"), "ok")


class V1DashboardTests(TestCase):
    """DRF dashboard slices under /api/v1/dashboard/ (requires login — ``IsAuthenticated``)."""

    def setUp(self) -> None:
        self.client = Client()
        user = create_test_user()
        self.client.force_login(user)

    @patch("apps.documentation.api.v1.views.get_adapter")
    def test_dashboard_pages(self, mock_get_adapter: Mock) -> None:
        ad = Mock()
        mock_get_adapter.return_value = ad
        ad.list_pages.return_value = {"pages": [{"page_id": "p1"}], "total": 1}
        r = self.client.get("/api/v1/dashboard/pages/")
        self.assertEqual(r.status_code, 200)
        body = r.json()
        self.assertIn("items", body)
        self.assertIn("pageInfo", body)

    @patch("apps.documentation.api.v1.views.get_adapter")
    def test_dashboard_endpoints(self, mock_get_adapter: Mock) -> None:
        ad = Mock()
        mock_get_adapter.return_value = ad
        ad.list_endpoints.return_value = {
            "endpoints": [{"endpoint_id": "e1"}],
            "total": 1,
        }
        r = self.client.get("/api/v1/dashboard/endpoints/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("items", r.json())


class V1PagesRoutesTests(TestCase):
    """``api_v1_pages`` URLconf — GraphQL adapter."""

    def setUp(self) -> None:
        self.client = Client()

    @patch("apps.documentation.api.v1.pages_views.get_adapter")
    def test_pages_list(self, mock_get_adapter: Mock) -> None:
        ad = Mock()
        mock_get_adapter.return_value = ad
        ad.list_pages.return_value = {"pages": [{"page_id": "a"}], "total": 1}
        url = reverse("api_v1:api_v1_pages:pages_list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content.decode())
        self.assertIn("pages", data)
        self.assertEqual(data["total"], 1)

    @patch("apps.documentation.api.v1.pages_views.get_adapter")
    def test_pages_detail_segment(self, mock_get_adapter: Mock) -> None:
        ad = Mock()
        mock_get_adapter.return_value = ad
        ad.get_page.return_value = {"page_id": "seg1", "title": "T"}
        url = reverse(
            "api_v1:api_v1_pages:pages_user_type_or_detail",
            kwargs={"segment": "seg1"},
        )
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.content.decode()).get("page_id"), "seg1")


class V1EndpointsRoutesTests(TestCase):
    """``api_v1_endpoints`` URLconf."""

    def setUp(self) -> None:
        self.client = Client()

    @patch("apps.documentation.api.v1.endpoints_views.get_adapter")
    def test_endpoints_list(self, mock_get_adapter: Mock) -> None:
        ad = Mock()
        mock_get_adapter.return_value = ad
        ad.list_endpoints.return_value = {"endpoints": [], "total": 0}
        url = reverse("api_v1:api_v1_endpoints:endpoints_list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content.decode())
        self.assertIn("endpoints", data)

    @patch("apps.documentation.api.v1.endpoints_views.get_adapter")
    def test_endpoints_methods(self, mock_get_adapter: Mock) -> None:
        ad = Mock()
        mock_get_adapter.return_value = ad
        ad.get_method_statistics.return_value = {"methods": [], "total": 0}
        url = reverse("api_v1:api_v1_endpoints:endpoints_methods")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)


class V1RelationshipsRoutesTests(TestCase):
    """``api_v1_relationships`` URLconf."""

    def setUp(self) -> None:
        self.client = Client()

    @patch("apps.documentation.api.v1.relationships_views.get_adapter")
    def test_relationships_list(self, mock_get_adapter: Mock) -> None:
        ad = Mock()
        mock_get_adapter.return_value = ad
        ad.list_relationships.return_value = {"relationships": [], "total": 0}
        url = reverse("api_v1:api_v1_relationships:relationships_list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content.decode())
        self.assertIn("relationships", data)


class V1PostmanRoutesTests(TestCase):
    """``api_v1_postman`` URLconf."""

    def setUp(self) -> None:
        self.client = Client()

    @patch("apps.documentation.api.v1.postman_views.get_postman_service")
    def test_postman_list(self, mock_svc: Mock) -> None:
        s = Mock()
        mock_svc.return_value = s
        s.list_configurations.return_value = {"configurations": [], "total": 0}
        url = reverse("api_v1:api_v1_postman:postman_list")
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content.decode())
        self.assertIn("configurations", data)


class V1UrlNamespaceTests(TestCase):
    """Guards: reverse names used in docs/clients must resolve."""

    def test_critical_reverses(self) -> None:
        reverse("api_v1:api_v1_pages:pages_list")
        reverse("api_v1:api_v1_endpoints:endpoints_list")
        reverse("api_v1:api_v1_relationships:relationships_list")
        reverse("api_v1:api_v1_postman:postman_list")
