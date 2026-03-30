---
title: "graphql/PromoteToSuperAdmin"
source_json: mutation_promote_to_super_admin_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/PromoteToSuperAdmin

## Overview

Promote a user to SuperAdmin role. Accepts PromoteToSuperAdminInput with userId (ID!, required, valid UUID format). Returns User with uuid, email, name, isActive, lastSignInAt, createdAt, updatedAt, and profile (role updated to 'SuperAdmin'). Only SuperAdmin can promote users. Role check via UserProfileRepository. Reloads user after promotion to get updated profile. Raises NotFoundError (404) if target user doesn't exist. Raises ForbiddenError (403) if current user is not SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_promote_to_super_admin_graphql |
| _id | mutation_promote_to_super_admin_graphql-001 |
| endpoint_path | graphql/PromoteToSuperAdmin |
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


## GraphQL operation

```graphql
mutation PromoteToSuperAdmin($input: PromoteToSuperAdminInput!) { users { promoteToSuperAdmin(input: $input) { uuid email name profile { role } } } }
```

## Service / repository methods

### service_methods

- promoteToSuperAdmin

### repository_methods

- promote_user_to_super_admin

## Inventory

- **page_count:** 0
- **Source:** `mutation_promote_to_super_admin_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — Governance & RBAC (SuperAdmin Promotion).

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
- **Outbound**: `GetMe`, `UpdateUserRole`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_promote_to_super_admin_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
