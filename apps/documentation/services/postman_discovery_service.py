"""Postman Discovery Service – scan media/postman/ for collections and environments."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from apps.documentation.utils.paths import get_media_root, get_postman_dir, list_directory_files

logger = logging.getLogger(__name__)

SKIP_FILES = {"auth.json", "vars.json", "index.json", "contact360.json", "requestly.json"}


class PostmanDiscoveryService:
    """Discover Postman collections and environments from media/postman/."""

    def __init__(self) -> None:
        self.media_root = get_media_root()
        self.postman_dir = get_postman_dir()

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
        """Discover .postman_collection.json files at postman root."""
        result: List[Dict[str, Any]] = []
        if not self.postman_dir.exists() or not self.postman_dir.is_dir():
            return result

        for fp in self.postman_dir.iterdir():
            if not fp.is_file():
                continue
            if not fp.name.endswith(".postman_collection.json"):
                continue
            try:
                rel = fp.relative_to(self.media_root)
                rel_str = str(rel).replace("\\", "/")
                name = fp.stem.replace(".postman_collection", "").replace("_", " ")
                try:
                    data = json.loads(fp.read_text(encoding="utf-8"))
                    info = data.get("info", {})
                    name = info.get("name", name)
                except Exception:
                    pass
                result.append({
                    "collection_id": name,
                    "file_name": fp.name,
                    "relative_path": rel_str,
                    "type": "collection",
                    "format": "postman",
                })
            except (OSError, ValueError) as e:
                logger.warning("Discovery skip %s: %s", fp, e)
                continue

        result.sort(key=lambda x: (x["collection_id"].lower(), x["file_name"]))
        return result

    def _discover_folder_collections(self) -> List[Dict[str, Any]]:
        """Discover Requestly-style folder collections (top-level dirs with request JSONs)."""
        result: List[Dict[str, Any]] = []
        if not self.postman_dir.exists() or not self.postman_dir.is_dir():
            return result

        for fp in self.postman_dir.iterdir():
            if not fp.is_dir():
                continue
            if fp.name in ("collection", "environment", "environments", "configurations"):
                continue
            try:
                if self._looks_like_requestly_folder(fp):
                    rel = fp.relative_to(self.media_root)
                    rel_str = str(rel).replace("\\", "/")
                    result.append({
                        "collection_id": fp.name,
                        "relative_path": rel_str,
                        "type": "folder_collection",
                        "format": "requestly",
                    })
            except (OSError, ValueError) as e:
                logger.warning("Discovery skip folder %s: %s", fp, e)
                continue

        result.sort(key=lambda x: x["collection_id"].lower())
        return result

    def _looks_like_requestly_folder(self, folder: Path) -> bool:
        """Check if folder contains Requestly-style request JSONs."""
        count = 0
        for _ in folder.rglob("*.json"):
            count += 1
            if count >= 1:
                break
        if count == 0:
            return False
        for fp in folder.rglob("*.json"):
            if fp.name in SKIP_FILES:
                continue
            try:
                data = json.loads(fp.read_text(encoding="utf-8"))
                if isinstance(data, dict) and "request" in data:
                    return True
            except Exception:
                continue
        return False

    def _discover_environments(self) -> List[Dict[str, Any]]:
        """Discover environment files (root .postman_environment.json + postman/environments/*.json)."""
        result: List[Dict[str, Any]] = []

        if self.postman_dir.exists():
            for fp in self.postman_dir.iterdir():
                if not fp.is_file():
                    continue
                if not fp.name.endswith(".postman_environment.json"):
                    continue
                try:
                    rel = fp.relative_to(self.media_root)
                    rel_str = str(rel).replace("\\", "/")
                    name = fp.stem.replace(".postman_environment", "").replace("_", " ")
                    try:
                        data = json.loads(fp.read_text(encoding="utf-8"))
                        name = data.get("name", name)
                    except Exception:
                        pass
                    result.append({
                        "environment_id": name,
                        "file_name": fp.name,
                        "relative_path": rel_str,
                        "type": "environment",
                        "format": "postman",
                    })
                except (OSError, ValueError) as e:
                    logger.warning("Discovery skip env %s: %s", fp, e)

        env_dir = self.postman_dir / "environments"
        if env_dir.exists() and env_dir.is_dir():
            for fp in env_dir.iterdir():
                if not fp.is_file() or fp.suffix.lower() != ".json":
                    continue
                try:
                    rel = fp.relative_to(self.media_root)
                    rel_str = str(rel).replace("\\", "/")
                    name = fp.stem
                    try:
                        data = json.loads(fp.read_text(encoding="utf-8"))
                        name = data.get("name", name)
                    except Exception:
                        pass
                    result.append({
                        "environment_id": name,
                        "file_name": fp.name,
                        "relative_path": rel_str,
                        "type": "environment",
                        "format": "requestly",
                    })
                except (OSError, ValueError) as e:
                    logger.warning("Discovery skip env %s: %s", fp, e)

        result.sort(key=lambda x: (x["environment_id"].lower(), x["relative_path"]))
        return result

    def _discover_configurations(self) -> List[Dict[str, Any]]:
        """Discover configuration files."""
        result: List[Dict[str, Any]] = []
        config_dir = self.postman_dir / "configurations"
        if not config_dir.exists() or not config_dir.is_dir():
            for fp in self.postman_dir.iterdir() if self.postman_dir.exists() else []:
                if not fp.is_file():
                    continue
                if fp.name in ("contact360.json", "requestly.json"):
                    try:
                        data = json.loads(fp.read_text(encoding="utf-8"))
                        result.append({
                            "config_id": fp.stem,
                            "name": data.get("name", fp.stem),
                            "state": data.get("state", "development"),
                            "file_name": fp.name,
                            "type": "configuration",
                        })
                    except Exception:
                        pass
        else:
            for fp in config_dir.iterdir():
                if not fp.is_file() or fp.suffix.lower() != ".json":
                    continue
                try:
                    data = json.loads(fp.read_text(encoding="utf-8"))
                    result.append({
                        "config_id": fp.stem,
                        "name": data.get("name", fp.stem),
                        "state": data.get("state", "development"),
                        "file_name": fp.name,
                        "type": "configuration",
                    })
                except Exception:
                    pass

        result.sort(key=lambda x: x.get("config_id", "").lower())
        return result

    def get_index(self) -> Dict[str, Any]:
        """Return discovery result with all collections and environments."""
        return self.discover_all()
