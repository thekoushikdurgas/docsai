---
title: "graphql/UpdateUserCredits"
source_json: mutation_update_user_credits_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdateUserCredits

## Overview

Update a user's credit balance. Returns updated user profile with new credit balance.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_user_credits_graphql |
| _id | mutation_update_user_credits_graphql-001 |
| endpoint_path | graphql/UpdateUserCredits |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
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
| service_file | contact360.io/api/app/graphql/modules/admin/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/adminService.ts |


## Service / repository methods

### service_methods

- updateUserCredits

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /admin/users | Admin Users Page | adminService | useAdminUsers | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_update_user_credits_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `7.x` — Deployment & Governance (Admin Credits).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | READ / WRITE | [users.sql](../database/tables/users.sql) |
| `user_profiles` | READ / WRITE | [user_profiles.sql](../database/tables/user_profiles.sql) |
| `user_history` | WRITE | [user_history.sql](../database/tables/user_history.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Billing/Credits**: Linked to `UserCreditsUpdate` event.

## Related endpoint graph

- **Inbound**: `Admin Users Page` (Frontend).
- **Outbound**: `GetMe` (identity sync).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_user_credits_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
