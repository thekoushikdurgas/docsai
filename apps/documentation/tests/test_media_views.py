"""
Integration tests for media views (S3-only).

Tests the media view layer for:
- Media file list API (S3-only stub)
- Media sync status and bulk sync APIs (S3-only stubs)
"""

import json
from unittest.mock import Mock, patch
from django.test import TestCase
from django.urls import reverse

from apps.documentation.tests.helpers import (
    BaseAPITestCase,
    assert_api_response,
)


class MediaFilesListAPITestCase(BaseAPITestCase):
    """Test cases for media files list API (S3-only: returns empty list)."""

    def setUp(self):
        super().setUp()
        self.list_api_url = reverse('documentation:api_media_files')

    def test_list_files_api_success(self):
        """List files API returns 200 and empty data in S3-only mode."""
        response = self.client.get(self.list_api_url)
        assert_api_response(self, response, expected_status=200, expected_success=True)
        data = response.json()
        self.assertIn("data", data)
        self.assertEqual(data["data"], [])

    def test_list_files_api_resource_type_param(self):
        """List files API accepts resource_type query param."""
        for resource_type in ('pages', 'endpoints', 'relationships', 'postman'):
            response = self.client.get(self.list_api_url, {'resource_type': resource_type})
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data.get("meta", {}).get("resource_type"), resource_type)

    def test_list_files_api_returns_s3_only_meta(self):
        """List files API indicates S3-only in meta."""
        response = self.client.get(self.list_api_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("meta", {}).get("s3_only", False))


class MediaSyncAPITestCase(BaseAPITestCase):
    """Test cases for media sync APIs (S3-only stubs)."""

    def setUp(self):
        super().setUp()
        self.sync_status_url = reverse('documentation:api_media_sync_status')
        self.bulk_sync_url = reverse('documentation:api_media_bulk_sync')

    def test_sync_status_api_success(self):
        """Sync status API returns 200 and s3_only in S3-only mode."""
        response = self.client.get(self.sync_status_url)
        assert_api_response(self, response, expected_status=200, expected_success=True)
        data = response.json()
        self.assertIn("data", data)
        self.assertEqual(data["data"].get("status"), "s3_only")

    def test_bulk_sync_api_success(self):
        """Bulk sync API returns 200 and s3_only in S3-only mode."""
        response = self.client.post(
            self.bulk_sync_url,
            data=json.dumps({"resource_type": "pages", "direction": "to_lambda"}),
            content_type="application/json",
        )
        assert_api_response(self, response, expected_status=200, expected_success=True)
        data = response.json()
        self.assertIn("data", data)
        self.assertTrue(data["data"].get("s3_only", False))
