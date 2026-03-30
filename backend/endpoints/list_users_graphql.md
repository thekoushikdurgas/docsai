---
title: "graphql/ListUsers"
source_json: list_users_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListUsers

## Overview

List all users with filtering and pagination. Accepts optional UserFilterInput with email (String, partial match), role (enum: FreeUser, ProUser, Admin, SuperAdmin), isActive (Boolean), limit (Int, default 100), offset (Int, default 0). Returns UserConnection with items (array of User with id, email, firstName, lastName, role, isActive, createdAt), total, limit, offset, hasNext, hasPrevious. Raises ForbiddenError (403) if not SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | list_users_graphql |
| _id | list_users_graphql-001 |
| endpoint_path | graphql/ListUsers |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-19T12:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
| era | 1.x |
| introduced_in | 1.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limit | 50 requests/minute |
| rate_limited | True |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/admin/queries.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## GraphQL operation

```graphql
query ListUsers($input: UserFilterInput) { admin { users(input: $input) { items { id email firstName lastName role isActive } total hasNext } } }
```

## Service / repository methods

### service_methods

- users

### repository_methods

- get_all_users

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/users | Admin Users Page | adminService | useAdminUsers | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `list_users_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

- *No `db_tables_read` / `db_tables_write` in this spec — gateway-only or metadata TBD; see lineage.*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `list_users_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
