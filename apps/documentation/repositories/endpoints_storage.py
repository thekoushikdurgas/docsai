"""Endpoints-specific storage logic for UnifiedStorage."""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from apps.documentation.repositories.unified_storage_base import BaseUnifiedStorage

logger = logging.getLogger(__name__)


class EndpointsStorageMixin:
    """Mixin providing endpoints get/list/count/statistics methods. Requires BaseUnifiedStorage."""

    def get_endpoint(self, endpoint_id: str) -> Optional[Dict[str, Any]]:
        cache_key = self._get_cache_key('endpoints', endpoint_id)
        cached = self._safe_cache_get(cache_key)
        if cached:
            self.logger.debug(f"Cache hit for endpoint: {endpoint_id}")
            return cached

        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            endpoint_data = repo.get_by_endpoint_id(endpoint_id)
            if endpoint_data:
                self.logger.debug(f"Loaded endpoint from S3: {endpoint_id}")
                self._safe_cache_set(cache_key, endpoint_data, self.cache_timeout)
                return endpoint_data
        except Exception as e:
            self.logger.warning(f"Failed to load endpoint from S3: {e}")

        self.logger.debug(f"Endpoint not found in any source: {endpoint_id}")
        return None

    def get_endpoints_bulk(self, endpoint_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        if not endpoint_ids:
            return {}
        ids = list(dict.fromkeys(endpoint_ids))
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
            endpoints_cached = cached.get("endpoints") or []
            if endpoints_cached or (cached.get("total") or 0) > 0:
                self.logger.debug("Cache hit for list_endpoints")
                return cached
            self.logger.debug("Skipping cached empty list_endpoints, retrying")

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
            self.logger.debug(f"Loaded {len(endpoints)} endpoints from S3")
            result = {'endpoints': endpoints, 'total': total, 'source': 's3'}
            if endpoints or total > 0:
                self._safe_cache_set(cache_key, result, self.cache_timeout)
            return result
        except Exception as e:
            self.logger.warning(f"Failed to load endpoints from S3: {e}")

        return {'endpoints': [], 'total': 0, 'source': 'none'}

    def get_endpoint_by_path_and_method(
        self, endpoint_path: str, method: str
    ) -> Optional[Dict[str, Any]]:
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.get_by_path_and_method(endpoint_path, method)
        except Exception as e:
            self.logger.warning(f"get_endpoint_by_path_and_method failed: {e}")
        return None

    def get_endpoints_by_api_version(self, api_version: str) -> List[Dict[str, Any]]:
        return self.list_endpoints(api_version=api_version, limit=None, offset=0).get("endpoints", [])

    def get_endpoints_by_method(self, method: str) -> List[Dict[str, Any]]:
        return self.list_endpoints(method=method, limit=None, offset=0).get("endpoints", [])

    def count_endpoints_by_api_version(self, api_version: str) -> int:
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.count_endpoints_by_api_version(api_version)
        except Exception as e:
            self.logger.warning(f"count_endpoints_by_api_version failed: {e}")
        return len(self.get_endpoints_by_api_version(api_version))

    def count_endpoints_by_method(self, method: str) -> int:
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.count_endpoints_by_method(method)
        except Exception as e:
            self.logger.warning(f"count_endpoints_by_method failed: {e}")
        return len(self.get_endpoints_by_method(method))

    def get_api_version_statistics(self) -> Dict[str, Any]:
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.get_api_version_statistics()
        except Exception as e:
            self.logger.warning(f"get_api_version_statistics failed: {e}")
        return {"versions": [], "total": 0}

    def get_method_statistics(self) -> Dict[str, Any]:
        try:
            from apps.documentation.repositories.endpoints_repository import EndpointsRepository
            repo = EndpointsRepository(storage=self.s3_storage)
            return repo.get_method_statistics()
        except Exception as e:
            self.logger.warning(f"get_method_statistics failed: {e}")
        return {"methods": [], "total": 0}
