---
title: "graphql/DeleteUser"
source_json: mutation_delete_user_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteUser

## Overview

Delete a user by UUID. Returns boolean indicating success.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_user_graphql |
| _id | mutation_delete_user_graphql-001 |
| endpoint_path | graphql/DeleteUser |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 7.x |
| introduced_in | 7.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | superadmin |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/admin/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## Service / repository methods

### service_methods

- deleteUser

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/users | Admin Users Page | adminService | useAdminUsers | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_delete_user_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `7.x` — Deployment & Governance (Privileged User Management).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | DELETE | [users.sql](../database/tables/users.sql) |
| `user_profiles` | CASCADE DELETE | [user_profiles.sql](../database/tables/user_profiles.sql) |
| `user_history` | CASCADE DELETE | [user_history.sql](../database/tables/user_history.sql) |
| `user_activities` | CASCADE DELETE | [user_activities.sql](../database/tables/user_activities.sql) |
| `sessions` | CASCADE DELETE | [sessions.sql](../database/tables/sessions.sql) |
| `token_blacklist` | CASCADE DELETE | [token_blacklist.sql](../database/tables/token_blacklist.sql) |
| `saved_searches` | CASCADE DELETE | [saved_searches.sql](../database/tables/saved_searches.sql) |
| `notifications` | CASCADE DELETE | [notifications.sql](../database/tables/notifications.sql) |
| `ai_chats` | CASCADE DELETE | [ai_chats.sql](../database/tables/ai_chats.sql) |
| `two_factor` | CASCADE DELETE | [two_factor.sql](../database/tables/two_factor.sql) |
| `team_members` | CASCADE DELETE | [team_members.sql](../database/tables/team_members.sql) |
| `api_keys` | CASCADE DELETE | [api_keys.sql](../database/tables/api_keys.sql) |
| `feature_usage` | CASCADE DELETE | [feature_usage.sql](../database/tables/feature_usage.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Direct PostgreSQL delete with ON DELETE CASCADE across all user-scoped tables.
- **S3 Storage**: User's logical bucket and all objects (avatars, uploads, exports) remain orphaned — manual cleanup required.

## Related endpoint graph

- **Inbound**: `Admin Users Page` (Frontend), `ListUsers` (admin search).
- **Outbound**: Triggers cascade across all user data; no further endpoint calls.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_user_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
