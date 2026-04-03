"""Propagate a single request correlation id on every response (Era 0.x / 6.x ops baseline)."""

from __future__ import annotations

import uuid
from typing import Callable

REQUEST_ID_ATTR = "c360_request_id"


class RequestIdMiddleware:
    """Ensure inbound X-Request-ID is echoed; synthesize one if missing."""

    def __init__(self, get_response: Callable):
        self.get_response = get_response

    def __call__(self, request):
        rid = request.META.get("HTTP_X_REQUEST_ID") or request.META.get(
            "HTTP_X_CORRELATION_ID"
        )
        if not rid:
            rid = str(uuid.uuid4())
        setattr(request, REQUEST_ID_ATTR, rid)
        response = self.get_response(request)
        response["X-Request-ID"] = rid
        return response
