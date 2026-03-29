---
title: "graphql/GetAIChat"
source_json: query_get_ai_chat_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetAIChat

## Overview

Get a specific AI chat conversation by UUID. Returns full chat with uuid, userId, title, messages (with contacts), createdAt, updatedAt.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_ai_chat_graphql |
| _id | query_get_ai_chat_graphql-001 |
| endpoint_path | graphql/GetAIChat |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
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
| service_file | appointment360/app/graphql/modules/ai_chats/queries.py |
| router_file | contact360/dashboard/src/services/graphql/aiChatsService.ts |


## Service / repository methods

### service_methods

- getChat
- aiChat

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /ai-chat | Ai Chat Page | aiChatsService | useAiChat | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_ai_chat_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — AI Workflows.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `ai_chats` | READ | [ai_chats.sql](../database/tables/ai_chats.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Contact AI Lineage](../database/contact_ai_data_lineage.md)

## Downstream services (cross-endpoint)

- **Contact AI Lambda** (`backend(dev)/contact.ai`): Chat and message retrieval delegated via `LambdaAIClient`.

## Related endpoint graph

- **Inbound**: `AI Chat Page` (Frontend chat thread), `ListAIChats` (sidebar click), `CreateAIChat` (open new).
- **Outbound**: `SendMessage` (continue conversation), `UpdateAIChat` (rename).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_ai_chat_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
