"""
Tests for Dashboard list APIs (API v1).

Dashboard list data is now served by /api/v1/dashboard/pages/, etc.
Old /docs/api/dashboard/* routes were removed.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
import json

User = get_user_model()

# API v1 dashboard base path (no reverse to avoid name conflict with documentation:dashboard_pages)
API_V1_DASHBOARD_PAGES = '/api/v1/dashboard/pages/'
API_V1_DASHBOARD_ENDPOINTS = '/api/v1/dashboard/endpoints/'
API_V1_DASHBOARD_RELATIONSHIPS = '/api/v1/dashboard/relationships/'
API_V1_DASHBOARD_POSTMAN = '/api/v1/dashboard/postman/'


class DashboardAPITestCase(TestCase):
    """Base test case for dashboard API v1 tests."""

    def setUp(self):
        """Set up test client and user."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')

    def get_json_response(self, url, params=None):
        """Helper to get JSON response."""
        response = self.client.get(url, params or {})
        self.assertEqual(response['Content-Type'], 'application/json')
        return json.loads(response.content)


class DashboardPagesAPITest(DashboardAPITestCase):
    """Tests for /api/v1/dashboard/pages/."""

    def test_pages_list_api_basic(self):
        """Test basic pages list API call (API v1 format: success, data, meta.pagination)."""
        data = self.get_json_response(API_V1_DASHBOARD_PAGES)
        self.assertTrue(data.get('success'))
        self.assertIn('data', data)
        self.assertIn('meta', data)
        self.assertIn('pagination', data['meta'])
        pag = data['meta']['pagination']
        self.assertIn('total', pag)
        self.assertIn('page', pag)
        self.assertIn('page_size', pag)

    def test_pages_list_api_pagination(self):
        """Test pagination parameters."""
        data = self.get_json_response(API_V1_DASHBOARD_PAGES, {'page': 1, 'page_size': 10})
        self.assertEqual(data['meta']['pagination']['page'], 1)
        self.assertEqual(data['meta']['pagination']['page_size'], 10)


class DashboardEndpointsAPITest(DashboardAPITestCase):
    """Tests for /api/v1/dashboard/endpoints/."""

    def test_endpoints_list_api_basic(self):
        """Test basic endpoints list API call."""
        data = self.get_json_response(API_V1_DASHBOARD_ENDPOINTS)
        self.assertTrue(data.get('success'))
        self.assertIn('data', data)
        self.assertIn('meta', data)
        self.assertIn('pagination', data['meta'])


class DashboardRelationshipsAPITest(DashboardAPITestCase):
    """Tests for /api/v1/dashboard/relationships/."""

    def test_relationships_list_api_basic(self):
        """Test basic relationships list API call."""
        data = self.get_json_response(API_V1_DASHBOARD_RELATIONSHIPS)
        self.assertTrue(data.get('success'))
        self.assertIn('data', data)
        self.assertIn('meta', data)
        self.assertIn('pagination', data['meta'])


class DashboardPostmanAPITest(DashboardAPITestCase):
    """Tests for /api/v1/dashboard/postman/."""

    def test_postman_list_api_basic(self):
        """Test basic Postman list API call."""
        data = self.get_json_response(API_V1_DASHBOARD_POSTMAN)
        self.assertTrue(data.get('success'))
        self.assertIn('data', data)
        self.assertIn('meta', data)
        self.assertIn('pagination', data['meta'])

    def test_postman_list_api_pagination(self):
        """Test pagination."""
        data = self.get_json_response(API_V1_DASHBOARD_POSTMAN, {'page': 1, 'page_size': 10})
        self.assertEqual(data['meta']['pagination']['page'], 1)
        self.assertEqual(data['meta']['pagination']['page_size'], 10)
