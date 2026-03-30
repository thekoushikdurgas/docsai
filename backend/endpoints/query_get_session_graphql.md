---
title: "graphql/GetSession"
source_json: query_get_session_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetSession

## Overview

Get current session information. Returns user UUID, email, authentication status, and last sign-in timestamp. Used by useSessionGuard hook for session validation across protected pages.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_session_graphql |
| _id | query_get_session_graphql-001 |
| endpoint_path | graphql/GetSession |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.4.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/auth/queries.py |
| router_file | contact360/dashboard/src/services/graphql/authService.ts |


## Service / repository methods

### service_methods

- getSession

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /login | Login Page | authService | useAuth | secondary | data_fetching | 2025-01-27T12:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_session_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Auth/Sessions).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `sessions` | READ | [sessions.sql](../database/tables/sessions.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Security Auditing**: None (read-only validation).

## Related endpoint graph

- **Inbound**: `Standard Layout` (Global), `protected` routes.
- **Outbound**: `GetMe` (identity).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_session_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
