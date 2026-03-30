---
title: "graphql/GetUserHistory"
source_json: query_get_user_history_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetUserHistory

## Overview

Get user activity history records (registration/login events) with optional filtering (userId, eventType) and pagination. Returns paginated history items with geolocation data (IP, continent, country, city, device, etc.).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_user_history_graphql |
| _id | query_get_user_history_graphql-001 |
| endpoint_path | graphql/GetUserHistory |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.5.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/admin/queries.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## Service / repository methods

### service_methods

- getUserHistory
- userHistory

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/user-history | Admin User History Page | adminService | useAdminUserHistory | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_user_history_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Identity).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_history` | READ | [user_history.sql](../database/tables/user_history.sql) |
| `users` | READ | [users.sql](../database/tables/users.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Security Auditing**: Access to history logs is restricted to Admins.

## Related endpoint graph

- **Inbound**: `Admin User History Page` (Frontend).
- **Outbound**: `GetUser` (identity sync).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_user_history_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
