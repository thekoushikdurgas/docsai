---
title: "graphql/ListAIChats"
source_json: query_list_ai_chats_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListAIChats

## Overview

List AI chat conversations for current user. Accepts optional AIChatFilterInput with title (String, partial match), search (String, searches title and messages), startDate/endDate (DateTime range), orderBy (enum: CREATED_AT, UPDATED_AT, TITLE), orderDirection (enum: ASC, DESC), limit (Int, default 100), offset (Int, default 0). Returns AIChatConnection with items (array of AIChat with uuid, title, createdAt, updatedAt), total, limit, offset, hasNext, hasPrevious. Uses Lambda AI service. User isolation enforced.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_ai_chats_graphql |
| _id | query_list_ai_chats_graphql-001 |
| endpoint_path | graphql/ListAIChats |
| method | QUERY |
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
| service_file | appointment360/app/graphql/modules/ai_chats/queries.py |
| router_file | contact360/dashboard/src/services/graphql/aiChatsService.ts |


## GraphQL operation

```graphql
query ListAIChats($input: AIChatFilterInput) { aiChats { chats(input: $input) { items { uuid title createdAt updatedAt } total hasNext } } }
```

## Service / repository methods

### service_methods

- chats

### repository_methods

- get_chats_by_user

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /ai-chat | Ai Chat Page | aiChatsService | useAiChat | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_list_ai_chats_graphql.json`

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

- **Contact AI Lambda** (`backend(dev)/contact.ai`): Chat listing delegated via `LambdaAIClient`. Returns user-scoped chats with pagination.

## Related endpoint graph

- **Inbound**: `AI Chat Page` (Frontend sidebar listing).
- **Outbound**: `GetAIChat` (open specific chat), `CreateAIChat` (new chat button), `DeleteAIChat` (delete action).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_ai_chats_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
