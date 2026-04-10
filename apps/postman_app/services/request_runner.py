"""Postman request runner — proxies HTTP requests from the admin backend.

Uses httpx (already available in the admin virtualenv).
"""

import re
import time
import logging
from typing import Any, Dict, Optional

import httpx

logger = logging.getLogger(__name__)

# Maximum response body to buffer (5 MiB)
MAX_RESPONSE_BYTES = 5 * 1024 * 1024


def _substitute_vars(text: str, variables: Dict[str, str]) -> str:
    """Replace ``{{varName}}`` placeholders with environment variable values."""
    if not variables or not text:
        return text

    def _replacer(match):
        key = match.group(1).strip()
        return variables.get(key, match.group(0))

    return re.sub(r"\{\{([^}]+)\}\}", _replacer, text)


def _apply_vars_to_headers(
    headers: Dict[str, str], variables: Dict[str, str]
) -> Dict[str, str]:
    return {k: _substitute_vars(v, variables) for k, v in headers.items()}


def run_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    body: Optional[str] = None,
    body_type: str = "raw",
    form_data: Optional[Dict[str, str]] = None,
    query_params: Optional[Dict[str, str]] = None,
    timeout: int = 30,
    variables: Optional[Dict[str, str]] = None,
    follow_redirects: bool = True,
) -> Dict[str, Any]:
    """Execute an HTTP request and return a structured result dict.

    Returns:
        {
            "status": int,
            "status_text": str,
            "elapsed_ms": int,
            "size_bytes": int,
            "headers": dict,
            "body": str,
            "body_truncated": bool,
            "error": str | None,
        }
    """
    vars_ = variables or {}

    # Substitute variables
    url = _substitute_vars(url, vars_)
    headers = _apply_vars_to_headers(headers or {}, vars_)
    if body:
        body = _substitute_vars(body, vars_)

    method = method.upper()

    try:
        start = time.monotonic()
        with httpx.Client(
            timeout=httpx.Timeout(float(timeout)),
            follow_redirects=follow_redirects,
        ) as client:
            if body_type == "form" and form_data:
                resp = client.request(
                    method, url, headers=headers, data=form_data, params=query_params
                )
            elif body_type == "raw" and body:
                resp = client.request(
                    method,
                    url,
                    headers=headers,
                    content=body.encode("utf-8"),
                    params=query_params,
                )
            else:
                resp = client.request(method, url, headers=headers, params=query_params)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        raw_bytes = resp.content
        truncated = len(raw_bytes) > MAX_RESPONSE_BYTES
        body_bytes = raw_bytes[:MAX_RESPONSE_BYTES]

        # Decode body as text
        charset = resp.encoding or "utf-8"
        try:
            body_text = body_bytes.decode(charset, errors="replace")
        except Exception:
            body_text = body_bytes.decode("utf-8", errors="replace")

        resp_headers = dict(resp.headers)

        return {
            "status": resp.status_code,
            "status_text": _status_text(resp.status_code),
            "elapsed_ms": elapsed_ms,
            "size_bytes": len(raw_bytes),
            "headers": resp_headers,
            "body": body_text,
            "body_truncated": truncated,
            "error": None,
        }

    except httpx.TimeoutException:
        return _error_result(f"Request timed out after {timeout}s")
    except httpx.ConnectError as exc:
        return _error_result(f"Connection error: {exc}")
    except httpx.RequestError as exc:
        return _error_result(f"Request error: {exc}")
    except Exception as exc:
        logger.exception("postman request_runner unexpected error")
        return _error_result(f"Unexpected error: {exc}")


def _error_result(message: str) -> Dict[str, Any]:
    return {
        "status": 0,
        "status_text": "Error",
        "elapsed_ms": 0,
        "size_bytes": 0,
        "headers": {},
        "body": "",
        "body_truncated": False,
        "error": message,
    }


def _status_text(code: int) -> str:
    _map = {
        100: "Continue",
        101: "Switching Protocols",
        200: "OK",
        201: "Created",
        202: "Accepted",
        204: "No Content",
        301: "Moved Permanently",
        302: "Found",
        304: "Not Modified",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        409: "Conflict",
        422: "Unprocessable Entity",
        429: "Too Many Requests",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
    }
    return _map.get(code, "Unknown")
