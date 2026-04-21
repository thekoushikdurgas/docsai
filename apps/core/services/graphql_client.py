"""
Shared GraphQL client for all admin service calls.

Transport for ``POST /graphql`` on the Contact360 API gateway: retries, backoff,
``X-Request-ID``, Bearer token. See ``docs/backend/endpoints/contact360.io/ADMIN-MODULE.md``.

``GraphQLClient`` is the OO wrapper used by documentation services; module-level
``graphql_query`` / ``graphql_mutation`` remain for admin_ops and core views.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional

import httpx
from django.conf import settings
from django.core.cache import cache

if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


class GraphQLError(RuntimeError):
    """GraphQL returned errors in the response body or transport failed after retries."""


_CACHE_GEN_KEY = "graphql_client_cache_gen"
_DEFAULT_QUERY_CACHE_TTL = 300


class GraphQLClient:
    """
    Gateway GraphQL client with optional Django-cache for read queries.

    Token resolution: explicit ``access_token``, else ``request.session['operator']['token']``,
    else ``GRAPHQL_INTERNAL_TOKEN`` via ``graphql_query`` (server-to-server).
    """

    def __init__(
        self,
        endpoint_url: str | None = None,
        access_token: str | None = None,
        request: HttpRequest | None = None,
    ) -> None:
        raw = (endpoint_url or getattr(settings, "GRAPHQL_URL", "") or "").strip()
        self.endpoint_url = raw or "http://localhost:8001/graphql"
        self._access_token = access_token
        self.request = request

    @property
    def access_token(self) -> str | None:
        """Resolved Bearer for logging; may differ from internal token used on wire."""
        return self._resolve_token()

    def _resolve_token(self) -> str | None:
        if self._access_token:
            return self._access_token
        if self.request is not None:
            op = self.request.session.get("operator") or {}
            tok = op.get("token")
            if tok:
                return str(tok)
        return None

    def clear_cache(self) -> None:
        """Invalidate query cache entries for this client (generation bump)."""
        try:
            gen = cache.get(_CACHE_GEN_KEY) or 0
            cache.set(_CACHE_GEN_KEY, int(gen) + 1, timeout=None)
        except Exception as exc:
            logger.warning("GraphQLClient.clear_cache failed: %s", exc)

    def _cache_key(self, document: str, variables: Optional[Dict[str, Any]]) -> str:
        gen = cache.get(_CACHE_GEN_KEY) or 0
        payload = json.dumps(
            {"q": document, "v": variables or {}, "g": gen},
            sort_keys=True,
            default=str,
        )
        h = hashlib.sha256(payload.encode()).hexdigest()[:48]
        return f"graphql_client:{h}"

    def execute_query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        *,
        use_cache: bool = False,
        cache_timeout: int = _DEFAULT_QUERY_CACHE_TTL,
    ) -> Dict[str, Any]:
        """
        Run a GraphQL query; returns the ``data`` object (not the full HTTP body).

        Raises:
            GraphQLError: On GraphQL errors array or missing data after errors.
        """
        if use_cache:
            ck = self._cache_key(query, variables)
            try:
                hit = cache.get(ck)
                if hit is not None:
                    return hit
            except Exception as exc:
                logger.warning("GraphQL cache get failed: %s", exc)

        token = self._resolve_token()
        body = graphql_query(
            query, variables, token=token, graphql_url=self.endpoint_url
        )
        data = self._unwrap_data(body)

        if use_cache and data is not None:
            try:
                cache.set(ck, data, timeout=cache_timeout)
            except Exception as exc:
                logger.warning("GraphQL cache set failed: %s", exc)
        return data

    def execute_mutation(
        self,
        mutation: str,
        variables: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        token = self._resolve_token()
        body = graphql_mutation(
            mutation, variables, token=token, graphql_url=self.endpoint_url
        )
        return self._unwrap_data(body)

    @staticmethod
    def _unwrap_data(body: Dict[str, Any]) -> Dict[str, Any]:
        errs = body.get("errors")
        if errs:
            msg = errs[0].get("message", str(errs[0])) if errs else "GraphQL error"
            raise GraphQLError(msg)
        data = body.get("data")
        if data is None:
            raise GraphQLError("GraphQL response missing data")
        return data


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
    graphql_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute a GraphQL query against the Contact360 API gateway.
    Returns the parsed JSON response dict.
    Raises RuntimeError on non-2xx responses or network errors after retries.
    """
    return _execute(
        query, variables, token, request_id, timeout, max_retries, graphql_url
    )


def graphql_mutation(
    mutation: str,
    variables: Optional[Dict[str, Any]] = None,
    token: Optional[str] = None,
    request_id: Optional[str] = None,
    timeout: float = _DEFAULT_TIMEOUT,
    max_retries: int = _MAX_RETRIES,
    graphql_url: Optional[str] = None,
) -> Dict[str, Any]:
    return _execute(
        mutation, variables, token, request_id, timeout, max_retries, graphql_url
    )


def _execute(
    document: str,
    variables: Optional[Dict[str, Any]],
    token: Optional[str],
    request_id: Optional[str],
    timeout: float,
    max_retries: int = _MAX_RETRIES,
    graphql_url: Optional[str] = None,
) -> Dict[str, Any]:
    url = graphql_url or settings.GRAPHQL_URL
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
                raise RuntimeError(
                    f"GraphQL gateway {resp.status_code}: {resp.text[:200]}"
                )
            resp.raise_for_status()
            try:
                data = resp.json()
            except ValueError as je:
                raise RuntimeError(
                    f"GraphQL response is not JSON: {resp.text[:200]}"
                ) from je
            return data
        except (httpx.RequestError, httpx.HTTPStatusError, RuntimeError) as exc:
            last_exc = exc
            if attempt + 1 >= attempts:
                break
            wait = _BACKOFF_BASE**attempt
            logger.warning(
                "GraphQL attempt %d failed (%s); retrying in %.1fs",
                attempt + 1,
                exc,
                wait,
            )
            time.sleep(wait)

    raise RuntimeError(f"GraphQL request failed after {attempts} attempts: {last_exc}")
