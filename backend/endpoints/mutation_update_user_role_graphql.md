---
title: "graphql/UpdateUserRole"
source_json: mutation_update_user_role_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdateUserRole

## Overview

Update a user's role (FreeUser, ProUser, Admin, SuperAdmin). Returns updated user profile.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_user_role_graphql |
| _id | mutation_update_user_role_graphql-001 |
| endpoint_path | graphql/UpdateUserRole |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 5.x |
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
| service_file | contact360.io/api/app/graphql/modules/admin/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## Service / repository methods

### service_methods

- updateUserRole

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/users | Admin Users Page | adminService | useAdminUsers | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_update_user_role_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — Governance & RBAC (Role Management).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | WRITE | [users.sql](../database/tables/users.sql) |
| `user_profiles` | WRITE | [user_profiles.sql](../database/tables/user_profiles.sql) |
| `user_history` | WRITE | [user_history.sql](../database/tables/user_history.sql) |
| `rbac_roles` | READ | [rbac_roles.sql](../database/tables/rbac_roles.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Admin Governance](../database/admin_data_lineage.md)

## Downstream services (cross-endpoint)

- **Admin**: Reflected in `contact360.io/admin`.

## Related endpoint graph

- **Inbound**: `Admin Users Page`.
- **Outbound**: `GetMe`, `PromoteToAdmin`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_user_role_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
