---
title: "graphql/SendMessage"
source_json: mutation_send_message_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/SendMessage

## Overview

Send a message to an AI chat and receive AI-generated response. Accepts SendMessageInput with chatId (required, UUID), message (required, String, max 10000 chars). Returns MessageResponse with messageId (UUID), userMessage (String), aiResponse (String), createdAt (DateTime). Uses Lambda AI service with Google Gemini AI for response generation. Chat history is maintained for context. Raises NotFoundError (404) if chat doesn't exist. Raises ForbiddenError (403) if user doesn't own the chat. Raises RateLimitError (429) if rate limit exceeded.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_send_message_graphql |
| _id | mutation_send_message_graphql-001 |
| endpoint_path | graphql/SendMessage |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limit | 10 requests/minute |
| rate_limited | True |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/ai_chats/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/aiChatsService.ts |


## GraphQL operation

```graphql
mutation SendMessage($input: SendMessageInput!) { aiChats { sendMessage(input: $input) { messageId userMessage aiResponse createdAt } } }
```

## Service / repository methods

### service_methods

- sendMessage

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /ai-chat | Ai Chat Page | aiChatsService | useAiChat | primary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_send_message_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (AI/Service Layer).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `ai_chat_messages` | WRITE | [ai_chat_messages.sql](../database/tables/ai_chat_messages.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [AI Service Architecture](../database/contact_ai_data_lineage.md)

## Downstream services (cross-endpoint)

- **AI Service**: Intelligence provided via `backend(dev)/contact.ai`.

## Related endpoint graph

- **Inbound**: `Ai Chat Page`.
- **Outbound**: `CreateAiChat`, `ListAiChats`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_send_message_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
