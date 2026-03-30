---
title: "graphql/DeleteAPIKey"
source_json: mutation_delete_api_key_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteAPIKey

## Overview

Delete an API key by ID. Accepts DeleteAPIKeyInput with keyId (required, UUID). Permanently removes API key and revokes access. Returns Boolean indicating success (true if deleted). User isolation enforced - users can only delete their own API keys. Raises NotFoundError (404) if API key not found. Raises ForbiddenError (403) if key belongs to another user.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_api_key_graphql |
| _id | mutation_delete_api_key_graphql-001 |
| endpoint_path | graphql/DeleteAPIKey |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 5.x |
| introduced_in | 5.0.0 |


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
mutation DeleteAPIKey($input: DeleteAPIKeyInput!) { profile { deleteAPIKey(input: $input) } }
```

## Service / repository methods

### service_methods

- deleteAPIKey

### repository_methods

- delete_api_key

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | profileService | useAPIKeys | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_delete_api_key_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — Governance & RBAC (API Key Revocation).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `api_keys` | DELETE | [api_keys.sql](../database/tables/api_keys.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Admin Governance](../database/admin_data_lineage.md)

## Downstream services (cross-endpoint)

- **Admin**: Audit logging via `contact360.io/admin`.

## Related endpoint graph

- **Inbound**: `Profile Page`.
- **Outbound**: `CreateAPIKey`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_api_key_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
