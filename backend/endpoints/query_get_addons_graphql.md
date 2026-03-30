---
title: "graphql/GetAddons"
source_json: query_get_addons_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetAddons

## Overview

Get available addon packages with pricing and credit information.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_addons_graphql |
| _id | query_get_addons_graphql-001 |
| endpoint_path | graphql/GetAddons |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 0.x |
| introduced_in | 0.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/billing/queries.py |
| router_file | contact360/dashboard/src/services/graphql/billingService.ts |


## Service / repository methods

### service_methods

- getAddons
- addons

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /billing | Billing Page | billingService | useBillingPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_addons_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation & Pre-Product Stabilization (Billing bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `addon_packages` | READ | [addon_packages.sql](../database/tables/addon_packages.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Reads active `addon_packages` via BillingRepository. No downstream service calls.

## Related endpoint graph

- **Inbound**: `Billing Page` (Frontend), `PurchaseAddon` (addon selection).
- **Outbound**: `PurchaseAddon` (user selects addon from list).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_addons_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
