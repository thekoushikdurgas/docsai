"""Unified storage interface with multi-strategy pattern: S3 → GraphQL → local JSON fallback."""

import json
import logging
from typing import Any, Dict, List, Optional, Sequence, Tuple
from abc import ABC, abstractmethod
from enum import Enum

from django.conf import settings
from django.core.cache import cache

from apps.documentation.repositories.s3_json_storage import S3JSONStorage, _local_path_for_s3_key
from apps.core.exceptions import RepositoryError, S3Error

# Optional imports for fallback services
try:
    from apps.documentation.services.graphql_documentation_service import GraphQLDocumentationService
except ImportError:
    GraphQLDocumentationService = None

# Lambda client removed - using local/S3/GraphQL only

logger = logging.getLogger(__name__)


class StorageBackend(Enum):
    """Enumeration of available storage backends."""
    LOCAL = "local"
    S3 = "s3"
    GRAPHQL = "graphql"


class StorageBackendInterface(ABC):
    """Abstract interface for storage backends."""
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if backend is available."""
        pass
    
    @abstractmethod
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of the backend."""
        pass


class UnifiedStorage:
    """Unified storage with fallback strategy: S3 → GraphQL.
    
    Provides a unified interface for accessing documentation data from S3
    with optional GraphQL fallback, caching, circuit breakers, and
    request deduplication. Local media/ storage has been removed.
    
    Features:
    - S3 as primary backend
    - Optional GraphQL fallback
    - Redis caching with TTL
    - Circuit breakers for external services
    - Request deduplication
    - Comprehensive error handling
    - Health checks and metrics
    """

    def __init__(
        self,
        s3_storage: Optional[S3JSONStorage] = None,
        graphql_service: Optional[GraphQLDocumentationService] = None,
    ):
        """Initialize unified storage.
        
        Args:
            s3_storage: Optional S3JSONStorage instance
            graphql_service: Optional GraphQLDocumentationService instance
        """
        if s3_storage is None:
            from apps.documentation.services import get_shared_s3_storage
            self.s3_storage = get_shared_s3_storage()
        else:
            self.s3_storage = s3_storage
        
        # Initialize GraphQL service if enabled
        self.graphql_service = None
        if getattr(settings, 'GRAPHQL_ENABLED', False) and GraphQLDocumentationService:
            try:
                self.graphql_service = graphql_service or GraphQLDocumentationService()
            except Exception as e:
                logger.warning(f"Failed to initialize GraphQL service: {e}")
        
        # Configuration (local JSON files removed - S3 only)
        self.use_local_json_files = False
        self.cache_timeout = getattr(settings, 'UNIFIED_STORAGE_CACHE_TTL', 300)  # 5 minutes default
        self.enable_request_deduplication = getattr(settings, 'ENABLE_REQUEST_DEDUPLICATION', True)
        self.enable_caching = getattr(settings, 'UNIFIED_STORAGE_ENABLE_CACHE', True)
        self.fallback_enabled = getattr(settings, 'UNIFIED_STORAGE_FALLBACK_ENABLED', True)
        
        # Request deduplication tracking
        self._pending_requests: Dict[str, Any] = {}
        try:
            from apps.core.utils.request_deduplication import RequestDeduplicator
            self.request_deduplicator = RequestDeduplicator(cache_timeout=self.cache_timeout)
        except Exception as e:
            logger.warning(f"Failed to initialize request deduplicator: {e}")
            self.request_deduplicator = None
        
        # Initialize circuit breakers for external services
        try:
            from apps.core.services.circuit_breaker import CircuitBreaker
            self.s3_circuit_breaker = CircuitBreaker('s3_storage', failure_threshold=5, timeout_seconds=60)
            if self.graphql_service:
                self.graphql_circuit_breaker = CircuitBreaker('graphql_api', failure_threshold=5, timeout_seconds=60)
            else:
                self.graphql_circuit_breaker = None
        except Exception as e:
            logger.warning(f"Failed to initialize circuit breakers: {e}")
            self.s3_circuit_breaker = None
            self.graphql_circuit_breaker = None
        
        # Metrics tracking
        self._metrics: Dict[str, Any] = {
            'cache_hits': 0,
            'cache_misses': 0,
            'backend_usage': {
                'local': 0,
                's3': 0,
                'graphql': 0
            },
            'errors': {
                'local': 0,
                's3': 0,
                'graphql': 0
            }
        }
        
        self.logger = logging.getLogger(f"{__name__}.UnifiedStorage")
        self.logger.debug(f"UnifiedStorage initialized (S3 only, caching={self.enable_caching}, fallback={self.fallback_enabled})")

    def _get_cache_key(self, resource_type: str, identifier: str = None, filters: Optional[Dict] = None) -> str:
        """Generate cache key.
        
        Args:
            resource_type: Type of resource ('pages', 'endpoints', 'relationships')
            identifier: Optional identifier (page_id, endpoint_id, etc.)
            filters: Optional filter parameters for list operations
            
        Returns:
            Cache key string
        """
        if identifier:
            return f"unified_storage:{resource_type}:{identifier}"

        # Include filters in cache key for list operations (memcached-safe: no list repr)
        if filters:
            parts = []
            for k, v in sorted(filters.items()):
                if v is not None:
                    seg = self._cache_key_filter_value(v)
                    if seg:
                        parts.append(f"{k}={seg}")
            if parts:
                filter_str = ":".join(parts)
                return f"unified_storage:{resource_type}:list:{filter_str}"

        return f"unified_storage:{resource_type}:all"

    @staticmethod
    def _cache_key_filter_value(value: Any) -> str:
        """Convert a filter value to a memcached-safe cache key segment (no brackets, quotes, spaces)."""
        if value is None:
            return ""
        if isinstance(value, (list, tuple)):
            return ",".join(sorted(str(x) for x in value))
        return str(value)

    def _get_request_key(self, resource_type: str, operation: str, **kwargs) -> str:
        """Generate request key for deduplication."""
        key_parts = [resource_type, operation]
        for k, v in sorted(kwargs.items()):
            if v is not None:
                key_parts.append(f"{k}={v}")
        return ':'.join(key_parts)

    def _safe_cache_get(self, key: str, default: Any = None) -> Any:
        """Safely get value from cache, handling Redis connection failures.
        
        Args:
            key: Cache key
            default: Default value if cache fails or key not found
            
        Returns:
            Cached value or default
        """
        if not self.enable_caching:
            return default
        
        try:
            value = cache.get(key, default)
            if value != default:
                self._metrics['cache_hits'] += 1
            else:
                self._metrics['cache_misses'] += 1
            return value
        except Exception as e:
            self.logger.warning(f"Cache get failed for key {key}: {e}")
            self._metrics['cache_misses'] += 1
            return default

    def _safe_cache_set(self, key: str, value: Any, timeout: int = None) -> bool:
        """Safely set value in cache, handling Redis connection failures.
        
        Args:
            key: Cache key
            value: Value to cache
            timeout: Cache timeout in seconds
            
        Returns:
            True if successful, False otherwise
        """
        if not self.enable_caching:
            return False
        
        try:
            if timeout is None:
                timeout = self.cache_timeout
            cache.set(key, value, timeout)
            return True
        except Exception as e:
            self.logger.warning(f"Cache set failed for key {key}: {e}")
            return False
    
    def _track_backend_usage(self, backend: StorageBackend, success: bool = True):
        """Track backend usage for metrics.
        
        Args:
            backend: Storage backend used
            success: Whether the operation was successful
        """
        backend_name = backend.value
        if success:
            self._metrics['backend_usage'][backend_name] = self._metrics['backend_usage'].get(backend_name, 0) + 1
        else:
            self._metrics['errors'][backend_name] = self._metrics['errors'].get(backend_name, 0) + 1
    
    def _handle_backend_error(self, backend: StorageBackend, error: Exception, operation: str) -> None:
        """Handle errors from storage backends with consistent logging.
        
        Args:
            backend: Storage backend that failed
            error: Exception that occurred
            operation: Operation that failed
        """
        backend_name = backend.value
        self._track_backend_usage(backend, success=False)
        self.logger.warning(
            f"Backend {backend_name} failed for operation {operation}: {error}",
            exc_info=True
        )

    def get_page(self, page_id: str, page_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get a single page with fallback strategy.
        
        Strategy: Local → S3 → GraphQL
        
        Args:
            page_id: Page ID
            page_type: Optional page type filter
            
        Returns:
            Page data dictionary, or None if not found
        """
        # Check cache first
        cache_key = self._get_cache_key('pages', page_id)
        cached = self._safe_cache_get(cache_key)
        if cached:
            self.logger.debug(f"Cache hit for page: {page_id}")
            # Apply page_type filter to cached result
            if page_type and cached.get('page_type') != page_type:
                return None
            return cached
        
        # Try S3 with circuit breaker and request deduplication
        def _fetch_from_s3():
            from apps.documentation.repositories.pages_repository import PagesRepository
            repo = PagesRepository(storage=self.s3_storage)
            if self.s3_circuit_breaker:
                return self.s3_circuit_breaker.call(
                    repo.get_by_page_id,
                    page_id,
                    page_type
                )
            else:
                return repo.get_by_page_id(page_id, page_type)
        
        page_data = None
        try:
            if self.enable_request_deduplication and self.request_deduplicator:
                request_key = self._get_request_key('pages', 's3_get', page_id=page_id, page_type=page_type)
                page_data = self.request_deduplicator.execute(request_key, _fetch_from_s3)
            else:
                page_data = _fetch_from_s3()
            
            if page_data:
                self._track_backend_usage(StorageBackend.S3, success=True)
                self.logger.debug(f"Loaded page from S3: {page_id}")
                self._safe_cache_set(cache_key, page_data, self.cache_timeout)
                return page_data
            self.logger.debug(f"Page not found in S3: {page_id}")
        except Exception as e:
            self._handle_backend_error(StorageBackend.S3, e, f"get_page({page_id})")
            if not self.fallback_enabled:
                raise RepositoryError(
                    message=f"Failed to load page from S3: {str(e)}",
                    entity_id=page_id,
                    operation="get_page",
                    error_code="S3_STORAGE_FAILED"
                ) from e

        # GraphQL fallback when S3 returned None or raised and fallback is enabled
        if self.graphql_service:
            try:
                if self.graphql_circuit_breaker:
                    page_data = self.graphql_circuit_breaker.call(
                        self.graphql_service.get_page,
                        page_id,
                        page_type
                    )
                else:
                    page_data = self.graphql_service.get_page(page_id, page_type)
                if page_data:
                    self._track_backend_usage(StorageBackend.GRAPHQL, success=True)
                    self.logger.debug(f"Loaded page from GraphQL: {page_id}")
                    self._safe_cache_set(cache_key, page_data, self.cache_timeout)
                    return page_data
            except Exception as e:
                self._handle_backend_error(StorageBackend.GRAPHQL, e, f"get_page({page_id})")
        
        # Local JSON fallback when S3 and GraphQL have no data (e.g. contact360/media/pages/*.json)
        s3_key = f"{getattr(settings, 'S3_DATA_PREFIX', 'data/')}pages/{page_id}.json"
        local_path = _local_path_for_s3_key(s3_key)
        if local_path and local_path.is_file():
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    page_data = json.load(f)
                if page_data and (not page_type or page_data.get("page_type") == page_type):
                    self._track_backend_usage(StorageBackend.LOCAL, success=True)
                    self.logger.debug(f"Loaded page from local JSON: {page_id}")
                    self._safe_cache_set(cache_key, page_data, self.cache_timeout)
                    return page_data
            except (json.JSONDecodeError, OSError) as e:
                self.logger.warning(f"Failed to read local page JSON {local_path}: {e}")
        
        self.logger.debug(f"Page not found in any source: {page_id}")
        return None

    def list_pages(
        self,
        page_type: Optional[str] = None,
        page_types: Optional[Sequence[str]] = None,
        include_drafts: bool = True,
        include_deleted: bool = False,
        status: Optional[str] = None,
        page_state: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List pages with fallback strategy.

        Strategy: Local → S3 → GraphQL

        Args:
            page_type: Optional single page type filter (ignored if page_types is set)
            page_types: Optional list of page types to include (takes precedence over page_type)
            include_drafts: Include draft pages
            include_deleted: Include deleted pages
            status: Optional status filter
            page_state: Optional page state filter (coming_soon, published, draft, development, test)
            limit: Optional limit
            offset: Offset for pagination

        Returns:
            Dictionary with 'pages' list and 'total' count
        """
        if page_types is not None and len(page_types) == 0:
            page_types = None
        effective_types = list(page_types) if page_types else None
        filters = {
            'page_type': effective_types if effective_types else page_type,
            'page_types': effective_types,
            'status': status,
            'page_state': page_state,
            'include_drafts': include_drafts,
            'include_deleted': include_deleted,
            'limit': limit,
            'offset': offset,
        }
        cache_key = self._get_cache_key('pages', None, filters)
        cached = self._safe_cache_get(cache_key)
        if cached is not None:
            logger.debug("Cache hit for list_pages")
            return cached

        # Try S3
        try:
            from apps.documentation.repositories.pages_repository import PagesRepository
            repo = PagesRepository(storage=self.s3_storage)
            out = repo.list_all(
                page_type=page_type if not effective_types else None,
                page_types=effective_types,
                include_drafts=include_drafts,
                include_deleted=include_deleted,
                status=status,
                page_state=page_state,
                limit=limit,
                offset=offset
            )
            pages = out.get("pages", []) if isinstance(out, dict) else out
            total = out.get("total", len(pages)) if isinstance(out, dict) else len(pages)
            logger.debug(f"Loaded {len(pages)} pages from S3, total={total}")
            result = {'pages': pages, 'total': total, 'source': 's3'}
            self._safe_cache_set(cache_key, result, self.cache_timeout)
            return result
        except Exception as e:
            logger.warning(f"Failed to load pages from S3: {e}")
        
        # All sources exhausted - return empty result
        return {
            'pages': [],
            'total': 0,
            'source': 'none'
        }

    def get_pages_by_type(
        self,
        page_type: str,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Get all pages for a specific page type, optionally filtered by status."""
        result = self.list_pages(page_type=page_type, limit=None, offset=0)
        pages = result.get("pages", [])
        if status:
            pages = [p for p in pages if (p.get("metadata") or {}).get("status") == status]
        return pages

    def count_pages_by_type(self, page_type: str) -> int:
        """Count pages by type (S3)."""
        # S3
        try:
            from apps.documentation.repositories.pages_repository import PagesRepository
            repo = PagesRepository(storage=self.s3_storage)
            s3_count = repo.count_pages_by_type(page_type)
            return s3_count
        except Exception as e:
            self.logger.warning(f"S3 count_pages_by_type failed: {e}")
        
        return 0

    def get_type_statistics(self) -> Dict[str, Any]:
        """Get statistics for all page types."""
        try:
            from apps.documentation.repositories.pages_repository import PagesRepository
            repo = PagesRepository(storage=self.s3_storage)
            return repo.get_type_statistics()
        except Exception as e:
            self.logger.warning(f"get_type_statistics failed: {e}")
        result = self.list_pages(limit=None, offset=0)
        pages = result.get("pages", [])
        from apps.documentation.constants import PAGE_TYPES
        count_by_type = {pt: {"published": 0, "draft": 0, "deleted": 0, "total": 0} for pt in PAGE_TYPES}
        for p in pages:
            pt = p.get("page_type", "docs")
            if pt not in count_by_type:
                count_by_type[pt] = {"published": 0, "draft": 0, "deleted": 0, "total": 0}
            st = (p.get("metadata") or {}).get("status", "published")
            count_by_type[pt]["total"] += 1
            if st == "published":
                count_by_type[pt]["published"] += 1
            elif st == "draft":
                count_by_type[pt]["draft"] += 1
            elif st == "deleted":
                count_by_type[pt]["deleted"] += 1
        statistics = [{"type": t, "count": v["total"], "published": v["published"], "draft": v["draft"], "deleted": v["deleted"]}
                     for t, v in count_by_type.items()]
        return {"statistics": statistics, "total": len(pages)}

    def list_pages_by_user_type(
        self,
        user_type: str,
        page_type: Optional[str] = None,
        include_drafts: bool = True,
        include_deleted: bool = False,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """List pages accessible by user_type (access_control.can_view).

        user_type 'public' means pages with no access_control restrictions
        (access_control null or empty).
        """
        valid_user_types = ["super_admin", "admin", "pro_user", "free_user", "guest", "public"]
        if user_type not in valid_user_types:
            raise ValueError(f"Invalid user_type: {user_type}. Must be one of {valid_user_types}")
        result = self.list_pages(
            page_type=page_type,
            include_drafts=include_drafts,
            include_deleted=include_deleted,
            status=status,
            limit=None,
            offset=0,
        )
        # Map camelCase keys from form to snake_case for API
        _key_map = {"freeUser": "free_user", "proUser": "pro_user", "superAdmin": "super_admin"}

        pages = result.get("pages", [])
        filtered = []
        for page in pages:
            ac = page.get("access_control") or page.get("metadata", {}).get("access_control") or {}
            if not isinstance(ac, dict):
                ac = {}
            ac = {_key_map.get(k, k): v for k, v in ac.items()}
            if user_type == "public":
                if not ac:
                    filtered.append(page)
                continue
            role = ac.get(user_type)
            if not role:
                filtered.append(page)
                continue
            if role.get("can_view", True):
                filtered.append(page)
        total = len(filtered)
        if limit is not None:
            filtered = filtered[offset:offset + limit]
        else:
            filtered = filtered[offset:]
        return {"pages": filtered, "total": total}

    def get_endpoint(self, endpoint_id: str) -> Optional[Dict[str, Any]]:
        """Get a single endpoint with fallback strategy.
        
        Strategy: Local → S3 → GraphQL
        
        Args:
            endpoint_id: Endpoint ID
            
        Returns:
            Endpoint data dictionary, or None if not found
        """
        # Check cache first
        cache_key = self._get_cache_key('endpoints', endpoint_id)
        cached = self._safe_cache_get(cache_key)
        if cached:
            logger.debug(f"Cache hit for endpoint: {endpoint_id}")
            return cached
        
        # Try S3
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            endpoint_data = repo.get_by_endpoint_id(endpoint_id)
            if endpoint_data:
                logger.debug(f"Loaded endpoint from S3: {endpoint_id}")
                self._safe_cache_set(cache_key, endpoint_data, self.cache_timeout)
                return endpoint_data
        except Exception as e:
            logger.warning(f"Failed to load endpoint from S3: {e}")
        
        # All sources exhausted
        logger.debug(f"Endpoint not found in any source: {endpoint_id}")
        return None

    def get_endpoints_bulk(self, endpoint_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """Fetch multiple endpoints by ID. Returns dict mapping endpoint_id -> endpoint data."""
        if not endpoint_ids:
            return {}
        ids = list(dict.fromkeys(endpoint_ids))  # deduplicate, preserve order

        # Check cache first
        out: Dict[str, Dict[str, Any]] = {}
        remaining = []
        for eid in ids:
            key = self._get_cache_key('endpoints', eid)
            cached = self._safe_cache_get(key)
            if cached:
                out[eid] = cached
            else:
                remaining.append(eid)

        if not remaining:
            return out

        # Single get_endpoint for any still missing
        for eid in remaining:
            ep = self.get_endpoint(eid)
            if ep:
                out[eid] = ep

        return out

    def list_endpoints(
        self,
        method: Optional[str] = None,
        api_version: Optional[str] = None,
        endpoint_state: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> Dict[str, Any]:
        """List endpoints with fallback strategy.
        
        Strategy: Local → S3 → GraphQL
        
        Args:
            method: Optional method filter ('QUERY', 'MUTATION', 'GET', 'POST', etc.)
            api_version: Optional API version filter
            endpoint_state: Optional endpoint state filter (coming_soon, published, draft, development, test)
            limit: Optional limit
            offset: Offset for pagination
            
        Returns:
            Dictionary with 'endpoints' list and 'total' count
        """
        filters = {
            'method': method,
            'api_version': api_version,
            'endpoint_state': endpoint_state,
            'limit': limit,
            'offset': offset,
        }
        cache_key = self._get_cache_key('endpoints', None, filters)
        cached = self._safe_cache_get(cache_key)
        if cached is not None:
            # Do not use cached empty result so retries can get real data (avoids stale "No endpoints found")
            endpoints_cached = cached.get("endpoints") or []
            if endpoints_cached or (cached.get("total") or 0) > 0:
                logger.debug("Cache hit for list_endpoints")
                return cached
            logger.debug("Skipping cached empty list_endpoints, retrying")

        # Try S3
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            endpoints = repo.list_all(
                method=method,
                api_version=api_version,
                endpoint_state=endpoint_state,
                limit=limit,
                offset=offset
            )
            # Use index total for pagination when no filters; with filters use slice length
            if api_version or method or endpoint_state:
                total = len(endpoints)
            else:
                try:
                    from apps.documentation.services import get_shared_s3_index_manager
                    idx = get_shared_s3_index_manager().read_index("endpoints", use_cache=True)
                    total = idx.get("total", len(endpoints))
                    if limit is not None and total < len(endpoints):
                        total = len(endpoints)
                except Exception:
                    total = len(endpoints)
            logger.debug(f"Loaded {len(endpoints)} endpoints from S3")
            result = {'endpoints': endpoints, 'total': total, 'source': 's3'}
            # Do not cache empty results so retries can get real data (avoids stale "No endpoints found" when index has data)
            if endpoints or total > 0:
                self._safe_cache_set(cache_key, result, self.cache_timeout)
            return result
        except Exception as e:
            logger.warning(f"Failed to load endpoints from S3: {e}")

        # All sources exhausted - return empty result
        return {
            'endpoints': [],
            'total': 0,
            'source': 'none'
        }

    def get_endpoint_by_path_and_method(
        self, endpoint_path: str, method: str
    ) -> Optional[Dict[str, Any]]:
        """Get endpoint by path and method (S3)."""
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.get_by_path_and_method(endpoint_path, method)
        except Exception as e:
            self.logger.warning(f"get_endpoint_by_path_and_method failed: {e}")
        return None

    def get_endpoints_by_api_version(self, api_version: str) -> List[Dict[str, Any]]:
        """Get all endpoints for a specific API version."""
        return self.list_endpoints(api_version=api_version, limit=None, offset=0).get("endpoints", [])

    def get_endpoints_by_method(self, method: str) -> List[Dict[str, Any]]:
        """Get all endpoints for a specific method."""
        return self.list_endpoints(method=method, limit=None, offset=0).get("endpoints", [])

    def count_endpoints_by_api_version(self, api_version: str) -> int:
        """Count endpoints by API version."""
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.count_endpoints_by_api_version(api_version)
        except Exception as e:
            self.logger.warning(f"count_endpoints_by_api_version failed: {e}")
        return len(self.get_endpoints_by_api_version(api_version))

    def count_endpoints_by_method(self, method: str) -> int:
        """Count endpoints by method."""
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.count_endpoints_by_method(method)
        except Exception as e:
            self.logger.warning(f"count_endpoints_by_method failed: {e}")
        return len(self.get_endpoints_by_method(method))

    def get_api_version_statistics(self) -> Dict[str, Any]:
        """Get statistics for all API versions."""
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.get_api_version_statistics()
        except Exception as e:
            self.logger.warning(f"get_api_version_statistics failed: {e}")
        return {"versions": [], "total": 0}

    def get_method_statistics(self) -> Dict[str, Any]:
        """Get statistics for all methods."""
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.get_method_statistics()
        except Exception as e:
            self.logger.warning(f"get_method_statistics failed: {e}")
        return {"methods": [], "total": 0}

    def get_relationship(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        """Get a single relationship with fallback strategy.

        Strategy: Local → S3 → GraphQL

        Args:
            relationship_id: Relationship ID

        Returns:
            Relationship data dictionary, or None if not found
        """
        # Check cache first
        cache_key = self._get_cache_key('relationships', relationship_id)
        cached = self._safe_cache_get(cache_key)
        if cached:
            logger.debug(f"Cache hit for relationship: {relationship_id}")
            return cached

        # Try S3
        try:
            from apps.documentation.repositories.relationships_repository import RelationshipsRepository
            repo = RelationshipsRepository(storage=self.s3_storage)
            relationship_data = repo.get_by_relationship_id(relationship_id)
            if relationship_data:
                logger.debug(f"Loaded relationship from S3: {relationship_id}")
                self._safe_cache_set(cache_key, relationship_data, self.cache_timeout)
                return relationship_data
        except Exception as e:
            logger.warning(f"Failed to load relationship from S3: {e}")

        # All sources exhausted
        logger.debug(f"Relationship not found in any source: {relationship_id}")
        return None

    def list_relationships(
        self,
        page_id: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        usage_type: Optional[str] = None,
        usage_context: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """List relationships with optional filters. Returns {relationships: [], total: n}."""
        try:
            from apps.documentation.repositories.relationships_repository import RelationshipsRepository
            repo = RelationshipsRepository(storage=self.s3_storage)
            rels = repo.list_all(page_id=page_id, endpoint_id=endpoint_id, limit=limit, offset=offset)
            if usage_type or usage_context:
                filtered = []
                for r in rels:
                    if usage_type and r.get("usage_type") != usage_type:
                        continue
                    if usage_context and r.get("usage_context") != usage_context:
                        continue
                    filtered.append(r)
                rels = filtered
            return {"relationships": rels, "total": len(rels)}
        except Exception as e:
            self.logger.warning(f"list_relationships failed: {e}")
        return {"relationships": [], "total": 0}

    def get_relationship_statistics(self) -> Dict[str, Any]:
        """Get relationship statistics (counts by usage_type, etc.)."""
        result = self.list_relationships(limit=None, offset=0)
        rels = result.get("relationships", [])
        by_usage_type = {}
        by_usage_context = {}
        for r in rels:
            ut = r.get("usage_type") or "primary"
            by_usage_type[ut] = by_usage_type.get(ut, 0) + 1
            uc = r.get("usage_context") or "data_fetching"
            by_usage_context[uc] = by_usage_context.get(uc, 0) + 1
        return {
            "total": len(rels),
            "by_usage_type": by_usage_type,
            "by_usage_context": by_usage_context,
            "statistics": [
                {"usage_type": k, "count": v} for k, v in by_usage_type.items()
            ],
        }

    def get_relationship_graph(self) -> Dict[str, Any]:
        """Get graph representation (nodes and edges) for relationships."""
        result = self.list_relationships(limit=None, offset=0)
        rels = result.get("relationships", [])
        nodes = []
        edges = []
        seen_pages = set()
        seen_endpoints = set()
        for r in rels:
            page_path = r.get("page_path") or r.get("page_id") or ""
            endpoint_path = r.get("endpoint_path") or ""
            method = r.get("method") or "GET"
            if page_path and page_path not in seen_pages:
                nodes.append({"id": page_path, "type": "page", "label": page_path})
                seen_pages.add(page_path)
            ep_key = f"{method}:{endpoint_path}"
            if ep_key and ep_key not in seen_endpoints:
                nodes.append({"id": ep_key, "type": "endpoint", "label": endpoint_path})
                seen_endpoints.add(ep_key)
            if page_path and ep_key:
                edges.append({
                    "source": page_path,
                    "target": ep_key,
                    "usage_type": r.get("usage_type"),
                    "usage_context": r.get("usage_context"),
                })
        return {"nodes": nodes, "edges": edges}

    def get_relationships_by_page(self, page_path: str) -> Optional[Dict[str, Any]]:
        """Get relationships for a page with fallback strategy.
        
        Strategy: Local → S3 → GraphQL
        
        Args:
            page_path: Page route path
            
        Returns:
            Relationships data dictionary, or None if not found
        """
        # Try S3
        try:
            from apps.documentation.repositories.relationships_repository import RelationshipsRepository
            repo = RelationshipsRepository(storage=self.s3_storage)
            # Try to find page_id from page_path
            # First try to get page by route to find page_id
            from apps.documentation.repositories.pages_repository import PagesRepository
            pages_repo = PagesRepository(storage=self.s3_storage)
            page_data = pages_repo.get_by_route(page_path)
            if page_data:
                page_id = page_data.get('page_id')
                if page_id:
                    relationships = repo.get_by_page(page_id)
                    if relationships:
                        logger.debug(f"Loaded relationships from S3 for page: {page_path}")
                        return {'relationships': relationships, 'page_id': page_id}
        except Exception as e:
            logger.warning(f"Failed to load relationships from S3: {e}")
        
        return None

    def get_relationships_by_endpoint(
        self,
        endpoint_path: str,
        method: str = "QUERY"
    ) -> Optional[Dict[str, Any]]:
        """Get relationships for an endpoint with fallback strategy.
        
        Strategy: Local → S3 → GraphQL
        
        Args:
            endpoint_path: Endpoint path
            method: HTTP method
            
        Returns:
            Relationships data dictionary, or None if not found
        """
        # Try S3
        try:
            from apps.documentation.repositories.relationships_repository import RelationshipsRepository
            repo = RelationshipsRepository(storage=self.s3_storage)
            relationships = repo.get_by_endpoint(endpoint_path, method)
            if relationships:
                logger.debug(f"Loaded relationships from S3 for endpoint: {endpoint_path}")
                return {'relationships': relationships, 'endpoint_path': endpoint_path, 'method': method}
        except Exception as e:
            logger.warning(f"Failed to load relationships from S3: {e}")
        
        return None

    def _safe_cache_delete(self, key: str) -> bool:
        """Safely delete value from cache, handling Redis connection failures.
        
        Args:
            key: Cache key to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cache.delete(key)
            return True
        except Exception as e:
            logger.warning(f"Cache delete failed for key {key}: {e}")
            return False

    def clear_cache(self, resource_type: str = None, identifier: str = None, filters: Optional[Dict] = None):
        """Clear cache for a specific resource or all resources.
        
        Args:
            resource_type: Optional resource type to clear
            identifier: Optional identifier to clear
            filters: Optional filters for list cache keys
            
        Examples:
            # Clear specific page
            clear_cache('pages', 'page-001')
            
            # Clear all pages
            clear_cache('pages')
            
            # Clear all cache
            clear_cache()
        """
        try:
            # Try to use RedisCacheManager for pattern deletion
            from apps.core.utils.redis_cache import RedisCacheManager
            cache_manager = RedisCacheManager()
            
            if resource_type and identifier:
                # Clear specific resource
                cache_key = self._get_cache_key(resource_type, identifier)
                deleted = cache_manager.delete(cache_key)
                logger.debug(f"Cleared cache for {resource_type}:{identifier} (deleted: {deleted})")
            elif resource_type:
                # Clear all cache for resource type using pattern
                pattern = f"unified_storage:{resource_type}:*"
                deleted = cache_manager.delete_pattern(pattern)
                logger.debug(f"Cleared cache for resource type '{resource_type}' (deleted {deleted} keys)")
            else:
                # Clear all unified_storage cache
                pattern = "unified_storage:*"
                deleted = cache_manager.delete_pattern(pattern)
                logger.debug(f"Cleared all unified_storage cache (deleted {deleted} keys)")
        except ImportError:
            # Fallback to Django cache if RedisCacheManager not available
            if resource_type and identifier:
                cache_key = self._get_cache_key(resource_type, identifier)
                self._safe_cache_delete(cache_key)
                logger.debug(f"Cleared cache for {resource_type}:{identifier}")
            elif resource_type:
                # For non-Redis backends, we can't do pattern deletion easily
                # Log warning and suggest using cache versioning
                logger.warning(
                    f"Cache clear for resource type '{resource_type}' requires Redis backend for pattern deletion. "
                    "Consider using cache versioning for non-Redis backends."
                )
            else:
                logger.warning(
                    "Cache clear for all resources requires Redis backend for pattern deletion. "
                    "Consider using cache versioning for non-Redis backends."
                )
    
    def check_health(self) -> Dict[str, Any]:
        """
        Check health of storage backends (S3 and optional GraphQL; local removed).
        
        Returns:
            Dictionary with health status for each backend
        """
        health_status = {
            'local': {'healthy': False, 'available': False, 'message': 'removed (S3-only)'},
            's3': {'healthy': True, 'available': False},
            'graphql': {'healthy': True, 'available': False}
        }
        
        # Check S3 storage
        try:
            if self.s3_circuit_breaker:
                cb_status = self.s3_circuit_breaker.get_status()
                health_status['s3']['circuit_breaker'] = cb_status
                health_status['s3']['available'] = cb_status['state'] != 'open'
            else:
                # Simple connectivity check
                test_key = f"{self.s3_storage.data_prefix}health_check.json"
                self.s3_storage.read_json(test_key)  # Will fail but shows connectivity
                health_status['s3']['available'] = True
        except Exception as e:
            health_status['s3']['healthy'] = False
            health_status['s3']['available'] = False
            health_status['s3']['error'] = str(e)
        
        # Check GraphQL
        if self.graphql_service:
            try:
                if self.graphql_circuit_breaker:
                    cb_status = self.graphql_circuit_breaker.get_status()
                    health_status['graphql']['circuit_breaker'] = cb_status
                    health_status['graphql']['available'] = cb_status['state'] != 'open'
                else:
                    health_status['graphql']['available'] = True
            except Exception as e:
                health_status['graphql']['healthy'] = False
                health_status['graphql']['available'] = False
                health_status['graphql']['error'] = str(e)
        
        return health_status
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get UnifiedStorage metrics.
        
        Returns:
            Dictionary with comprehensive metrics including:
            - Cache statistics (hits, misses, hit rate)
            - Backend usage statistics
            - Error counts per backend
            - Configuration settings
        """
        total_cache_requests = self._metrics['cache_hits'] + self._metrics['cache_misses']
        cache_hit_rate = (
            (self._metrics['cache_hits'] / total_cache_requests * 100)
            if total_cache_requests > 0 else 0
        )
        
        return {
            'cache': {
                'hits': self._metrics['cache_hits'],
                'misses': self._metrics['cache_misses'],
                'hit_rate': round(cache_hit_rate, 2),
                'timeout': self.cache_timeout,
                'enabled': self.enable_caching
            },
            'backend_usage': self._metrics['backend_usage'].copy(),
            'errors': self._metrics['errors'].copy(),
            'configuration': {
                'use_local_json_files': self.use_local_json_files,
                'fallback_enabled': self.fallback_enabled,
                'request_deduplication_enabled': self.enable_request_deduplication,
                'graphql_service_available': self.graphql_service is not None,
            },
            'circuit_breakers': {
                's3': self.s3_circuit_breaker.get_status() if self.s3_circuit_breaker else None,
                'graphql': self.graphql_circuit_breaker.get_status() if self.graphql_circuit_breaker else None,
            }
        }
    
    def reset_metrics(self):
        """Reset all metrics counters."""
        self._metrics = {
            'cache_hits': 0,
            'cache_misses': 0,
            'backend_usage': {
                'local': 0,
                's3': 0,
                'graphql': 0
            },
            'errors': {
                'local': 0,
                's3': 0,
                'graphql': 0
            }
        }
        self.logger.debug("Metrics reset")
