"""
JSON execute endpoint for Durgasman — same payload contract as ``send_request_view`` (server-side HTTP via httpx).

CSRF-exempt so API clients can POST with Bearer/session; still requires SuperAdmin decorator.
"""

import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.core.decorators import require_super_admin

from ..services.request_runner import run_request

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
@require_super_admin
def execute_request(request):
    try:
        payload = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    method = (payload.get("method") or "GET").upper()
    url = (payload.get("url") or "").strip()
    if not url:
        return JsonResponse({"success": False, "error": "URL is required."}, status=400)

    result = run_request(
        method=method,
        url=url,
        headers=payload.get("headers") or {},
        body=payload.get("body") or "",
        body_type=payload.get("body_type") or "raw",
        form_data=payload.get("form_data") or {},
        query_params=payload.get("query_params") or {},
        timeout=min(int(payload.get("timeout") or 30), 120),
        variables=payload.get("variables") or {},
    )
    out = {"success": result.get("error") is None, "result": result}
    if result.get("error"):
        out["error"] = result["error"]
    return JsonResponse(out)
