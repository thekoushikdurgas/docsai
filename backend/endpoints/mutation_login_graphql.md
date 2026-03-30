---
title: "graphql/Login"
source_json: mutation_login_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/Login

## Overview

Authenticate user with email and password. Accepts LoginInput with email (required, valid email format), password (required, minimum 8 characters), and optional geolocation data. Returns AuthPayload containing accessToken (JWT, expires in 30 minutes), refreshToken (JWT, expires in 7 days), and user info (uuid, email, name). Password is validated using bcrypt. Failed login attempts return UnauthorizedError (401). User history is tracked if geolocation provided (non-blocking). Token blacklisting is checked to prevent reuse of logged-out tokens.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_login_graphql |
| _id | mutation_login_graphql-001 |
| endpoint_path | graphql/Login |
| method | MUTATION |
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
| rate_limit | 10 requests/minute |
| rate_limited | True |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/auth/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/authService.ts |


## GraphQL operation

```graphql
mutation Login($input: LoginInput!) { auth { login(input: $input) { accessToken refreshToken user { uuid email name } } } }
```

## Service / repository methods

### service_methods

- login

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /login | Login Page | authService | useAuth | primary | authentication | 2025-01-27T12:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_login_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Auth/Bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | READ | [users.sql](../database/tables/users.sql) |
| `user_history` | WRITE | [user_history.sql](../database/tables/user_history.sql) |
| `user_profiles` | READ | [user_profiles.sql](../database/tables/user_profiles.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Activity Pipeline**: Async tracking of login events.

## Related endpoint graph

- **Inbound**: `Register` (post-signup auto-login), `Login Page` (Frontend).
- **Outbound**: `GetMe` (identity verification), `GetUsage` (tier check).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_login_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
