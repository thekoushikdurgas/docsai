"""Base class for UnifiedStorage with shared infrastructure (cache, circuit breakers, metrics)."""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod
from enum import Enum

from django.conf import settings
from django.core.cache import cache

from apps.documentation.repositories.s3_json_storage import S3JSONStorage

try:
    from apps.documentation.services.graphql_documentation_service import GraphQLDocumentationService
except ImportError:
    GraphQLDocumentationService = None

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


class BaseUnifiedStorage:
    """Base class with shared cache, circuit breakers, metrics, and common helpers."""

    def __init__(
        self,
        s3_storage: Optional[S3JSONStorage] = None,
        graphql_service: Optional[GraphQLDocumentationService] = None,
    ):
        if s3_storage is None:
            from apps.documentation.services import get_shared_s3_storage
            self.s3_storage = get_shared_s3_storage()
        else:
            self.s3_storage = s3_storage

        self.graphql_service = None
        if getattr(settings, 'GRAPHQL_ENABLED', False) and GraphQLDocumentationService:
            try:
                self.graphql_service = graphql_service or GraphQLDocumentationService()
            except Exception as e:
                logger.warning(f"Failed to initialize GraphQL service: {e}")

        self.use_local_json_files = False
        self.cache_timeout = getattr(settings, 'UNIFIED_STORAGE_CACHE_TTL', 300)
        self.enable_request_deduplication = getattr(settings, 'ENABLE_REQUEST_DEDUPLICATION', True)
        self.enable_caching = getattr(settings, 'UNIFIED_STORAGE_ENABLE_CACHE', True)
        self.fallback_enabled = getattr(settings, 'UNIFIED_STORAGE_FALLBACK_ENABLED', True)

        self._pending_requests: Dict[str, Any] = {}
        try:
            from apps.core.utils.request_deduplication import RequestDeduplicator
            self.request_deduplicator = RequestDeduplicator(cache_timeout=self.cache_timeout)
        except Exception as e:
            logger.warning(f"Failed to initialize request deduplicator: {e}")
            self.request_deduplicator = None

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

        self._metrics: Dict[str, Any] = {
            'cache_hits': 0,
            'cache_misses': 0,
            'backend_usage': {'local': 0, 's3': 0, 'graphql': 0},
            'errors': {'local': 0, 's3': 0, 'graphql': 0}
        }

        self.logger = logging.getLogger(f"{__name__}.BaseUnifiedStorage")
        self.logger.debug(f"BaseUnifiedStorage initialized (caching={self.enable_caching}, fallback={self.fallback_enabled})")

    def _get_cache_key(self, resource_type: str, identifier: str = None, filters: Optional[Dict] = None) -> str:
        if identifier:
            return f"unified_storage:{resource_type}:{identifier}"
        if filters:
            parts = []
            for k, v in sorted(filters.items()):
                if v is not None:
                    seg = self._cache_key_filter_value(v)
                    if seg:
                        parts.append(f"{k}={seg}")
            if parts:
                return f"unified_storage:{resource_type}:list:{':'.join(parts)}"
        return f"unified_storage:{resource_type}:all"

    @staticmethod
    def _cache_key_filter_value(value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, (list, tuple)):
            return ",".join(sorted(str(x) for x in value))
        return str(value)

    def _get_request_key(self, resource_type: str, operation: str, **kwargs) -> str:
        key_parts = [resource_type, operation]
        for k, v in sorted(kwargs.items()):
            if v is not None:
                key_parts.append(f"{k}={v}")
        return ':'.join(key_parts)

    def _safe_cache_get(self, key: str, default: Any = None) -> Any:
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

    def _safe_cache_delete(self, key: str) -> bool:
        try:
            cache.delete(key)
            return True
        except Exception as e:
            self.logger.warning(f"Cache delete failed for key {key}: {e}")
            return False

    def _track_backend_usage(self, backend: StorageBackend, success: bool = True):
        backend_name = backend.value
        if success:
            self._metrics['backend_usage'][backend_name] = self._metrics['backend_usage'].get(backend_name, 0) + 1
        else:
            self._metrics['errors'][backend_name] = self._metrics['errors'].get(backend_name, 0) + 1

    def _handle_backend_error(self, backend: StorageBackend, error: Exception, operation: str) -> None:
        self._track_backend_usage(backend, success=False)
        self.logger.warning(f"Backend {backend.value} failed for operation {operation}: {error}", exc_info=True)

    def clear_cache(self, resource_type: str = None, identifier: str = None, filters: Optional[Dict] = None):
        try:
            from apps.core.utils.redis_cache import RedisCacheManager
            cache_manager = RedisCacheManager()
            if resource_type and identifier:
                cache_key = self._get_cache_key(resource_type, identifier)
                deleted = cache_manager.delete(cache_key)
                self.logger.debug(f"Cleared cache for {resource_type}:{identifier} (deleted: {deleted})")
            elif resource_type:
                pattern = f"unified_storage:{resource_type}:*"
                deleted = cache_manager.delete_pattern(pattern)
                self.logger.debug(f"Cleared cache for resource type '{resource_type}' (deleted {deleted} keys)")
            else:
                pattern = "unified_storage:*"
                deleted = cache_manager.delete_pattern(pattern)
                self.logger.debug(f"Cleared all unified_storage cache (deleted {deleted} keys)")
        except ImportError:
            if resource_type and identifier:
                cache_key = self._get_cache_key(resource_type, identifier)
                self._safe_cache_delete(cache_key)
                self.logger.debug(f"Cleared cache for {resource_type}:{identifier}")
            elif resource_type:
                self.logger.warning(
                    f"Cache clear for resource type '{resource_type}' requires Redis backend for pattern deletion."
                )
            else:
                self.logger.warning("Cache clear for all resources requires Redis backend for pattern deletion.")

    def check_health(self) -> Dict[str, Any]:
        health_status = {
            'local': {'healthy': False, 'available': False, 'message': 'removed (S3-only)'},
            's3': {'healthy': True, 'available': False},
            'graphql': {'healthy': True, 'available': False}
        }
        try:
            if self.s3_circuit_breaker:
                cb_status = self.s3_circuit_breaker.get_status()
                health_status['s3']['circuit_breaker'] = cb_status
                health_status['s3']['available'] = cb_status['state'] != 'open'
            else:
                test_key = f"{self.s3_storage.data_prefix}health_check.json"
                self.s3_storage.read_json(test_key)
                health_status['s3']['available'] = True
        except Exception as e:
            health_status['s3']['healthy'] = False
            health_status['s3']['available'] = False
            health_status['s3']['error'] = str(e)

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
        self._metrics = {
            'cache_hits': 0,
            'cache_misses': 0,
            'backend_usage': {'local': 0, 's3': 0, 'graphql': 0},
            'errors': {'local': 0, 's3': 0, 'graphql': 0}
        }
        self.logger.debug("Metrics reset")
