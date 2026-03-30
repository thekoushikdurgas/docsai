---
title: "graphql/ListSessions"
source_json: query_list_sessions_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListSessions

## Overview

List all active sessions for the current user. Returns session metadata including device, location, IP, and last activity.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_sessions_graphql |
| _id | query_list_sessions_graphql-001 |
| endpoint_path | graphql/ListSessions |
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
| service_file | contact360.io/api/app/graphql/modules/profile/queries.py |
| router_file | contact360/dashboard/src/services/graphql/profileService.ts |


## Service / repository methods

### service_methods

- listSessions

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | profileService | useProfilePage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_list_sessions_graphql.json`

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

- **Security Auditing**: None (read-only listing).

## Related endpoint graph

- **Inbound**: `Profile Page` (Frontend), `Security Settings`.
- **Outbound**: `RevokeSession` (to invalidation).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_sessions_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
