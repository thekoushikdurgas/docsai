"""Relationships-specific storage logic for UnifiedStorage."""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from apps.documentation.repositories.unified_storage_base import BaseUnifiedStorage

logger = logging.getLogger(__name__)


class RelationshipsStorageMixin:
    """Mixin providing relationships get/list/statistics methods. Requires BaseUnifiedStorage."""

    def get_relationship(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        cache_key = self._get_cache_key("relationships", relationship_id)
        cached = self._safe_cache_get(cache_key)
        if cached:
            self.logger.debug(f"Cache hit for relationship: {relationship_id}")
            return cached

        try:
            from apps.documentation.repositories.relationships_repository import (
                RelationshipsRepository,
            )

            repo = RelationshipsRepository(storage=self.s3_storage)
            relationship_data = repo.get_by_relationship_id(relationship_id)
            if relationship_data:
                self.logger.debug(f"Loaded relationship from S3: {relationship_id}")
                self._safe_cache_set(cache_key, relationship_data, self.cache_timeout)
                return relationship_data
        except Exception as e:
            self.logger.warning(f"Failed to load relationship from S3: {e}")

        self.logger.debug(f"Relationship not found in any source: {relationship_id}")
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
        try:
            from apps.documentation.repositories.relationships_repository import (
                RelationshipsRepository,
            )

            repo = RelationshipsRepository(storage=self.s3_storage)
            rels = repo.list_all(
                page_id=page_id, endpoint_id=endpoint_id, limit=limit, offset=offset
            )
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
                edges.append(
                    {
                        "source": page_path,
                        "target": ep_key,
                        "usage_type": r.get("usage_type"),
                        "usage_context": r.get("usage_context"),
                    }
                )
        return {"nodes": nodes, "edges": edges}

    def get_relationships_by_page(self, page_path: str) -> Optional[Dict[str, Any]]:
        try:
            from apps.documentation.repositories.relationships_repository import (
                RelationshipsRepository,
            )
            from apps.documentation.repositories.pages_repository import PagesRepository

            repo = RelationshipsRepository(storage=self.s3_storage)
            pages_repo = PagesRepository(storage=self.s3_storage)
            page_data = pages_repo.get_by_route(page_path)
            if page_data:
                page_id = page_data.get("page_id")
                if page_id:
                    relationships = repo.get_by_page(page_id)
                    if relationships:
                        self.logger.debug(
                            f"Loaded relationships from S3 for page: {page_path}"
                        )
                        return {"relationships": relationships, "page_id": page_id}
        except Exception as e:
            self.logger.warning(f"Failed to load relationships from S3: {e}")
        return None

    def get_relationships_by_endpoint(
        self, endpoint_path: str, method: str = "QUERY"
    ) -> Optional[Dict[str, Any]]:
        try:
            from apps.documentation.repositories.relationships_repository import (
                RelationshipsRepository,
            )

            repo = RelationshipsRepository(storage=self.s3_storage)
            relationships = repo.get_by_endpoint(endpoint_path, method)
            if relationships:
                self.logger.debug(
                    f"Loaded relationships from S3 for endpoint: {endpoint_path}"
                )
                return {
                    "relationships": relationships,
                    "endpoint_path": endpoint_path,
                    "method": method,
                }
        except Exception as e:
            self.logger.warning(f"Failed to load relationships from S3: {e}")
        return None
