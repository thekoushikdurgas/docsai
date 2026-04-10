"""
GraphQL adapter for documentation API v1 — mirrors contact360.io/2 service shapes
using appointment360 GraphQL (documentation.* and docs.*).
"""

from __future__ import annotations

import logging
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

from apps.core.services.graphql_client import graphql_query

logger = logging.getLogger(__name__)

LIST_DOCUMENTATION_PAGES = """
query ListDocumentationPages(
  $pageType: String,
  $includeDrafts: Boolean,
  $includeDeleted: Boolean,
  $status: String
) {
  documentation {
    documentationPages(
      pageType: $pageType,
      includeDrafts: $includeDrafts,
      includeDeleted: $includeDeleted,
      status: $status
    ) {
      pages {
        pageId
        title
        description
        category
        contentUrl
        lastUpdated
        version
        id
      }
      total
    }
  }
}
"""

GET_DOCUMENTATION_PAGE = """
query GetDocumentationPage($pageId: String!, $pageType: String) {
  documentation {
    documentationPage(pageId: $pageId, pageType: $pageType) {
      pageId
      title
      description
      category
      contentUrl
      lastUpdated
      version
      id
    }
  }
}
"""

DOCS_STATS = """
query DocsStatsLite {
  docs {
    stats {
      totalPages
      totalEndpoints
      totalRelationships
      totalPostman
      pagesByType { type count }
      endpointsByMethod { method count }
    }
  }
}
"""

DOCS_RELATIONSHIPS = """
query DocsRelationships {
  docs {
    relationships {
      items {
        id
        pageId
        endpointId
        usageType
      }
    }
  }
}
"""


def _token(request) -> Optional[str]:
    if request is not None and hasattr(request, "session"):
        t = (request.session or {}).get("operator", {}).get("token")
        if t:
            return t
    return None


def _unwrap_errors(resp: Dict[str, Any]) -> Optional[str]:
    errs = resp.get("errors")
    if errs:
        return str(errs[0].get("message", errs))
    return None


def _transform_page(p: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "page_id": p.get("pageId"),
        "title": p.get("title"),
        "description": p.get("description"),
        "category": p.get("category"),
        "content_url": p.get("contentUrl"),
        "last_updated": p.get("lastUpdated"),
        "version": p.get("version"),
        "_id": p.get("id"),
        "metadata": {
            "title": p.get("title"),
            "description": p.get("description"),
            "category": p.get("category"),
            "page_type": p.get("pageType") or "docs",
            "last_updated": p.get("lastUpdated"),
            "version": p.get("version"),
        },
    }


class DocsGraphQLAdapter:
    """Facade used by API v1 views (request-aware for session token)."""

    def __init__(self, request=None):
        self.request = request
        self._token = _token(request)

    def list_pages(
        self,
        page_type: Optional[str] = None,
        include_drafts: bool = True,
        include_deleted: bool = False,
        status: Optional[str] = None,
        page_state: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Dict[str, Any]:
        variables: Dict[str, Any] = {
            "includeDrafts": include_drafts,
            "includeDeleted": include_deleted,
        }
        if page_type:
            variables["pageType"] = page_type
        if status:
            variables["status"] = status
        if page_state and not status:
            variables["status"] = page_state
        try:
            resp = graphql_query(LIST_DOCUMENTATION_PAGES, variables, token=self._token)
            err = _unwrap_errors(resp)
            if err:
                logger.warning("list_pages graphql errors: %s", err)
                return {"pages": [], "total": 0}
            data = (resp.get("data") or {}).get("documentation") or {}
            block = data.get("documentationPages") or {}
            raw_pages = block.get("pages") or []
            total = block.get("total", 0)
            pages = [_transform_page(p) for p in raw_pages]
            if limit is not None:
                pages = pages[offset : offset + limit]
            elif offset:
                pages = pages[offset:]
            return {"pages": pages, "total": total}
        except Exception as exc:
            logger.warning("list_pages failed: %s", exc)
            return {"pages": [], "total": 0}

    def get_page(
        self, page_id: str, page_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        variables: Dict[str, Any] = {"pageId": page_id}
        if page_type:
            variables["pageType"] = page_type
        try:
            resp = graphql_query(GET_DOCUMENTATION_PAGE, variables, token=self._token)
            if _unwrap_errors(resp):
                return None
            data = (resp.get("data") or {}).get("documentation") or {}
            p = data.get("documentationPage")
            if not p:
                return None
            return _transform_page(p)
        except Exception as exc:
            logger.warning("get_page failed: %s", exc)
            return None

    def count_pages_by_type(self, page_type: str) -> int:
        r = self.list_pages(page_type=page_type, limit=None, offset=0)
        return int(r.get("total", 0))

    def list_pages_by_user_type(
        self,
        user_type: str,
        page_type: Optional[str] = None,
        include_drafts: bool = True,
        include_deleted: bool = False,
        status: Optional[str] = None,
    ) -> Dict[str, Any]:
        # Gateway may not filter by user_type; return all pages for type (compat stub).
        return self.list_pages(
            page_type=page_type,
            include_drafts=include_drafts,
            include_deleted=include_deleted,
            status=status,
            limit=None,
            offset=0,
        )

    def relationships_items(self) -> List[Dict[str, Any]]:
        try:
            resp = graphql_query(DOCS_RELATIONSHIPS, token=self._token)
            if _unwrap_errors(resp):
                return []
            docs = (resp.get("data") or {}).get("docs") or {}
            rel = (docs.get("relationships") or {}).get("items") or []
            out = []
            for r in rel:
                rid = r.get("id")
                pid = r.get("pageId")
                eid = r.get("endpointId")
                ut = r.get("usageType")
                out.append(
                    {
                        "relationship_id": rid,
                        "id": rid,
                        "page_id": pid,
                        "page_path": pid,
                        "endpoint_id": eid,
                        "endpoint_path": eid,
                        "usage_type": ut,
                    }
                )
            return out
        except Exception as exc:
            logger.warning("relationships_items failed: %s", exc)
            return []

    def list_relationships(
        self,
        page_id: Optional[str] = None,
        endpoint_id: Optional[str] = None,
        usage_type: Optional[str] = None,
        usage_context: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Dict[str, Any]:
        items = self.relationships_items()
        if page_id:
            items = [x for x in items if x.get("page_id") == page_id]
        if endpoint_id:
            items = [x for x in items if x.get("endpoint_id") == endpoint_id]
        if usage_type:
            items = [
                x
                for x in items
                if (x.get("usage_type") or "").lower() == usage_type.lower()
            ]
        if usage_context:
            items = [
                x
                for x in items
                if (x.get("usage_context") or "").lower() == usage_context.lower()
            ]
        total = len(items)
        if limit is not None:
            items = items[offset : offset + limit]
        elif offset:
            items = items[offset:]
        return {"relationships": items, "total": total}

    def get_relationship(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        for r in self.relationships_items():
            if (
                r.get("relationship_id") == relationship_id
                or r.get("id") == relationship_id
            ):
                return r
        return None

    def list_endpoints(
        self,
        api_version: Optional[str] = None,
        method: Optional[str] = None,
        endpoint_state: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Derive minimal endpoint records from relationship endpointIds + docs.stats."""
        items_raw = self.relationships_items()
        seen: Dict[str, Dict[str, Any]] = {}
        for r in items_raw:
            eid = r.get("endpoint_id")
            if not eid:
                continue
            if eid not in seen:
                seen[eid] = {
                    "endpoint_id": eid,
                    "endpoint_path": eid,
                    "method": "GET",
                    "api_version": "v1",
                    "metadata": {},
                }
        endpoints = list(seen.values())
        try:
            resp = graphql_query(DOCS_STATS, token=self._token)
            if not _unwrap_errors(resp):
                stats = ((resp.get("data") or {}).get("docs") or {}).get("stats") or {}
                by_method = stats.get("endpointsByMethod") or []
                # enrich counts only — keep list from relationships
                _ = by_method
        except Exception:
            pass
        if api_version:
            endpoints = [
                e for e in endpoints if (e.get("api_version") or "") == api_version
            ]
        if method:
            endpoints = [
                e
                for e in endpoints
                if (e.get("method") or "").upper() == method.upper()
            ]
        if endpoint_state:
            endpoints = [
                e
                for e in endpoints
                if (e.get("endpoint_state") or e.get("state") or "") == endpoint_state
            ]
        total = len(endpoints)
        if limit is not None:
            endpoints = endpoints[offset : offset + limit]
        elif offset:
            endpoints = endpoints[offset:]
        return {"endpoints": endpoints, "total": total}

    def get_endpoint(self, endpoint_id: str) -> Optional[Dict[str, Any]]:
        r = self.list_endpoints(limit=None, offset=0)
        for e in r.get("endpoints", []):
            if e.get("endpoint_id") == endpoint_id:
                return e
        return None

    def list_configurations(
        self,
        state: Optional[str] = None,
        limit: Optional[int] = None,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """Postman configs not exposed on current GraphQL — return empty shape."""
        return {"configurations": [], "total": 0}

    def get_configuration(self, config_id: str) -> Optional[Dict[str, Any]]:
        return None

    def get_graph(self) -> Dict[str, Any]:
        items = self.relationships_items()
        edges = []
        for r in items:
            pid, eid = r.get("page_id"), r.get("endpoint_id")
            if pid and eid:
                edges.append(
                    {"source": pid, "target": eid, "label": r.get("usage_type")}
                )
        return {"nodes": [], "edges": edges}

    def get_statistics(self) -> Dict[str, Any]:
        items = self.relationships_items()
        pages = {r.get("page_id") for r in items if r.get("page_id")}
        eps = {r.get("endpoint_id") for r in items if r.get("endpoint_id")}
        by_ut: Counter = Counter()
        by_uc: Counter = Counter()
        for r in items:
            if r.get("usage_type"):
                by_ut[str(r["usage_type"])] += 1
            if r.get("usage_context"):
                by_uc[str(r["usage_context"])] += 1
        return {
            "total_relationships": len(items),
            "unique_pages": len(pages),
            "unique_endpoints": len(eps),
            "by_usage_type": dict(by_ut),
            "by_usage_context": dict(by_uc),
        }

    def get_postman_statistics(self) -> Dict[str, Any]:
        return {"total": 0, "statistics": {"total_configurations": 0}}

    def list_by_state(self, state: str) -> Dict[str, Any]:
        return {"configurations": [], "state": state, "total": 0}

    def count_by_state(self, state: str) -> int:
        return 0

    def get_collection(self, config_id: str):
        return None

    def get_environments(self, config_id: str):
        return []

    def get_environment(self, config_id: str, env_name: str):
        return None

    def get_endpoint_mappings(self, config_id: str):
        return []

    def get_test_suites(self, config_id: str):
        return []

    def get_test_suite(self, config_id: str, suite_id: str):
        return None

    def get_access_control(self, config_id: str):
        return None

    def get_api_version_statistics(self) -> Dict[str, Any]:
        eps = self.list_endpoints(limit=None, offset=0).get("endpoints", [])
        c = Counter((e.get("api_version") or "unknown") for e in eps)
        versions = [{"version": k, "count": v} for k, v in sorted(c.items())]
        return {"versions": versions, "total": len(versions)}

    def get_method_statistics(self) -> Dict[str, Any]:
        eps = self.list_endpoints(limit=None, offset=0).get("endpoints", [])
        c = Counter((e.get("method") or "UNKNOWN") for e in eps)
        methods = [{"method": k, "count": v} for k, v in sorted(c.items())]
        return {"methods": methods, "total": len(methods)}

    def get_endpoints_by_api_version(self, api_version: str) -> List[Dict[str, Any]]:
        return self.list_endpoints(api_version=api_version, limit=None, offset=0).get(
            "endpoints", []
        )

    def get_endpoints_by_version_and_method(
        self, api_version: str, method: str
    ) -> List[Dict[str, Any]]:
        eps = self.get_endpoints_by_api_version(api_version)
        return [e for e in eps if (e.get("method") or "").upper() == method.upper()]

    def count_endpoints_by_api_version(self, api_version: str) -> int:
        return len(self.get_endpoints_by_api_version(api_version))

    def count_endpoints_by_method(self, method: str) -> int:
        r = self.list_endpoints(method=method, limit=None, offset=0)
        return r.get("total", 0)

    def get_endpoints_by_method(self, method: str) -> List[Dict[str, Any]]:
        return self.list_endpoints(method=method, limit=None, offset=0).get(
            "endpoints", []
        )

    def count_endpoints_by_lambda(self, service_name: str) -> int:
        return 0

    def get_endpoints_by_lambda(self, service_name: str) -> List[Dict[str, Any]]:
        return []


def get_adapter(request=None) -> DocsGraphQLAdapter:
    return DocsGraphQLAdapter(request=request)
