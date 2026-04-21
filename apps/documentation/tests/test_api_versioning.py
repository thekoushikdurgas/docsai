"""
Tests for API versioning (versions endpoint, version router).
"""

from django.test import TestCase

from apps.documentation.api_router import (
    get_version_from_path,
    negotiate_version,
    SUPPORTED_VERSIONS,
    DEFAULT_VERSION,
    VERSION_INFO,
)


class ApiVersionRouterTestCase(TestCase):
    """Test cases for version router utilities."""

    def test_get_version_from_path_v1(self):
        self.assertEqual(get_version_from_path("/docs/api/v1/pages/"), "v1")
        self.assertEqual(get_version_from_path("/docs/api/v1/health/"), "v1")

    def test_get_version_from_path_v2(self):
        self.assertEqual(get_version_from_path("/docs/api/v2/stats/"), "v2")

    def test_get_version_from_path_no_version(self):
        self.assertIsNone(get_version_from_path("/docs/api/health/"))
        self.assertIsNone(get_version_from_path("/docs/api/pages/"))

    def test_get_version_from_path_invalid(self):
        self.assertIsNone(get_version_from_path("/docs/api/v9/"))
        self.assertIsNone(get_version_from_path("/other/path/"))

    def test_supported_versions(self):
        self.assertIn("v1", SUPPORTED_VERSIONS)
        self.assertIn("v2", SUPPORTED_VERSIONS)
        self.assertEqual(DEFAULT_VERSION, "v1")

    def test_version_info_structure(self):
        for v in SUPPORTED_VERSIONS:
            self.assertIn(v, VERSION_INFO)
            info = VERSION_INFO[v]
            self.assertIn("deprecated", info)
            self.assertIn("description", info)


# Note: JSON routes ``/docs/api/versions/`` and ``documentation:api_versions`` were removed
# (see ``documentation/urls.py``). Use ``/api/v1/`` (OpenAPI) or media-manager HTML views instead.
