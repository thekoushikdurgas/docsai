"""
TkdJob API Client - HTTP client for lambda/tkdjob Job Scheduler REST endpoints.

Uses X-API-Key authentication. When JOB_SCHEDULER_API_URL and JOB_SCHEDULER_API_KEY
are configured, admin jobs page fetches from the Job Scheduler API.
"""
import logging
from typing import Any, Dict, List, Optional

import httpx
from django.conf import settings

from apps.core.exceptions import LambdaAPIError

logger = logging.getLogger(__name__)


class TkdJobClient:
    """Client for lambda/tkdjob Job Scheduler REST endpoints."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: Optional[int] = None,
    ):
        self.base_url = (
            base_url or getattr(settings, "JOB_SCHEDULER_API_URL", "") or ""
        ).rstrip("/")
        self.api_key = api_key or getattr(settings, "JOB_SCHEDULER_API_KEY", "") or ""
        self.timeout = timeout or getattr(settings, "JOB_SCHEDULER_API_TIMEOUT", 30)

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-API-Key": self.api_key,
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
                raise LambdaAPIError(
                    str(e),
                    endpoint=path,
                ) from e

    def _normalize_job(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize job item for templates (snake_case, consistent keys)."""
        return {
            "uuid": job.get("uuid", ""),
            "job_title": job.get("job_title", ""),
            "job_type": job.get("job_type", ""),
            "degree": job.get("degree", 0),
            "status": job.get("status", ""),
            "data": job.get("data") or {},
            "job_response": job.get("job_response") or {},
            "try_count": job.get("try_count", 0),
            "retry_interval": job.get("retry_interval", 0),
            "run_after": job.get("run_after"),
            "created_at": job.get("created_at"),
            "updated_at": job.get("updated_at"),
        }

    def list_jobs(
        self,
        status: Optional[List[str]] = None,
        uuid: Optional[str] = None,
        limit: int = 25,
        offset: int = 0,
    ) -> Dict[str, Any]:
        """List jobs with optional filters.

        Args:
            status: Optional list of status values to filter
            uuid: Optional single UUID filter
            limit: Max results (1-100)
            offset: Offset for pagination

        Returns:
            Dict with jobs (list of normalized job dicts) and total from response
        """
        params: Dict[str, Any] = {"limit": min(max(limit, 1), 100), "offset": offset}
        if status:
            params["status"] = status
        if uuid:
            params["uuid"] = uuid

        data = self._request("GET", "/api/v1/jobs/", params=params)
        raw_list = data.get("data") or []
        jobs = [self._normalize_job(j) for j in raw_list]
        return {"jobs": jobs, "total": len(jobs)}

    def get_job(self, job_uuid: str) -> Dict[str, Any]:
        """Get a single job by UUID."""
        data = self._request("GET", f"/api/v1/jobs/{job_uuid}")
        return self._normalize_job(data.get("data") or {})

    def get_job_status(self, job_uuid: str) -> Dict[str, Any]:
        """Get job status and progress."""
        data = self._request("GET", f"/api/v1/jobs/{job_uuid}/status")
        return data.get("data") or {}

    def get_job_timeline(self, job_uuid: str) -> Dict[str, Any]:
        """Get job lifecycle events."""
        data = self._request("GET", f"/api/v1/jobs/{job_uuid}/timeline")
        return {
            "job_uuid": data.get("job_uuid", job_uuid),
            "timeline": data.get("timeline") or [],
        }

    def get_job_dag(
        self, job_uuid: str, include_status: bool = True
    ) -> Dict[str, Any]:
        """Get DAG structure from this job."""
        data = self._request(
            "GET",
            f"/api/v1/jobs/{job_uuid}/dag",
            params={"include_status": str(include_status).lower()},
        )
        return data.get("dag") or {"root_uuid": job_uuid, "nodes": [], "edges": []}

    def retry_job(
        self,
        job_uuid: str,
        data: Optional[Dict[str, Any]] = None,
        priority: Optional[int] = None,
        retry_count: Optional[int] = None,
        retry_interval: Optional[int] = None,
        run_after: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retry a failed job.

        Args:
            job_uuid: Job UUID
            data: Optional updated job data
            priority: Optional priority
            retry_count: Optional retry count
            retry_interval: Optional retry interval (minutes)
            run_after: Optional ISO datetime for run_after

        Returns:
            Normalized job dict from response
        """
        body: Dict[str, Any] = {}
        if data is not None:
            body["data"] = data
        if priority is not None:
            body["priority"] = priority
        if retry_count is not None:
            body["retry_count"] = retry_count
        if retry_interval is not None:
            body["retry_interval"] = retry_interval
        if run_after is not None:
            body["run_after"] = run_after

        resp = self._request(
            "PUT",
            f"/api/v1/jobs/{job_uuid}/retry",
            json_data=body,
        )
        raw = resp.get("data") or {}
        return self._normalize_job(raw)
