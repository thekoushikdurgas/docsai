---
title: "graphql/GetMe"
source_json: query_get_me_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetMe

## Overview

Get current authenticated user information. No input required. Returns User object with uuid, email, name, isActive, lastSignInAt, createdAt, updatedAt, and profile (jobTitle, bio, role, credits, subscription info). Returns null if user is not authenticated. Used for session validation and displaying user info in the UI.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_me_graphql |
| _id | query_get_me_graphql-001 |
| endpoint_path | graphql/GetMe |
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


## GraphQL operation

```graphql
query { auth { me { uuid email name profile { jobTitle bio role credits } } } }
```

## Service / repository methods

### service_methods

- me

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | authService | useProfilePage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_me_graphql.json`

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

- **Subscription Status**: Aggregates data from `billing` service layer.

## Related endpoint graph

- **Inbound**: `Standard Layout` (Global), `Login`.
- **Outbound**: `GetBilling` (current tier).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_me_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
