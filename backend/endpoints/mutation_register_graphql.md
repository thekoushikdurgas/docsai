---
title: "graphql/Register"
source_json: mutation_register_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/Register

## Overview

Register a new user account. Accepts RegisterInput with name (required, 1-255 characters), email (required, valid email format, must be unique), password (required, minimum 8 characters), and optional geolocation data. Returns AuthPayload containing accessToken (JWT, expires in 30 minutes), refreshToken (JWT, expires in 7 days), and user info (uuid, email, name). Password is hashed using bcrypt before storage. Duplicate email raises ValidationError with fieldErrors. User and profile creation are atomic with transaction rollback on failure. User history is tracked if geolocation provided (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_register_graphql |
| _id | mutation_register_graphql-001 |
| endpoint_path | graphql/Register |
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
| rate_limit | 10 requests/minute |
| rate_limited | True |

## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/auth/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/authService.ts |

## GraphQL operation

```graphql
mutation Register($input: RegisterInput!) { auth { register(input: $input) { accessToken refreshToken user { uuid email name } } } }
```

## Service / repository methods

### service_methods

- register

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /register | Register Page | authService | useAuth | primary | authentication | 2025-01-27T12:00:00.000000+00:00 |

## Inventory

- **page_count:** 1
- **Source:** `mutation_register_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Auth/Bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `users` | WRITE | [users.sql](../database/tables/users.sql) |
| `user_profiles` | WRITE | [user_profiles.sql](../database/tables/user_profiles.sql) |
| `user_history` | WRITE | [user_history.sql](../database/tables/user_history.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Welcome Email**: Triggers async welcome sequence via `emailapis` Lambda.

## Related endpoint graph

- **Inbound**: `Register Page` (Frontend).
- **Outbound**: `Login` (auto-login), `GetMe` (identity).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_register_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
