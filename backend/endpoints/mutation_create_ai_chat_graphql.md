---
title: "graphql/CreateAIChat"
source_json: mutation_create_ai_chat_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateAIChat

## Overview

Create a new AI chat conversation. Accepts optional CreateAIChatInput with title (optional, String, max 255 chars). Returns AIChat with uuid, title (auto-generated if not provided: 'New Chat YYYY-MM-DD HH:MM'), createdAt, updatedAt. Uses Lambda AI service for chat management. User isolation enforced. Raises ForbiddenError (403) if user is not ProUser or higher.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_ai_chat_graphql |
| _id | mutation_create_ai_chat_graphql-001 |
| endpoint_path | graphql/CreateAIChat |
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
mutation CreateAIChat($input: CreateAIChatInput) { aiChats { createChat(input: $input) { uuid title createdAt } } }
```

## Service / repository methods

### service_methods

- createChat

### repository_methods

- create_chat

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /ai-chat | Ai Chat Page | aiChatsService | useAiChat | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_create_ai_chat_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — AI Workflows.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `ai_chats` | WRITE | [ai_chats.sql](../database/tables/ai_chats.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Contact AI Lineage](../database/contact_ai_data_lineage.md)

## Downstream services (cross-endpoint)

- **Contact AI Lambda** (`backend(dev)/contact.ai`): Chat creation delegated via `LambdaAIClient`. Creates `ai_chats` row with user_uuid FK.

## Related endpoint graph

- **Inbound**: `AI Chat Page` (Frontend), `ListAIChats` (chat sidebar).
- **Outbound**: `GetAIChat` (open created chat), `SendMessage` (begin conversation).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_ai_chat_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
