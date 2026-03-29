---
title: "graphql/connectIntegration"
source_json: mutation_connect_integration.json
generator: json_to_markdown_endpoints.py
---

# graphql/connectIntegration

## Overview

connectIntegration operation for backend docs expansion.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_connect_integration |
| _id | mutation_connect_integration-001 |
| endpoint_path | graphql/connectIntegration |
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
| service_file | appointment360/app/graphql/modules/integrations/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/integrationService.ts |


## GraphQL operation

```graphql
mutation connectIntegration
```

## Service / repository methods

### service_methods

- connectIntegration

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /integrations | Integrations Page | integrationService | useIntegrations | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_connect_integration.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `8.x` — Public & Private APIs and Endpoints.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `integrations` | WRITE | [integrations.sql](../database/tables/integrations.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Direct insert into `integrations` table. OAuth flow and token exchange handled inline.

## Related endpoint graph

- **Inbound**: `Integrations Page` (Frontend connect button).
- **Outbound**: `ListIntegrations` (verify connection), `SyncIntegration` (initial data sync).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_connect_integration.json`. Re-run `python json_to_markdown_endpoints.py`.*
