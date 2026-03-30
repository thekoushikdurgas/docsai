---
title: "graphql/Logout"
source_json: mutation_logout_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/Logout

## Overview

Logout current user and blacklist access token on server. No input required. Returns Boolean (true on success). The access token is added to a blacklist in the database, preventing reuse even if not expired. Used by AuthContext logout function and UserMenuPopup component. Raises UnauthorizedError (401) if user is not authenticated.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_logout_graphql |
| _id | mutation_logout_graphql-001 |
| endpoint_path | graphql/Logout |
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
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/auth/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/authService.ts |


## GraphQL operation

```graphql
mutation Logout { auth { logout } }
```

## Service / repository methods

### service_methods

- logout

## Inventory

- **page_count:** 0
- **Source:** `mutation_logout_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Auth/Bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `token_blacklist` | WRITE | [token_blacklist.sql](../database/tables/token_blacklist.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Security Auditing**: Logs logout event via internal stats.

## Related endpoint graph

- **Inbound**: `Logout Button` (Frontend).
- **Outbound**: `Login` (redirect).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_logout_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
