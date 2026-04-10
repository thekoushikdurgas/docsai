"""Postman Discovery Service – discover collections and environments from S3."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from django.conf import settings

logger = logging.getLogger(__name__)

SKIP_FILES = {
    "auth.json",
    "vars.json",
    "index.json",
    "contact360.json",
    "requestly.json",
}


class PostmanDiscoveryService:
    """Discover Postman collections and environments from S3."""

    def __init__(self, s3_storage: Optional[Any] = None) -> None:
        if s3_storage is None:
            from apps.documentation.services import get_shared_s3_storage

            self.s3_storage = get_shared_s3_storage()
        else:
            self.s3_storage = s3_storage
        self.data_prefix = (
            getattr(settings, "S3_DATA_PREFIX", "data/") or "data/"
        ).rstrip("/") + "/"
        self.postman_prefix = f"{self.data_prefix}postman/"
        self.collections_prefix = f"{self.data_prefix}postman/collections/"
        self.environments_prefix = f"{self.data_prefix}postman/environments/"
        self.configurations_prefix = f"{self.data_prefix}postman/configurations/"

    def discover_all(self) -> Dict[str, Any]:
        """Discover all collections and environments. Returns unified index structure."""
        collections = self._discover_single_file_collections()
        folder_collections = self._discover_folder_collections()
        environments = self._discover_environments()
        configurations = self._discover_configurations()

        return {
            "version": "2.0",
            "last_updated": datetime.utcnow().isoformat(),
            "collections": collections,
            "folder_collections": folder_collections,
            "environments": environments,
            "configurations": configurations,
            "statistics": {
                "total": len(collections) + len(folder_collections) + len(environments),
                "collections": len(collections),
                "folder_collections": len(folder_collections),
                "environments": len(environments),
                "configurations": len(configurations),
            },
        }

    def _discover_single_file_collections(self) -> List[Dict[str, Any]]:
        """Discover collection JSON files in S3 under postman/collections/."""
        result: List[Dict[str, Any]] = []
        try:
            file_keys = self.s3_storage.list_json_files(
                self.collections_prefix, max_keys=10000
            )
            for s3_key in file_keys:
                if s3_key.endswith("/index.json"):
                    continue
                file_name = s3_key.split("/")[-1]
                if not file_name.endswith(".json"):
                    continue
                try:
                    data = self.s3_storage.read_json(s3_key)
                    info = (data or {}).get("info", {})
                    name = info.get(
                        "name",
                        file_name.replace(".postman_collection.json", "")
                        .replace(".json", "")
                        .replace("_", " "),
                    )
                    relative_path = (
                        s3_key[len(self.data_prefix) :]
                        if s3_key.startswith(self.data_prefix)
                        else s3_key
                    )
                    result.append(
                        {
                            "collection_id": name,
                            "file_name": file_name,
                            "relative_path": relative_path.replace("\\", "/"),
                            "type": "collection",
                            "format": "postman",
                        }
                    )
                except (OSError, ValueError) as e:
                    logger.warning("Discovery skip %s: %s", s3_key, e)
                    continue
        except Exception as e:
            logger.warning("Discovery list collections failed: %s", e)
        result.sort(key=lambda x: (x["collection_id"].lower(), x["file_name"]))
        return result

    def _discover_folder_collections(self) -> List[Dict[str, Any]]:
        """Folder collections (Requestly-style) are not stored as S3 prefixes; return empty."""
        return []

    def _discover_environments(self) -> List[Dict[str, Any]]:
        """Discover environment JSON files in S3 under postman/environments/."""
        result: List[Dict[str, Any]] = []
        try:
            file_keys = self.s3_storage.list_json_files(
                self.environments_prefix, max_keys=10000
            )
            for s3_key in file_keys:
                if s3_key.endswith("/index.json"):
                    continue
                file_name = s3_key.split("/")[-1]
                if not file_name.endswith(".json"):
                    continue
                try:
                    data = self.s3_storage.read_json(s3_key)
                    name = (data or {}).get(
                        "name",
                        file_name.replace(".postman_environment.json", "").replace(
                            ".json", ""
                        ),
                    )
                    relative_path = (
                        s3_key[len(self.data_prefix) :]
                        if s3_key.startswith(self.data_prefix)
                        else s3_key
                    )
                    result.append(
                        {
                            "environment_id": name,
                            "file_name": file_name,
                            "relative_path": relative_path.replace("\\", "/"),
                            "type": "environment",
                            "format": "postman",
                        }
                    )
                except (OSError, ValueError) as e:
                    logger.warning("Discovery skip env %s: %s", s3_key, e)
        except Exception as e:
            logger.warning("Discovery list environments failed: %s", e)
        result.sort(key=lambda x: (x["environment_id"].lower(), x["relative_path"]))
        return result

    def _discover_configurations(self) -> List[Dict[str, Any]]:
        """Discover configuration JSON files in S3 under postman/configurations/."""
        result: List[Dict[str, Any]] = []
        try:
            file_keys = self.s3_storage.list_json_files(
                self.configurations_prefix, max_keys=10000
            )
            for s3_key in file_keys:
                if s3_key.endswith("/index.json"):
                    continue
                file_name = s3_key.split("/")[-1]
                if not file_name.endswith(".json"):
                    continue
                try:
                    data = self.s3_storage.read_json(s3_key)
                    if not data:
                        continue
                    config_id = file_name.replace(".json", "")
                    result.append(
                        {
                            "config_id": config_id,
                            "name": data.get("name", config_id),
                            "state": data.get("state", "development"),
                            "file_name": file_name,
                            "type": "configuration",
                        }
                    )
                except Exception:
                    pass
        except Exception as e:
            logger.warning("Discovery list configurations failed: %s", e)
        result.sort(key=lambda x: x.get("config_id", "").lower())
        return result

    def get_index(self) -> Dict[str, Any]:
        """Return discovery result with all collections and environments."""
        return self.discover_all()
