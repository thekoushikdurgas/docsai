import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.core.decorators import require_login
from .services.ai_client import send_message, get_sessions


@require_login
def chat_view(request):
    sessions = []
    try:
        sessions = get_sessions(request.session.get("operator", {}).get("token", ""))
    except Exception:
        pass
    return render(
        request, "ai/chat.html", {"sessions": sessions, "page_title": "AI Chat"}
    )


@require_login
def sessions_view(request):
    sessions = []
    try:
        sessions = get_sessions(request.session.get("operator", {}).get("token", ""))
    except Exception:
        pass
    return render(
        request, "ai/sessions.html", {"sessions": sessions, "page_title": "AI Sessions"}
    )


@require_login
def session_detail_view(request, session_id):
    return render(
        request,
        "ai/chat.html",
        {"session_id": session_id, "page_title": f"Session {session_id[:8]}"},
    )


@require_login
@require_http_methods(["POST"])
def api_chat_view(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    session_id = body.get("session_id", "")
    content = body.get("content", "").strip()
    if not content:
        return JsonResponse({"error": "content is required"}, status=400)
    token = request.session.get("operator", {}).get("token", "")
    result = send_message(session_id, content, token)
    return JsonResponse(result)
