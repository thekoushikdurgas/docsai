---
title: "graphql/DeleteSavedSearch"
source_json: mutation_delete_saved_search_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteSavedSearch

## Overview

Delete a saved search by ID. Returns boolean indicating success.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_saved_search_graphql |
| _id | mutation_delete_saved_search_graphql-001 |
| endpoint_path | graphql/DeleteSavedSearch |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 9.x |
| introduced_in | 9.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/saved_searches/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/savedSearchesService.ts |


## Service / repository methods

### service_methods

- deleteSavedSearch

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /contacts | Contacts Page | savedSearchesService | useSavedSearches | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_delete_saved_search_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — Feature Maturity (Saved Search).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `saved_searches` | DELETE | [saved_searches.sql](../database/tables/saved_searches.sql) |
| `vql_queries` | DELETE | [vql_queries.sql](../database/tables/vql_queries.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Search Module Lineage](../database/connectra_data_lineage.md)

## Downstream services (cross-endpoint)

- **Sync**: Contextual search results via `contact360.io/sync`.

## Related endpoint graph

- **Inbound**: `Search Page` (Delete Action).
- **Outbound**: `ListSavedSearches`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_saved_search_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
