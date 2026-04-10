"""
Unified storage interface - facade composing per-resource modules.

Implementation is split into:
- unified_storage_base: BaseUnifiedStorage (cache, circuit breakers, metrics, clear_cache, check_health)
- pages_storage: PagesStorageMixin (get_page, list_pages, get_pages_by_type, etc.)
- endpoints_storage: EndpointsStorageMixin (get_endpoint, list_endpoints, etc.)
- relationships_storage: RelationshipsStorageMixin (get_relationship, list_relationships, etc.)
- postman_storage: PostmanStorageMixin (clear_cache for 'postman' handled by base)
"""

from __future__ import annotations

import logging

from apps.documentation.repositories.unified_storage_base import (
    BaseUnifiedStorage,
    StorageBackend,
    StorageBackendInterface,
)
from apps.documentation.repositories.pages_storage import PagesStorageMixin
from apps.documentation.repositories.endpoints_storage import EndpointsStorageMixin
from apps.documentation.repositories.relationships_storage import (
    RelationshipsStorageMixin,
)
from apps.documentation.repositories.postman_storage import PostmanStorageMixin

logger = logging.getLogger(__name__)


class UnifiedStorage(
    PagesStorageMixin,
    EndpointsStorageMixin,
    RelationshipsStorageMixin,
    PostmanStorageMixin,
    BaseUnifiedStorage,
):
    """Unified storage with fallback strategy: S3 → GraphQL.

    Provides a unified interface for accessing documentation data from S3
    with optional GraphQL fallback, caching, circuit breakers, and
    request deduplication.

    Features:
    - S3 as primary backend
    - Optional GraphQL fallback
    - Redis caching with TTL
    - Circuit breakers for external services
    - Request deduplication
    """

    def __init__(self, s3_storage=None, graphql_service=None):
        # BaseUnifiedStorage must be last in MRO so its __init__ runs (after mixins)
        super().__init__(s3_storage=s3_storage, graphql_service=graphql_service)
        self.logger = logging.getLogger(f"{__name__}.UnifiedStorage")
        self.logger.debug(
            f"UnifiedStorage initialized (S3 only, caching={self.enable_caching}, fallback={self.fallback_enabled})"
        )


# Re-export for backward compatibility
__all__ = ["UnifiedStorage", "StorageBackend", "StorageBackendInterface"]
