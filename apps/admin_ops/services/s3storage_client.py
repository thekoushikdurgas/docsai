"""S3Storage API client (photo upload, bucket objects) — same as contact360.io/2."""

import logging
import uuid
from typing import Any, Dict, Optional

import httpx
from django.conf import settings

from apps.core.exceptions import LambdaAPIError

logger = logging.getLogger(__name__)


class S3StorageClient:
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

    def _api_v1_base(self) -> str:
        """Base URL including ``/api/v1`` once (env may already end with ``/api/v1``)."""
        b = self.base_url
        if not b:
            return ""
        b = b.rstrip("/")
        if b.endswith("/api/v1"):
            return b
        return f"{b}/api/v1"

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
                raise LambdaAPIError(str(e), endpoint=path) from e

    def upload_photo(
        self,
        bucket_id: str,
        file,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not self.base_url:
            raise LambdaAPIError(
                "S3Storage is not configured (S3STORAGE_API_URL)",
                endpoint="/api/v1/uploads/photo",
                status_code=503,
            )
        name = filename or getattr(file, "name", "qr.png")
        content_type = getattr(file, "content_type", None) or "image/png"
        url = f"{self._api_v1_base()}/uploads/photo"
        params = {"bucket_id": bucket_id}
        with httpx.Client(timeout=self.timeout) as client:
            try:
                resp = client.post(
                    url,
                    headers={
                        "X-Request-ID": self.request_id,
                        **({"X-API-Key": self.api_key} if self.api_key else {}),
                    },
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
                    if isinstance(err_body, dict):
                        raw = err_body.get("detail")
                        if raw is None:
                            raw = err_body.get("error")
                        if raw is not None:
                            detail = raw if isinstance(raw, str) else str(raw)
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

    def upload_json(
        self,
        bucket_id: str,
        file,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Upload a JSON document (Postman collection / environment / generic) to S3.

        Returns dict with ``fileKey`` (relative, e.g. ``json/<uuid>.json``) and ``bucketId``.
        """
        if not self.base_url:
            raise LambdaAPIError(
                "S3Storage is not configured (S3STORAGE_API_URL)",
                endpoint="/api/v1/uploads/json",
                status_code=503,
            )
        name = filename or getattr(file, "name", "document.json")
        url = f"{self._api_v1_base()}/uploads/json"
        params = {"bucket_id": bucket_id}
        with httpx.Client(timeout=self.timeout) as client:
            try:
                resp = client.post(
                    url,
                    headers={
                        "X-Request-ID": self.request_id,
                        **({"X-API-Key": self.api_key} if self.api_key else {}),
                    },
                    params=params,
                    files={"file": (name, file, "application/json")},
                )
                resp.raise_for_status()
                data = resp.json() if resp.content else {}
                if isinstance(data, dict):
                    return data
                raise LambdaAPIError(
                    "Invalid response format",
                    endpoint="/api/v1/uploads/json",
                    status_code=resp.status_code,
                )
            except httpx.HTTPStatusError as e:
                detail = "Unknown error"
                try:
                    err_body = e.response.json()
                    if isinstance(err_body, dict):
                        raw = err_body.get("detail") or err_body.get("error")
                        if raw is not None:
                            detail = raw if isinstance(raw, str) else str(raw)
                except Exception:
                    detail = e.response.text or str(e)
                raise LambdaAPIError(
                    detail,
                    endpoint="/api/v1/uploads/json",
                    status_code=e.response.status_code,
                ) from e
            except httpx.RequestError as e:
                raise LambdaAPIError(
                    str(e),
                    endpoint="/api/v1/uploads/json",
                    status_code=503,
                ) from e

    def get_object(self, key: str) -> bytes:
        """Retrieve raw object bytes from S3. ``key`` is the full key (``bucket_id/relative``).

        Returns raw bytes (typically JSON). Raises ``LambdaAPIError`` on failure.
        """
        if not self.base_url:
            raise LambdaAPIError(
                "S3Storage is not configured (S3STORAGE_API_URL)",
                endpoint="/api/v1/objects/get",
                status_code=503,
            )
        url = f"{self._api_v1_base()}/objects/get"
        with httpx.Client(timeout=self.timeout) as client:
            try:
                resp = client.get(
                    url,
                    headers={
                        "X-Request-ID": self.request_id,
                        **({"X-API-Key": self.api_key} if self.api_key else {}),
                    },
                    params={"key": key},
                )
                resp.raise_for_status()
                return resp.content
            except httpx.HTTPStatusError as e:
                detail = "Unknown error"
                try:
                    err_body = e.response.json()
                    if isinstance(err_body, dict):
                        raw = err_body.get("detail") or err_body.get("error")
                        if raw is not None:
                            detail = raw if isinstance(raw, str) else str(raw)
                except Exception:
                    detail = e.response.text or str(e)
                raise LambdaAPIError(
                    detail,
                    endpoint="/api/v1/objects/get",
                    status_code=e.response.status_code,
                ) from e
            except httpx.RequestError as e:
                raise LambdaAPIError(
                    str(e),
                    endpoint="/api/v1/objects/get",
                    status_code=503,
                ) from e
