"""Media Sync – upload media JSON to S3 (and optionally sync from S3/Lambda)."""

import json
import logging
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from apps.documentation.services.media_file_manager import MediaFileManagerService
from apps.documentation.utils.paths import get_media_root

logger = logging.getLogger(__name__)


class MediaSyncService:
    """Sync local media/ JSON to S3. Sync-from-Lambda optional when API supports it."""

    def __init__(self) -> None:
        self.file_manager = MediaFileManagerService()
        self.media_root = get_media_root()

    def sync_file_to_s3(self, file_path: str) -> Dict[str, Any]:
        """
        Upload a single file to S3. Uses file_manager for path -> S3 key.
        Returns {success, s3_key, error}.
        """
        p = Path(file_path)
        if not p.exists() or not p.is_file():
            return {"success": False, "s3_key": None, "error": "File not found"}
        try:
            resource_type = self.file_manager._infer_resource_type(p)
            s3_key = self.file_manager.calculate_s3_key(p, resource_type)
        except Exception as e:
            return {"success": False, "s3_key": None, "error": str(e)}

        try:
            with open(p, "rb") as f:
                content = f.read()
        except OSError as e:
            return {"success": False, "s3_key": s3_key, "error": str(e)}

        try:
            from apps.core.services.s3_service import S3Service
            svc = S3Service()
            svc.upload_file(content, s3_key, content_type="application/json")
            return {"success": True, "s3_key": s3_key, "error": None}
        except Exception as e:
            logger.warning("sync_file_to_s3 failed path=%s key=%s: %s", file_path, s3_key, e)
            return {"success": False, "s3_key": s3_key, "error": str(e)}

    def _sync_resource_type(
        self,
        resource_type: str,
        dry_run: bool,
        progress_callback: Optional[Callable[[int, int, str, int, int, str], None]] = None,
        global_start_index: int = 0,
        global_total: int = 0,
    ) -> Dict[str, Any]:
        """Scan resource type, upload each JSON to S3. Returns {resource_type, total_files, synced, errors, success_files, error_details}.
        progress_callback(global_index, global_total, section, section_index, section_total, current_file) called per file."""
        result: Dict[str, Any] = {
            "resource_type": resource_type,
            "total_files": 0,
            "synced": 0,
            "created": 0,
            "updated": 0,
            "errors": 0,
            "error_details": [],
            "success_files": [],
        }
        files = self.file_manager.scan_media_directory(resource_type)
        result["total_files"] = len(files)
        if dry_run:
            result["synced"] = len(files)
            return result

        for idx, fi in enumerate(files):
            fp = fi.get("file_path")
            rel_path = (fi.get("relative_path") or fi.get("name") or str(fp)).replace("\\", "/")
            if not fp:
                continue
            if progress_callback and global_total > 0:
                try:
                    progress_callback(
                        global_start_index + idx,
                        global_total,
                        resource_type,
                        idx + 1,
                        len(files),
                        rel_path,
                    )
                except Exception:
                    pass
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    data = json.load(f)
                out = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
                rt = fi.get("resource_type", resource_type)
                s3_key = self.file_manager.calculate_s3_key(Path(fp), rt)
                from apps.core.services.s3_service import S3Service
                svc = S3Service()
                svc.upload_file(out, s3_key, content_type="application/json")
                result["synced"] += 1
                result["updated"] += 1
                result["success_files"].append({"file": rel_path, "s3_key": s3_key})
            except Exception as e:
                result["errors"] += 1
                result["error_details"].append({"file": rel_path, "error": str(e)})

        return result

    def sync_pages_to_s3(self, dry_run: bool = False, **kwargs: Any) -> Dict[str, Any]:
        return self._sync_resource_type("pages", dry_run, **kwargs)

    def sync_endpoints_to_s3(self, dry_run: bool = False, **kwargs: Any) -> Dict[str, Any]:
        return self._sync_resource_type("endpoints", dry_run, **kwargs)

    def sync_relationships_to_s3(self, dry_run: bool = False, **kwargs: Any) -> Dict[str, Any]:
        return self._sync_resource_type("relationships", dry_run, **kwargs)

    def sync_postman_to_s3(self, dry_run: bool = False, **kwargs: Any) -> Dict[str, Any]:
        return self._sync_resource_type("postman", dry_run, **kwargs)

    def sync_n8n_to_s3(self, dry_run: bool = False, **kwargs: Any) -> Dict[str, Any]:
        return self._sync_resource_type("n8n", dry_run, **kwargs)

    def sync_result_to_s3(self, dry_run: bool = False, **kwargs: Any) -> Dict[str, Any]:
        return self._sync_resource_type("result", dry_run, **kwargs)

    def sync_project_to_s3(self, dry_run: bool = False, **kwargs: Any) -> Dict[str, Any]:
        return self._sync_resource_type("project", dry_run, **kwargs)

    def sync_media_to_s3(self, dry_run: bool = False, **kwargs: Any) -> Dict[str, Any]:
        return self._sync_resource_type("media", dry_run, **kwargs)

    def sync_all_to_s3(self, dry_run: bool = False) -> Dict[str, Any]:
        out: Dict[str, Any] = {}
        for rt in ("pages", "endpoints", "relationships", "postman", "n8n", "result", "project", "media"):
            out[rt] = self._sync_resource_type(rt, dry_run)
        return out
