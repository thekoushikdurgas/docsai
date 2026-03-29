---
title: "graphql/DeleteAIChat"
source_json: mutation_delete_ai_chat_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteAIChat

## Overview

Delete an AI chat by UUID. Accepts DeleteAIChatInput with chatId (required, UUID). Deletes chat and all associated messages. Returns Boolean indicating success (true if deleted). User isolation enforced - users can only delete their own chats. Raises NotFoundError (404) if chat not found. Raises ForbiddenError (403) if user doesn't own the chat or is not ProUser+.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_ai_chat_graphql |
| _id | mutation_delete_ai_chat_graphql-001 |
| endpoint_path | graphql/DeleteAIChat |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 5.x |
| introduced_in | 5.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/ai_chats/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/aiChatsService.ts |


## GraphQL operation

```graphql
mutation DeleteAIChat($input: DeleteAIChatInput!) { aiChats { deleteChat(input: $input) } }
```

## Service / repository methods

### service_methods

- deleteChat

### repository_methods

- delete_chat

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /ai-chat | Ai Chat Page | aiChatsService | useAiChat | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_delete_ai_chat_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — AI Workflows.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `ai_chats` | DELETE | [ai_chats.sql](../database/tables/ai_chats.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Contact AI Lineage](../database/contact_ai_data_lineage.md)

## Downstream services (cross-endpoint)

- **Contact AI Lambda** (`backend(dev)/contact.ai`): Chat deletion delegated via `LambdaAIClient`. Removes chat thread and message history.

## Related endpoint graph

- **Inbound**: `AI Chat Page` (Frontend chat sidebar delete action).
- **Outbound**: `ListAIChats` (refresh sidebar after deletion).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_ai_chat_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
