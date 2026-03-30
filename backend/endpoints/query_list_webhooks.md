---
title: "graphql/listWebhooks"
source_json: query_list_webhooks.json
generator: json_to_markdown_endpoints.py
---

# graphql/listWebhooks

## Overview

listWebhooks operation for backend docs expansion.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_webhooks |
| _id | query_list_webhooks-001 |
| endpoint_path | graphql/listWebhooks |
| method | QUERY |
| api_version | graphql |
| endpoint_state | planned |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-03-24T00:00:00.000000+00:00 |
| updated_at | 2026-03-24T00:00:00.000000+00:00 |
| era | 8.x |
| introduced_in | 8.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/webhooks/queries.py |
| router_file | contact360/dashboard/src/services/graphql/webhookService.ts |


## GraphQL operation

```graphql
query listWebhooks
```

## Service / repository methods

### service_methods

- listWebhooks

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /integrations/webhooks | Integrations/Webhooks Page | webhookService | useWebhooks | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_list_webhooks.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `8.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

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

*Generated from `query_list_webhooks.json`. Re-run `python json_to_markdown_endpoints.py`.*
