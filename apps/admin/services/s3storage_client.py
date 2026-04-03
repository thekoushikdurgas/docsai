"""
S3Storage API Client - HTTP client for lambda/s3storage REST endpoints.

Uses X-API-Key authentication. When S3STORAGE_API_URL and S3STORAGE_API_KEY are
configured, admin storage files page fetches from the s3storage API.
"""
import logging
import uuid
from typing import Any, Dict, List, Optional

import httpx
from django.conf import settings

from apps.core.exceptions import LambdaAPIError

logger = logging.getLogger(__name__)


class S3StorageClient:
    """Client for lambda/s3storage REST endpoints."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        request_id: Optional[str] = None,
    ):
        self.base_url = (
            base_url or getattr(settings, "S3STORAGE_API_URL", "") or ""
        ).rstrip("/")
        self.api_key = api_key or getattr(settings, "S3STORAGE_API_KEY", "") or ""
        self.timeout = timeout or getattr(settings, "S3STORAGE_API_TIMEOUT", 30)
        self.request_id = request_id or str(uuid.uuid4())

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        headers["X-Request-ID"] = self.request_id
        return headers

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        with httpx.Client(timeout=self.timeout) as client:
            try:
                resp = client.request(
                    method=method,
                    url=url,
                    headers=self._headers(),
                    params=params,
                    json=json_data,
                )
                resp.raise_for_status()
                data = resp.json() if resp.content else {}
                if isinstance(data, dict):
                    return data
                raise LambdaAPIError(
                    "Invalid response format",
                    endpoint=path,
                    status_code=resp.status_code,
                )
            except httpx.HTTPStatusError as e:
                detail = "Unknown error"
                try:
                    err_body = e.response.json()
                    if isinstance(err_body, dict) and "detail" in err_body:
                        detail = (
                            err_body["detail"]
                            if isinstance(err_body["detail"], str)
                            else str(err_body["detail"])
                        )
                except Exception:
                    detail = e.response.text or str(e)
                raise LambdaAPIError(
                    detail,
                    endpoint=path,
                    status_code=e.response.status_code,
                ) from e
            except httpx.RequestError as e:
                raise LambdaAPIError(
                    str(e),
                    endpoint=path,
                ) from e

    def list_objects(
        self,
        bucket_id: str,
        prefix: str = "",
    ) -> List[Dict[str, Any]]:
        """List CSV/files in a logical bucket.

        Args:
            bucket_id: Logical bucket ID
            prefix: Optional key prefix filter

        Returns:
            List of file dicts (key, filename, size, last_modified, content_type)
        """
        params: Dict[str, Any] = {}
        if prefix:
            params["prefix"] = prefix
        data = self._request(
            "GET",
            f"/api/v1/buckets/{bucket_id}/objects",
            params=params if params else None,
        )
        return data.get("files") or []

    def get_download_url(
        self,
        bucket_id: str,
        file_key: str,
        expires_in: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Get presigned download URL for a file.

        Returns:
            Dict with downloadUrl and expiresIn
        """
        params: Dict[str, Any] = {"file_key": file_key}
        if expires_in is not None:
            params["expires_in"] = expires_in
        data = self._request(
            "GET",
            f"/api/v1/buckets/{bucket_id}/objects/download-url",
            params=params,
        )
        return {
            "downloadUrl": data.get("downloadUrl", ""),
            "expiresIn": data.get("expiresIn", 0),
        }

    def get_object_info(self, bucket_id: str, file_key: str) -> Dict[str, Any]:
        """Get metadata for a single file."""
        return self._request(
            "GET",
            f"/api/v1/buckets/{bucket_id}/objects/info",
            params={"file_key": file_key},
        )

    def delete_object(self, bucket_id: str, file_key: str) -> Dict[str, Any]:
        """Delete a file from a logical bucket."""
        return self._request(
            "DELETE",
            f"/api/v1/buckets/{bucket_id}/objects",
            params={"file_key": file_key},
        )

    def upload_photo(
        self,
        bucket_id: str,
        file,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload an image to the photo/ folder via s3storage.

        Args:
            bucket_id: Logical bucket ID
            file: File-like object (e.g. Django UploadedFile)
            filename: Optional filename override (defaults to file.name)

        Returns:
            Dict with fileKey, status
        """
        if not self.base_url:
            raise LambdaAPIError(
                "S3Storage is not configured (S3STORAGE_API_URL)",
                endpoint="/api/v1/uploads/photo",
                status_code=503,
            )
        name = filename or getattr(file, "name", "qr.png")
        content_type = getattr(file, "content_type", None) or "image/png"
        url = f"{self.base_url}/api/v1/uploads/photo"
        params = {"bucket_id": bucket_id}
        with httpx.Client(timeout=self.timeout) as client:
            try:
                resp = client.post(
                    url,
                    headers={"X-Request-ID": self.request_id, **({"X-API-Key": self.api_key} if self.api_key else {})},
                    params=params,
                    files={"file": (name, file, content_type)},
                )
                resp.raise_for_status()
                data = resp.json() if resp.content else {}
                if isinstance(data, dict):
                    return data
                raise LambdaAPIError(
                    "Invalid response format",
                    endpoint="/api/v1/uploads/photo",
                    status_code=resp.status_code,
                )
            except httpx.HTTPStatusError as e:
                detail = "Unknown error"
                try:
                    err_body = e.response.json()
                    if isinstance(err_body, dict) and "detail" in err_body:
                        detail = (
                            err_body["detail"]
                            if isinstance(err_body["detail"], str)
                            else str(err_body["detail"])
                        )
                except Exception:
                    detail = e.response.text or str(e)
                raise LambdaAPIError(
                    detail,
                    endpoint="/api/v1/uploads/photo",
                    status_code=e.response.status_code,
                ) from e
            except httpx.RequestError as e:
                raise LambdaAPIError(
                    str(e),
                    endpoint="/api/v1/uploads/photo",
                    status_code=503,
                ) from e
