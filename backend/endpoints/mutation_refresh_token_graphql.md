---
title: "graphql/RefreshToken"
source_json: mutation_refresh_token_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/RefreshToken

## Overview

Refresh access token using refresh token. Accepts RefreshTokenInput with refreshToken (required, valid JWT). Returns AuthPayload containing new accessToken (JWT, expires in 30 minutes), new refreshToken (JWT, expires in 7 days), and user info (uuid, email, name). Implements token rotation - both tokens are refreshed on each call. Validates refresh token signature and expiration. Raises UnauthorizedError (401) if refresh token is invalid, expired, or blacklisted. Used internally by graphqlClient for automatic token refresh when access token expires.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_refresh_token_graphql |
| _id | mutation_refresh_token_graphql-001 |
| endpoint_path | graphql/RefreshToken |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.1.0 |

## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |

## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/auth/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/authService.ts |


## GraphQL operation

```graphql
mutation RefreshToken($input: RefreshTokenInput!) { auth { refreshToken(input: $input) { accessToken refreshToken user { uuid email name } } } }
```

## Service / repository methods

### service_methods

- refreshToken

## Inventory

- **page_count:** 0
- **Source:** `mutation_refresh_token_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Auth/Bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | READ | [users.sql](../database/tables/users.sql) |
| `token_blacklist` | READ / WRITE | [token_blacklist.sql](../database/tables/token_blacklist.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Token Rotation**: Blacklists the old refresh token upon new issue.

## Related endpoint graph

- **Inbound**: `AuthContext` (Frontend), `Login`.
- **Outbound**: `GetMe` (identity).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_refresh_token_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
