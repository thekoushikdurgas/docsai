"""
Documentation Dashboard AJAX API - facade re-exporting per-resource modules.

Implementation is split into:
- dashboard_api_common: get_statistics_api, get_health_api
- pages_dashboard_api: get_pages_list_api, pages_bulk_* APIs
- endpoints_dashboard_api: get_endpoints_list_api, endpoints_bulk_* APIs
- relationships_dashboard_api: get_relationships_list_api, relationships_bulk_* APIs
- postman_dashboard_api: get_postman_list_api, postman_bulk_* APIs
"""

from __future__ import annotations

from .dashboard_api_common import get_statistics_api, get_health_api
from .pages_dashboard_api import (
    get_pages_list_api,
    pages_bulk_import_check_api,
    pages_bulk_import_preview_api,
    pages_bulk_import_api,
    pages_bulk_upload_to_s3_api,
    pages_import_one_api,
    pages_upload_one_to_s3_api,
)
from .endpoints_dashboard_api import (
    get_endpoints_list_api,
    endpoints_bulk_import_preview_api,
    endpoints_bulk_import_api,
    endpoints_bulk_upload_to_s3_api,
    endpoints_import_one_api,
    endpoints_upload_one_to_s3_api,
)
from .relationships_dashboard_api import (
    get_relationships_list_api,
    relationships_bulk_import_preview_api,
    relationships_bulk_import_api,
    relationships_bulk_upload_to_s3_api,
    relationships_import_one_api,
    relationships_upload_one_to_s3_api,
)
from .postman_dashboard_api import (
    get_postman_list_api,
    postman_bulk_import_preview_api,
    postman_bulk_import_api,
    postman_bulk_upload_to_s3_api,
    postman_import_one_api,
    postman_upload_one_to_s3_api,
)

__all__ = [
    "get_pages_list_api",
    "get_endpoints_list_api",
    "get_relationships_list_api",
    "get_postman_list_api",
    "get_statistics_api",
    "get_health_api",
    "pages_bulk_import_check_api",
    "pages_bulk_import_preview_api",
    "pages_bulk_import_api",
    "pages_bulk_upload_to_s3_api",
    "pages_import_one_api",
    "pages_upload_one_to_s3_api",
    "endpoints_bulk_import_preview_api",
    "endpoints_bulk_import_api",
    "endpoints_bulk_upload_to_s3_api",
    "endpoints_import_one_api",
    "endpoints_upload_one_to_s3_api",
    "relationships_bulk_import_preview_api",
    "relationships_bulk_import_api",
    "relationships_bulk_upload_to_s3_api",
    "relationships_import_one_api",
    "relationships_upload_one_to_s3_api",
    "postman_bulk_import_preview_api",
    "postman_bulk_import_api",
    "postman_bulk_upload_to_s3_api",
    "postman_import_one_api",
    "postman_upload_one_to_s3_api",
]
