"""Execute API — stub until Durgasman storage/engine is wired."""

import json
import logging

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.core.decorators import require_super_admin

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
@require_super_admin
def execute_request(request):
    try:
        body = json.loads(request.body) if request.body else {}
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)
    return JsonResponse(
        {
            "success": True,
            "stub": True,
            "echo": body,
            "message": "Durgasman execute API not wired to a runner in this build.",
        }
    )
