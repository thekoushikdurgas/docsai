"""
AI chat UI — ``aiChats.*`` via ``ai_client``; streaming proxies gateway
``POST /api/v1/ai-chats/{id}/message/stream`` (see ``contact360.io/api``).
"""

import json

import httpx
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from apps.core.decorators import require_login

from .services.ai_client import get_sessions, send_message


def _gateway_base_url() -> str:
    url = (getattr(settings, "GRAPHQL_URL", "") or "").strip()
    if "/graphql" in url:
        return url.rsplit("/graphql", 1)[0].rstrip("/")
    return url.rstrip("/")


@require_login
def chat_view(request):
    """AI chat UI; lists ``aiChats`` sessions. @role: authenticated"""
    sessions = []
    try:
        sessions = get_sessions(request.session.get("operator", {}).get("token", ""))
    except Exception:
        pass
    return render(
        request,
        "ai/chat.html",
        {
            "sessions": sessions,
            "page_title": "AI Chat",
            "stream_path": "/ai/api/chat/stream/",
        },
    )


@require_login
def sessions_view(request):
    """Session list from gateway ``aiChats`` list. @role: authenticated"""
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
    """Open one chat session in the main chat template. @role: authenticated"""
    return render(
        request,
        "ai/chat.html",
        {
            "session_id": session_id,
            "page_title": f"Session {session_id[:8]}",
            "stream_path": "/ai/api/chat/stream/",
        },
    )


@require_login
@require_http_methods(["POST"])
def api_chat_view(request):
    """XHR: ``aiChats.sendMessage`` (non-streaming). @role: authenticated"""
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


@require_login
@require_http_methods(["POST"])
def api_chat_stream_view(request):
    """
    Proxy SSE stream to gateway Contact AI (operator Bearer token).

    @role: authenticated
    """
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)
    session_id = (body.get("session_id") or "").strip()
    content = (body.get("content") or "").strip()
    if not session_id or not content:
        return JsonResponse(
            {"error": "session_id and content are required for streaming"}, status=400
        )
    token = request.session.get("operator", {}).get("token", "")
    base = _gateway_base_url()
    url = f"{base}/api/v1/ai-chats/{session_id}/message/stream"

    def byte_stream():
        try:
            with httpx.Client(timeout=httpx.Timeout(300.0)) as client:
                with client.stream(
                    "POST",
                    url,
                    json={"message": content},
                    headers={"Authorization": f"Bearer {token}"},
                ) as resp:
                    yield from resp.iter_bytes()
        except Exception as exc:
            err = json.dumps({"error": str(exc)})
            yield f"data: {err}\n\n".encode("utf-8")
            yield b"data: [DONE]\n\n"

    return StreamingHttpResponse(
        byte_stream(),
        content_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
