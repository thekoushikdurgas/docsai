---
title: "graphql/RevokeSession"
source_json: mutation_revoke_session_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/RevokeSession

## Overview

Revoke a session by its ID. Accepts RevokeSessionInput with sessionId (required, UUID). Adds session token to blacklist, invalidating it. Returns Boolean indicating success (true if revoked). User isolation enforced - users can only revoke their own sessions. Raises NotFoundError (404) if session not found. Raises ForbiddenError (403) if session belongs to another user.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_revoke_session_graphql |
| _id | mutation_revoke_session_graphql-001 |
| endpoint_path | graphql/RevokeSession |
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
| service_file | contact360.io/api/app/graphql/modules/profile/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/profileService.ts |


## GraphQL operation

```graphql
mutation RevokeSession($input: RevokeSessionInput!) { profile { revokeSession(input: $input) } }
```

## Service / repository methods

### service_methods

- revokeSession

### repository_methods

- blacklist_token

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | profileService | useSessions | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_revoke_session_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation (Auth/Sessions).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `sessions` | READ / WRITE | [sessions.sql](../database/tables/sessions.sql) |
| `token_blacklist` | WRITE | [token_blacklist.sql](../database/tables/token_blacklist.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Security Auditing**: Logs session revocation with device metadata.

## Related endpoint graph

- **Inbound**: `Profile Page` (Frontend), `Security Settings`.
- **Outbound**: `ListSessions` (refresh).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_revoke_session_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
