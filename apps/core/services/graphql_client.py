"""
Shared GraphQL client for all admin service calls.
Handles retry, exponential backoff, request ID propagation, and token injection.
"""
import logging
import uuid
import time
from typing import Any, Dict, Optional

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 30.0
_MAX_RETRIES = 3
_BACKOFF_BASE = 1.5


def _make_request_id() -> str:
    return str(uuid.uuid4())


def graphql_query(
    query: str,
    variables: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None,
    request_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
    max_retries: int = _MAX_RETRIES,
) -> Dict[str, Any]:
    """
    Execute a GraphQL query against the Contact360 API gateway.
    Returns the parsed JSON response dict.
    Raises RuntimeError on non-2xx responses or network errors after retries.
    """
    return _execute(query, variables, token, request_id, timeout, max_retries)


def graphql_mutation(
    mutation: str,
    variables: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None,
    request_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
    max_retries: int = _MAX_RETRIES,
) -> Dict[str, Any]:
    return _execute(mutation, variables, token, request_id, timeout, max_retries)


def _execute(
    document: str,
    variables: Optional[Dict[str, Any]],
    token: Optional[str],
    request_id: Optional[str],
    timeout: float,
    max_retries: int = _MAX_RETRIES,
) -> Dict[str, Any]:
    url = settings.GRAPHQL_URL
    rid = request_id or _make_request_id()

    headers = {
        "Content-Type": "application/json",
        "X-Request-ID": rid,
        "X-Service": "docsai-admin",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    elif settings.GRAPHQL_INTERNAL_TOKEN:
        headers["Authorization"] = f"Bearer {settings.GRAPHQL_INTERNAL_TOKEN}"

    payload: Dict[str, Any] = {"query": document}
    if variables:
        payload["variables"] = variables

    last_exc: Optional[Exception] = None
    attempts = max(1, min(max_retries, 10))
    for attempt in range(attempts):
        try:
            with httpx.Client(timeout=timeout) as client:
                resp = client.post(url, json=payload, headers=headers)
            if resp.status_code >= 500:
                raise RuntimeError(f"GraphQL gateway {resp.status_code}: {resp.text[:200]}")
            resp.raise_for_status()
            try:
                data = resp.json()
            except ValueError as je:
                raise RuntimeError(f"GraphQL response is not JSON: {resp.text[:200]}") from je
            return data
        except (httpx.RequestError, httpx.HTTPStatusError, RuntimeError) as exc:
            last_exc = exc
            if attempt + 1 >= attempts:
                break
            wait = _BACKOFF_BASE ** attempt
            logger.warning("GraphQL attempt %d failed (%s); retrying in %.1fs", attempt + 1, exc, wait)
            time.sleep(wait)

    raise RuntimeError(f"GraphQL request failed after {attempts} attempts: {last_exc}")
