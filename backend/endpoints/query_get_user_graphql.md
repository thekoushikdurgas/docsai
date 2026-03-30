---
title: "graphql/GetUser"
source_json: query_get_user_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetUser

## Overview

Get user by UUID. Accepts uuid (ID!, required, valid UUID format). Returns User object with uuid, email, name, isActive, lastSignInAt, createdAt, updatedAt, and profile (jobTitle, bio, role, credits, subscriptionPlan, subscriptionStatus, avatarUrl). Uses DataLoaders to prevent N+1 queries. Regular users can only query their own UUID; Admin/SuperAdmin can query any user. Raises NotFoundError (404) if user doesn't exist. Raises ForbiddenError (403) if regular user tries to access another user's data.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_user_graphql |
| _id | query_get_user_graphql-001 |
| endpoint_path | graphql/GetUser |
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
| router_file | contact360/dashboard/src/services/graphql/usersService.ts |


## GraphQL operation

```graphql
query GetUser($uuid: ID!) { users { user(uuid: $uuid) { uuid email name isActive profile { jobTitle bio role credits subscriptionPlan } } } }
```

## Service / repository methods

### service_methods

- user

### repository_methods

- get_user_by_uuid

## Inventory

- **page_count:** 0
- **Source:** `query_get_user_graphql.json`

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

- **Security Auditing**: Access to PII is logged in Admin audit trails.

## Related endpoint graph

- **Inbound**: `Admin Users Page` (Frontend), `Profile UI`.
- **Outbound**: `GetUserHistory` (drill-down).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_user_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
