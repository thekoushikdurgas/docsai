# ai.server — gateway route matrix (Era 3)

| `AIServerClient` method | HTTP endpoint |
|---------------------------|---------------|
| `chat` | `POST /chat` |
| `list_chats` | `GET /api/v1/ai-chats/` |
| `create_chat` | `POST /api/v1/ai-chats/` |
| `get_chat` | `GET /api/v1/ai-chats/{id}/` |
| `update_chat` | `PUT /api/v1/ai-chats/{id}/` |
| `delete_chat` | `DELETE /api/v1/ai-chats/{id}/` |
| `send_message` | `POST /api/v1/ai-chats/{id}/message` |
| `send_message_stream` | `POST /api/v1/ai-chats/{id}/message/stream` |
| `analyze_email_risk` | `POST /api/v1/gemini/email/analyze` |
| `generate_company_summary` | `POST /api/v1/gemini/company/summary` |
| `parse_contact_filters` | `POST /api/v1/gemini/parse-filters` |

Headers: **`X-API-Key`** (satellite); chat list/create/... may send **`X-User-ID`** (accepted; future multi-tenant scoping).

Last updated: 2026-04-15.
