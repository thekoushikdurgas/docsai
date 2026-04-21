"""AI chat client — gateway ``aiChats.*`` (non-streaming).

Streaming/SSE to the AI server is not wired here; see module docstring on
``apps.ai_agent.views`` (Phase 5: align with product SSE via gateway).
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from apps.core.services.graphql_client import graphql_mutation, graphql_query

logger = logging.getLogger(__name__)

_AI_CHATS_LIST = """
query AdminAiChatList($limit: Int!, $offset: Int!) {
  aiChats {
    aiChats(filters: { limit: $limit, offset: $offset }) {
      items {
        uuid
        title
        createdAt
        updatedAt
      }
      pageInfo {
        total
        limit
        offset
        hasNext
        hasPrevious
      }
    }
  }
}
"""

_CREATE_AI_CHAT = """
mutation AdminCreateAiChat($input: CreateAIChatInput!) {
  aiChats {
    createAIChat(input: $input) {
      uuid
      title
      messages {
        sender
        text
      }
    }
  }
}
"""

_SEND_MESSAGE = """
mutation AdminAiSendMessage($chatId: String!, $message: String!) {
  aiChats {
    sendMessage(chatId: $chatId, input: { message: $message }) {
      uuid
      title
      messages {
        sender
        text
      }
    }
  }
}
"""


def _errors_payload(resp: Dict[str, Any]) -> Optional[str]:
    errs = resp.get("errors")
    if isinstance(errs, list) and errs:
        first = errs[0]
        if isinstance(first, dict):
            return str(first.get("message", first))
        return str(first)
    return None


def _ai_chats_root(data: Dict[str, Any]) -> Dict[str, Any]:
    root = data.get("aiChats")
    return root if isinstance(root, dict) else {}


def _last_ai_reply(chat: Optional[Dict[str, Any]]) -> str:
    if not chat:
        return ""
    messages = chat.get("messages")
    if not isinstance(messages, list):
        return ""
    for m in reversed(messages):
        if not isinstance(m, dict):
            continue
        if m.get("sender") == "ai":
            return str(m.get("text") or "")
    return ""


def get_sessions(token: str = "") -> List[Dict[str, Any]]:
    """List chats for the current user via ``aiChats.aiChats``."""
    if not token:
        return []
    try:
        resp = graphql_query(_AI_CHATS_LIST, {"limit": 50, "offset": 0}, token=token)
        err = _errors_payload(resp)
        if err:
            logger.warning("get_sessions GraphQL: %s", err)
            return []
        data = resp.get("data")
        if not isinstance(data, dict):
            return []
        conn = _ai_chats_root(data).get("aiChats")
        if not isinstance(conn, dict):
            return []
        items = conn.get("items")
        if not isinstance(items, list):
            return []
        out: List[Dict[str, Any]] = []
        for it in items:
            if not isinstance(it, dict):
                continue
            uid = it.get("uuid")
            out.append(
                {
                    "id": uid,
                    "session_id": uid,
                    "title": it.get("title"),
                    "createdAt": it.get("createdAt"),
                    "messageCount": 0,
                }
            )
        return out
    except Exception as exc:
        logger.warning("get_sessions failed: %s", exc)
        return []


def send_message(session_id: str, content: str, token: str = "") -> Dict[str, Any]:
    """
    Send a user message and return ``{"reply": ...}`` or ``{"error": ...}``.

    Uses ``createAIChat`` when ``session_id`` is empty, then ``sendMessage``.
    """
    if not token:
        return {"error": "Not authenticated"}
    text = (content or "").strip()
    if not text:
        return {"error": "content is required"}
    chat_id = (session_id or "").strip()
    try:
        if not chat_id:
            resp = graphql_mutation(
                _CREATE_AI_CHAT,
                {"input": {"title": "Admin chat", "messages": []}},
                token=token,
            )
            err = _errors_payload(resp)
            if err:
                return {"error": err}
            data = resp.get("data")
            if not isinstance(data, dict):
                return {"error": "Invalid response"}
            created = _ai_chats_root(data).get("createAIChat")
            if not isinstance(created, dict) or not created.get("uuid"):
                return {"error": "createAIChat failed"}
            chat_id = str(created["uuid"])

        resp = graphql_mutation(
            _SEND_MESSAGE,
            {"chatId": chat_id, "message": text},
            token=token,
        )
        err = _errors_payload(resp)
        if err:
            return {"error": err}
        data = resp.get("data")
        if not isinstance(data, dict):
            return {"error": "Invalid response"}
        updated = _ai_chats_root(data).get("sendMessage")
        reply = _last_ai_reply(updated if isinstance(updated, dict) else None)
        return {
            "reply": reply or "(no AI text in response)",
            "session_id": chat_id,
        }
    except Exception as exc:
        logger.warning("send_message failed: %s", exc)
        return {"error": str(exc)}
