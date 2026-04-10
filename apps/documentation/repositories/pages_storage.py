"""Pages-specific storage logic for UnifiedStorage."""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Sequence

from apps.documentation.repositories.unified_storage_base import (
    BaseUnifiedStorage,
    StorageBackend,
)
from apps.documentation.repositories.s3_json_storage import _local_path_for_s3_key
from apps.core.exceptions import RepositoryError

from django.conf import settings


class PagesStorageMixin:
    """Mixin providing pages get/list/count/statistics methods. Requires BaseUnifiedStorage."""

    def get_page(
        self, page_id: str, page_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        cache_key = self._get_cache_key("pages", page_id)
        cached = self._safe_cache_get(cache_key)
        if cached:
            self.logger.debug(f"Cache hit for page: {page_id}")
            if page_type and cached.get("page_type") != page_type:
                return None
            return cached

        def _fetch_from_s3():
            from apps.documentation.repositories.pages_repository import PagesRepository

            repo = PagesRepository(storage=self.s3_storage)
            if self.s3_circuit_breaker:
                return self.s3_circuit_breaker.call(
                    repo.get_by_page_id, page_id, page_type
                )
            return repo.get_by_page_id(page_id, page_type)

        page_data = None
        try:
            if self.enable_request_deduplication and self.request_deduplicator:
                request_key = self._get_request_key(
                    "pages", "s3_get", page_id=page_id, page_type=page_type
                )
                page_data = self.request_deduplicator.execute(
                    request_key, _fetch_from_s3
                )
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
                    error_code="S3_STORAGE_FAILED",
                ) from e

        if self.graphql_service:
            try:
                if self.graphql_circuit_breaker:
                    page_data = self.graphql_circuit_breaker.call(
                        self.graphql_service.get_page, page_id, page_type
                    )
                else:
                    page_data = self.graphql_service.get_page(page_id, page_type)
                if page_data:
                    self._track_backend_usage(StorageBackend.GRAPHQL, success=True)
                    self.logger.debug(f"Loaded page from GraphQL: {page_id}")
                    self._safe_cache_set(cache_key, page_data, self.cache_timeout)
                    return page_data
            except Exception as e:
                self._handle_backend_error(
                    StorageBackend.GRAPHQL, e, f"get_page({page_id})"
                )

        s3_key = f"{getattr(settings, 'S3_DATA_PREFIX', 'data/')}pages/{page_id}.json"
        local_path = _local_path_for_s3_key(s3_key)
        if local_path and local_path.is_file():
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    page_data = json.load(f)
                if page_data and (
                    not page_type or page_data.get("page_type") == page_type
                ):
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
        offset: int = 0,
    ) -> Dict[str, Any]:
        if page_types is not None and len(page_types) == 0:
            page_types = None
        effective_types = list(page_types) if page_types else None
        filters = {
            "page_type": effective_types if effective_types else page_type,
            "page_types": effective_types,
            "status": status,
            "page_state": page_state,
            "include_drafts": include_drafts,
            "include_deleted": include_deleted,
            "limit": limit,
            "offset": offset,
        }
        cache_key = self._get_cache_key("pages", None, filters)
        cached = self._safe_cache_get(cache_key)
        if cached is not None:
            return cached

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
                offset=offset,
            )
            pages = out.get("pages", []) if isinstance(out, dict) else out
            total = (
                out.get("total", len(pages)) if isinstance(out, dict) else len(pages)
            )
            self.logger.debug(f"Loaded {len(pages)} pages from S3, total={total}")
            result = {"pages": pages, "total": total, "source": "s3"}
            self._safe_cache_set(cache_key, result, self.cache_timeout)
            return result
        except Exception as e:
            self.logger.warning(f"Failed to load pages from S3: {e}")

        return {"pages": [], "total": 0, "source": "none"}

    def get_pages_by_type(
        self,
        page_type: str,
        status: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        result = self.list_pages(page_type=page_type, limit=None, offset=0)
        pages = result.get("pages", [])
        if status:
            pages = [
                p for p in pages if (p.get("metadata") or {}).get("status") == status
            ]
        return pages

    def count_pages_by_type(self, page_type: str) -> int:
        try:
            from apps.documentation.repositories.pages_repository import PagesRepository

            repo = PagesRepository(storage=self.s3_storage)
            return repo.count_pages_by_type(page_type)
        except Exception as e:
            self.logger.warning(f"S3 count_pages_by_type failed: {e}")
        return 0

    def get_type_statistics(self) -> Dict[str, Any]:
        try:
            from apps.documentation.repositories.pages_repository import PagesRepository

            repo = PagesRepository(storage=self.s3_storage)
            return repo.get_type_statistics()
        except Exception as e:
            self.logger.warning(f"get_type_statistics failed: {e}")
        result = self.list_pages(limit=None, offset=0)
        pages = result.get("pages", [])
        from apps.documentation.constants import PAGE_TYPES

        count_by_type = {
            pt: {"published": 0, "draft": 0, "deleted": 0, "total": 0}
            for pt in PAGE_TYPES
        }
        for p in pages:
            pt = p.get("page_type", "docs")
            if pt not in count_by_type:
                count_by_type[pt] = {
                    "published": 0,
                    "draft": 0,
                    "deleted": 0,
                    "total": 0,
                }
            st = (p.get("metadata") or {}).get("status", "published")
            count_by_type[pt]["total"] += 1
            if st == "published":
                count_by_type[pt]["published"] += 1
            elif st == "draft":
                count_by_type[pt]["draft"] += 1
            elif st == "deleted":
                count_by_type[pt]["deleted"] += 1
        statistics = [
            {
                "type": t,
                "count": v["total"],
                "published": v["published"],
                "draft": v["draft"],
                "deleted": v["deleted"],
            }
            for t, v in count_by_type.items()
        ]
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
        valid_user_types = [
            "super_admin",
            "admin",
            "pro_user",
            "free_user",
            "guest",
            "public",
        ]
        if user_type not in valid_user_types:
            raise ValueError(
                f"Invalid user_type: {user_type}. Must be one of {valid_user_types}"
            )
        result = self.list_pages(
            page_type=page_type,
            include_drafts=include_drafts,
            include_deleted=include_deleted,
            status=status,
            limit=None,
            offset=0,
        )
        _key_map = {
            "freeUser": "free_user",
            "proUser": "pro_user",
            "superAdmin": "super_admin",
        }
        pages = result.get("pages", [])
        filtered = []
        for page in pages:
            ac = (
                page.get("access_control")
                or page.get("metadata", {}).get("access_control")
                or {}
            )
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
            filtered = filtered[offset : offset + limit]
        else:
            filtered = filtered[offset:]
        return {"pages": filtered, "total": total}
