---
title: "graphql/ListAPIKeys"
source_json: query_list_api_keys_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/ListAPIKeys

## Overview

List all API keys for the current user. Returns key metadata including name, prefix, created date, last used date, and permissions.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_api_keys_graphql |
| _id | query_list_api_keys_graphql-001 |
| endpoint_path | graphql/ListAPIKeys |
| method | QUERY |
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
| service_file | contact360.io/api/app/graphql/modules/profile/queries.py |
| router_file | contact360/dashboard/src/services/graphql/profileService.ts |


## Service / repository methods

### service_methods

- listAPIKeys

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /profile | Profile Page | profileService | useProfilePage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_list_api_keys_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `5.x` — Governance & RBAC (API Key Listing).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `api_keys` | READ | [api_keys.sql](../database/tables/api_keys.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Admin Governance](../database/admin_data_lineage.md)

## Downstream services (cross-endpoint)

- **Admin**: Visibility in `contact360.io/admin`.

## Related endpoint graph

- **Inbound**: `Profile Page`.
- **Outbound**: `CreateAPIKey`, `DeleteAPIKey`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_api_keys_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
