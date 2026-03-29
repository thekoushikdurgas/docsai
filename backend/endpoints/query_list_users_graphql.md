---
title: "graphql/ListUsers"
source_json: query_list_users_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListUsers

## Overview

List all users with pagination. Accepts limit (Int, default 100, validated via validate_pagination) and offset (Int, default 0, validated via validate_pagination). Returns array of User objects with uuid, email, name, isActive, lastSignInAt, createdAt, updatedAt, and profile information. Profile data is eagerly loaded using selectinload to avoid lazy loading issues. Raises ForbiddenError (403) if current user is not Admin or SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_users_graphql |
| _id | query_list_users_graphql-001 |
| endpoint_path | graphql/ListUsers |
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
| service_file | contact360.io/api/app/graphql/modules/users/queries.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## GraphQL operation

```graphql
query ListUsers($limit: Int, $offset: Int) { users { users(limit: $limit, offset: $offset) { uuid email name isActive createdAt } } }
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
- **Source:** `query_list_users_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Identity).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | READ | [users.sql](../database/tables/users.sql) |
| `user_profiles` | READ | [user_profiles.sql](../database/tables/user_profiles.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Security Auditing**: Admin access to global user lists is logged.

## Related endpoint graph

- **Inbound**: `Admin Users Page` (Frontend).
- **Outbound**: `GetUser` (detail view).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_users_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
