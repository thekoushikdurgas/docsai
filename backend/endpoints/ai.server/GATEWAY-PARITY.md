# ai.server — gateway parity (Era 10)

Checklist: Python [`AIServerClient`](../../../../contact360.io/api/app/clients/ai_client.py) vs [`router.go`](../../../../EC2/ai.server/internal/api/router.go).

| Client method | Endpoint | Status |
|---------------|----------|--------|
| `chat` | `POST /chat` | Implemented |
| `list_chats` | `GET /api/v1/ai-chats/` | Implemented |
| `create_chat` | `POST /api/v1/ai-chats/` | Implemented |
| `get_chat` | `GET /api/v1/ai-chats/{id}/` | Implemented (with messages) |
| `update_chat` | `PUT /api/v1/ai-chats/{id}/` | Implemented |
| `delete_chat` | `DELETE /api/v1/ai-chats/{id}/` | Implemented |
| `send_message` | `POST /api/v1/ai-chats/{id}/message` | Implemented (`message` or `content`) |
| `send_message_stream` | `POST .../message/stream` | Implemented (SSE passthrough) |
| `analyze_email_risk` | `POST /api/v1/gemini/email/analyze` | Implemented |
| `generate_company_summary` | `POST /api/v1/gemini/company/summary` | Implemented |
| `parse_contact_filters` | `POST /api/v1/gemini/parse-filters` | Implemented |

Last updated: 2026-04-15.
