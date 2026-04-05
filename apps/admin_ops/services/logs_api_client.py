"""Logs API Client — Lambda logs.api REST (same contract as contact360.io/2)."""
import logging
import uuid
from typing import Any, Dict, Optional

import httpx
from django.conf import settings

from apps.core.exceptions import LambdaAPIError

logger = logging.getLogger(__name__)


class LogsApiClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
        request_id: Optional[str] = None,
    ):
        self.base_url = (base_url or getattr(settings, "LOGS_API_URL", "") or "").rstrip("/")
        self.api_key = api_key or getattr(settings, "LOGS_API_KEY", "") or ""
        self.timeout = timeout or getattr(settings, "LOGS_API_TIMEOUT", 30)
        self.request_id = request_id or str(uuid.uuid4())

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-Key": self.api_key,
            "X-Request-ID": self.request_id,
        }

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
                data = resp.json()
                if not isinstance(data, dict):
                    raise LambdaAPIError(
                        "Invalid response format",
                        endpoint=path,
                        status_code=resp.status_code,
                    )
                if not data.get("success", True):
                    raise LambdaAPIError(
                        data.get("detail", "Request failed"),
                        endpoint=path,
                        status_code=resp.status_code,
                    )
                return data
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

    def update_log(
        self,
        log_id: str,
        message: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if message is not None:
            body["message"] = message
        if context is not None:
            body["context"] = context
        data = self._request("PUT", f"/logs/{log_id}", json_data=body if body else {})
        d = data.get("data") or {}
        return {
            "id": d.get("id", ""),
            "timestamp": d.get("timestamp"),
            "level": d.get("level", ""),
            "logger": d.get("logger", ""),
            "message": d.get("message", ""),
            "context": d.get("context"),
            "user_id": d.get("user_id"),
            "request_id": d.get("request_id"),
        }

    def delete_logs_bulk(
        self,
        level: Optional[str] = None,
        logger: Optional[str] = None,
        user_id: Optional[str] = None,
        request_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> Dict[str, Any]:
        body: Dict[str, Any] = {}
        if level:
            body["level"] = level
        if logger:
            body["logger"] = logger
        if user_id:
            body["user_id"] = user_id
        if request_id:
            body["request_id"] = request_id
        if start_time:
            body["start_time"] = start_time
        if end_time:
            body["end_time"] = end_time
        data = self._request("POST", "/logs/delete", json_data=body)
        d = data.get("data") or {}
        return {
            "deleted_count": d.get("deleted_count"),
            "status": data.get("status"),
            "message": data.get("message"),
        }
