"""AI service client."""

import logging
import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


def send_message(session_id: str, content: str, token: str = "") -> dict:
    if not settings.AI_API_URL:
        return {"error": "AI service not configured"}
    try:
        with httpx.Client(timeout=30.0) as c:
            resp = c.post(
                f"{settings.AI_API_URL}/api/v1/chat",
                json={"session_id": session_id, "content": content},
                headers={"Authorization": f"Bearer {token}"} if token else {},
            )
            resp.raise_for_status()
            return resp.json()
    except Exception as exc:
        logger.warning("AI send_message failed: %s", exc)
        return {"error": str(exc)}


def get_sessions(token: str = "") -> list:
    if not settings.AI_API_URL:
        return []
    try:
        with httpx.Client(timeout=10.0) as c:
            resp = c.get(
                f"{settings.AI_API_URL}/api/v1/sessions",
                headers={"Authorization": f"Bearer {token}"} if token else {},
            )
            resp.raise_for_status()
            return resp.json().get("sessions", [])
    except Exception as exc:
        logger.warning("AI get_sessions failed: %s", exc)
        return []
