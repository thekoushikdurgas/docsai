"""Index Generator – rebuild S3 index.json for pages, endpoints, postman, relationships from S3."""

import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from django.conf import settings

from apps.documentation.constants import PAGE_TYPES

logger = logging.getLogger(__name__)

INDEX_KEY_SUFFIX = "/index.json"


class IndexGeneratorService:
    """Generate index.json in S3 for each resource type by listing and reading S3 keys."""

    def __init__(self) -> None:
        from apps.documentation.services import (
            get_shared_s3_storage,
            get_shared_s3_index_manager,
        )

        self.storage = get_shared_s3_storage()
        self.index_manager = get_shared_s3_index_manager()
        self.data_prefix = (
            getattr(settings, "S3_DATA_PREFIX", "data/") or "data/"
        ).rstrip("/") + "/"

    def generate_pages_index(self, use_parallel: bool = True) -> Dict[str, Any]:
        """Build pages index from S3 and write via S3IndexManager. Returns {success, index_path, total, error}."""
        try:
            prefix = f"{self.data_prefix}pages/"
            keys = self.storage.list_json_files(prefix, max_keys=10000)
            keys = [k for k in keys if not k.endswith(INDEX_KEY_SUFFIX)]

            page_states = ("coming_soon", "published", "draft", "development", "test")
            pages: List[Dict[str, Any]] = []
            indexes: Dict[str, Any] = {
                "by_type": {pt: [] for pt in PAGE_TYPES},
                "by_route": {},
            }
            stats: Dict[str, Any] = {
                "total": 0,
                "by_type": {pt: 0 for pt in PAGE_TYPES},
                "by_page_state": {ps: 0 for ps in page_states},
            }

            for s3_key in keys:
                data = self.storage.read_json(s3_key)
                if not isinstance(data, dict):
                    continue
                pid = data.get("page_id") or s3_key.split("/")[-1].replace(".json", "")
                ptype = data.get("page_type", "docs")
                metadata = data.get("metadata")
                route = (
                    (metadata.get("route", "") if isinstance(metadata, dict) else "")
                    if metadata
                    else ""
                )
                page_state = (
                    metadata.get("page_state", "") if isinstance(metadata, dict) else ""
                ) or "draft"
                if page_state not in stats["by_page_state"]:
                    stats["by_page_state"][page_state] = 0
                stats["by_page_state"][page_state] += 1
                file_name = s3_key.split("/")[-1]
                pages.append(
                    {
                        "page_id": pid,
                        "page_type": ptype,
                        "route": route,
                        "file_name": file_name,
                    }
                )
                if ptype in indexes["by_type"] and pid not in indexes["by_type"][ptype]:
                    indexes["by_type"][ptype].append(pid)
                if route:
                    indexes["by_route"][route] = pid
                stats["total"] += 1
                if ptype in stats["by_type"]:
                    stats["by_type"][ptype] += 1

            payload = {
                "version": "2.0",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total": len(pages),
                "pages": pages,
                "indexes": indexes,
                "statistics": stats,
            }
            self.index_manager.update_index("pages", payload)
            logger.debug("Generated pages index with %d pages from S3", len(pages))
            return {
                "success": True,
                "index_path": f"{self.data_prefix}pages/index.json",
                "total": len(pages),
            }
        except Exception as e:
            logger.exception("generate_pages_index")
            return {"success": False, "error": str(e)}

    def generate_endpoints_index(self, use_parallel: bool = True) -> Dict[str, Any]:
        """Build endpoints index from S3 and write via S3IndexManager."""
        try:
            prefix = f"{self.data_prefix}endpoints/"
            keys = self.storage.list_json_files(prefix, max_keys=10000)
            keys = [k for k in keys if not k.endswith(INDEX_KEY_SUFFIX)]

            endpoints: List[Dict[str, Any]] = []
            indexes: Dict[str, Any] = {
                "by_method": {},
                "by_api_version": {},
                "by_path": {},
            }
            stats: Dict[str, Any] = {"total": 0, "by_method": {}, "by_api_version": {}}

            for s3_key in keys:
                data = self.storage.read_json(s3_key)
                if not isinstance(data, dict):
                    continue
                eid = data.get("endpoint_id") or s3_key.split("/")[-1].replace(
                    ".json", ""
                )
                method = data.get("method", "GET")
                api_version = data.get("api_version", "v1")
                path = data.get("endpoint_path") or data.get("path", "")
                file_name = s3_key.split("/")[-1]
                endpoints.append(
                    {
                        "endpoint_id": eid,
                        "method": method,
                        "api_version": api_version,
                        "path": path,
                        "file_name": file_name,
                    }
                )
                indexes["by_method"].setdefault(method, []).append(eid)
                indexes["by_api_version"].setdefault(api_version, []).append(eid)
                if path:
                    indexes["by_path"][path] = eid
                stats["total"] += 1
                stats["by_method"][method] = stats["by_method"].get(method, 0) + 1
                stats["by_api_version"][api_version] = (
                    stats["by_api_version"].get(api_version, 0) + 1
                )

            payload = {
                "version": "2.0",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total": len(endpoints),
                "endpoints": endpoints,
                "indexes": indexes,
                "statistics": stats,
            }
            self.index_manager.update_index("endpoints", payload)
            logger.debug(
                "Generated endpoints index with %d endpoints from S3", len(endpoints)
            )
            return {
                "success": True,
                "index_path": f"{self.data_prefix}endpoints/index.json",
                "total": len(endpoints),
            }
        except Exception as e:
            logger.exception("generate_endpoints_index")
            return {"success": False, "error": str(e)}

    def generate_postman_index(self) -> Dict[str, Any]:
        """Build postman index from S3 (collections, environments, configurations) and write via S3IndexManager."""
        try:
            collections: List[Dict[str, Any]] = []
            environments: List[Dict[str, Any]] = []
            configurations: List[Dict[str, Any]] = []

            for sub in ("collections", "environments", "configurations"):
                prefix = f"{self.data_prefix}postman/{sub}/"
                keys = self.storage.list_json_files(prefix, max_keys=10000)
                keys = [k for k in keys if not k.endswith(INDEX_KEY_SUFFIX)]
                for s3_key in keys:
                    data = self.storage.read_json(s3_key)
                    if not isinstance(data, dict):
                        continue
                    file_name = s3_key.split("/")[-1]
                    try:
                        if sub == "collections":
                            name = (data.get("info") or {}).get(
                                "name"
                            ) or file_name.replace(".json", "")
                            collections.append(
                                {
                                    "collection_id": name,
                                    "file_name": file_name,
                                    "type": "collection",
                                }
                            )
                        elif sub == "environments":
                            name = data.get("name") or file_name.replace(".json", "")
                            environments.append(
                                {
                                    "environment_id": name,
                                    "file_name": file_name,
                                    "type": "environment",
                                }
                            )
                        else:
                            cid = (
                                data.get("config_id")
                                or data.get("name")
                                or file_name.replace(".json", "")
                            )
                            configurations.append(
                                {
                                    "config_id": cid,
                                    "name": data.get("name", cid),
                                    "state": data.get("state", "development"),
                                    "file_name": file_name,
                                }
                            )
                    except Exception as e:
                        logger.warning("index postman %s skip %s: %s", sub, s3_key, e)

            indexes = {
                "by_state": {
                    "coming_soon": [],
                    "development": [],
                    "draft": [],
                    "test": [],
                    "published": [],
                }
            }
            for c in configurations:
                s = c.get("state", "development")
                if (
                    s in indexes["by_state"]
                    and c["config_id"] not in indexes["by_state"][s]
                ):
                    indexes["by_state"][s].append(c["config_id"])
            stats = {
                "total": len(configurations),
                "collections": len(collections),
                "environments": len(environments),
                "configurations": len(configurations),
            }
            payload = {
                "version": "2.0",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total": len(configurations),
                "collections": collections,
                "environments": environments,
                "configurations": configurations,
                "indexes": indexes,
                "statistics": stats,
            }
            self.index_manager.update_index("postman", payload)
            logger.debug(
                "Generated postman index from S3: %d collections, %d envs, %d configs",
                len(collections),
                len(environments),
                len(configurations),
            )
            return {
                "success": True,
                "index_path": f"{self.data_prefix}postman/index.json",
                "total": len(configurations),
                "collections": len(collections),
                "environments": len(environments),
            }
        except Exception as e:
            logger.exception("generate_postman_index")
            return {"success": False, "error": str(e)}

    def generate_relationships_index(self) -> Dict[str, Any]:
        """Build relationships index from S3 (by-page and by-endpoint keys) and write via S3IndexManager."""
        try:
            relationships: List[Dict[str, Any]] = []
            prefix = f"{self.data_prefix}relationships/"
            keys = self.storage.list_json_files(prefix, max_keys=10000)
            keys = [k for k in keys if not k.endswith(INDEX_KEY_SUFFIX)]

            for s3_key in keys:
                data = self.storage.read_json(s3_key)
                if data is None:
                    continue
                if isinstance(data, list):
                    relationships.extend(data)
                else:
                    relationships.append(data)

            indexes: Dict[str, Any] = {
                "by_page": {},
                "by_endpoint": {},
                "by_usage_type": {"primary": [], "secondary": [], "conditional": []},
            }
            stats: Dict[str, Any] = {"total": len(relationships)}
            for r in relationships:
                if not isinstance(r, dict):
                    continue
                pp = r.get("page_path")
                ep = r.get("endpoint_path")
                if pp:
                    indexes["by_page"].setdefault(pp, []).append(
                        r.get("relationship_id", "")
                    )
                if ep:
                    key = f"{ep}:{r.get('method', 'GET')}"
                    indexes["by_endpoint"].setdefault(key, []).append(
                        r.get("relationship_id", "")
                    )

            payload = {
                "version": "2.0",
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "total": len(relationships),
                "relationships": relationships,
                "indexes": indexes,
                "statistics": stats,
            }
            self.index_manager.update_index("relationships", payload)
            logger.debug(
                "Generated relationships index with %d entries from S3",
                len(relationships),
            )
            return {
                "success": True,
                "index_path": f"{self.data_prefix}relationships/index.json",
                "total": len(relationships),
            }
        except Exception as e:
            logger.exception("generate_relationships_index")
            return {"success": False, "error": str(e)}

    def generate_all_indexes(
        self, parallel: bool = True, max_workers: int = 4
    ) -> Dict[str, Any]:
        """Run all four generators. parallel/max_workers kept for API compatibility; S3 reads are sequential."""
        generators = [
            ("pages", lambda: self.generate_pages_index()),
            ("endpoints", lambda: self.generate_endpoints_index()),
            ("postman", self.generate_postman_index),
            ("relationships", self.generate_relationships_index),
        ]
        results: Dict[str, Any] = {}
        ok = True
        for name, fn in generators:
            try:
                out = fn()
                results[name] = out
                if not out.get("success"):
                    ok = False
            except Exception as e:
                logger.error("Error generating %s index: %s", name, e, exc_info=True)
                results[name] = {"success": False, "error": str(e)}
                ok = False
        return {"success": ok, "results": results}
