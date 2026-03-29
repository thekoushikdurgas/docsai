---
title: "graphql/deleteWebhook"
source_json: mutation_delete_webhook.json
generator: json_to_markdown_endpoints.py
---

# graphql/deleteWebhook

## Overview

deleteWebhook operation for backend docs expansion.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_webhook |
| _id | mutation_delete_webhook-001 |
| endpoint_path | graphql/deleteWebhook |
| method | MUTATION |
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
| service_file | appointment360/app/graphql/modules/webhooks/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/webhookService.ts |


## GraphQL operation

```graphql
mutation deleteWebhook
```

## Service / repository methods

### service_methods

- deleteWebhook

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /integrations/webhooks | Integrations/Webhooks Page | webhookService | useWebhooks | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_delete_webhook.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `8.x` — Public & Private APIs and Endpoints.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `webhooks` | DELETE | [webhooks.sql](../database/tables/webhooks.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Direct delete from `webhooks` table. Disables webhook delivery.

## Related endpoint graph

- **Inbound**: `Integrations/Webhooks Page` (Frontend delete action).
- **Outbound**: `ListWebhooks` (verify deletion).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_webhook.json`. Re-run `python json_to_markdown_endpoints.py`.*
