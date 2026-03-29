---
title: "graphql/UpdateSavedSearchUsage"
source_json: mutation_update_saved_search_usage_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdateSavedSearchUsage

## Overview

Update the last used timestamp and increment use count for a saved search. Accepts id (ID!, must be positive integer). Returns Boolean (true if successful). Uses SavedSearchRepository.update_usage to update usage tracking. User isolation enforced - users can only update usage for their own saved searches. Automatically sets last_used_at to current UTC timestamp and increments use_count by 1. Raises NotFoundError if saved search doesn't exist or ForbiddenError if it doesn't belong to user. Silently fails for usage tracking (no toast shown).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_saved_search_usage_graphql |
| _id | mutation_update_saved_search_usage_graphql-001 |
| endpoint_path | graphql/UpdateSavedSearchUsage |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
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
| service_file | appointment360/app/graphql/modules/saved_searches/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/savedSearchesService.ts |


## Service / repository methods

### service_methods

- updateSavedSearchUsage

## Inventory

- **page_count:** 0
- **Source:** `mutation_update_saved_search_usage_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

- *No `db_tables_read` / `db_tables_write` in this spec — gateway-only or metadata TBD; see lineage.*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_saved_search_usage_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
