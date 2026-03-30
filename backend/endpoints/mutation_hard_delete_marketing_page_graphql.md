---
title: "graphql/HardDeleteMarketingPage"
source_json: mutation_hard_delete_marketing_page_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/HardDeleteMarketingPage

## Overview

Permanently delete a marketing page (hard delete). Accepts HardDeleteMarketingPageInput with pageId (required, String, max 255 chars). Permanently removes page from database - cannot be undone. Returns Boolean (true if deleted). Uses MarketingService.delete_page with hard_delete=True. Raises NotFoundError (404) if page not found. Raises ForbiddenError (403) if not Admin/SuperAdmin. Use with caution.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_hard_delete_marketing_page_graphql |
| _id | mutation_hard_delete_marketing_page_graphql-001 |
| endpoint_path | graphql/HardDeleteMarketingPage |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
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
| service_file | appointment360/app/graphql/modules/marketing/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/marketingService.ts |


## GraphQL operation

```graphql
mutation HardDeleteMarketingPage($input: HardDeleteMarketingPageInput!) { marketing { hardDeleteMarketingPage(input: $input) } }
```

## Service / repository methods

### service_methods

- hardDeleteMarketingPage

### repository_methods

- hard_delete_marketing_page

## Inventory

- **page_count:** 0
- **Source:** `mutation_hard_delete_marketing_page_graphql.json`

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

*Generated from `mutation_hard_delete_marketing_page_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
