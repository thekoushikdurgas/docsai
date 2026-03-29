---
title: "graphql/CreateAPIKey"
source_json: mutation_create_api_key_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateAPIKey

## Overview

Create a new API key. Accepts CreateAPIKeyInput with name (required, String, max 255 chars), permissions (optional, array of enum: read, write, default: [read]). Returns CreateAPIKeyResponse with id (UUID), name (String), key (String, full key - shown only once), keyPrefix (String, first 8 chars for display), permissions (array), createdAt (DateTime). Key is hashed before storage. Important: Full key is returned only once on creation.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_api_key_graphql |
| _id | mutation_create_api_key_graphql-001 |
| endpoint_path | graphql/CreateAPIKey |
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
mutation CreateAPIKey($input: CreateAPIKeyInput!) { profile { createAPIKey(input: $input) { id name key keyPrefix permissions createdAt } } }
```

## Service / repository methods

### service_methods

- createAPIKey

### repository_methods

- create_api_key

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | profileService | useAPIKeys | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_create_api_key_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — Governance & RBAC (API Key Management).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `api_keys` | WRITE | [api_keys.sql](../database/tables/api_keys.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Admin Governance](../database/admin_data_lineage.md)

## Downstream services (cross-endpoint)

- **Admin**: Audit logging via `contact360.io/admin`.

## Related endpoint graph

- **Inbound**: `Profile Page`.
- **Outbound**: `ListAPIKeys`, `DeleteAPIKey`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_api_key_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
