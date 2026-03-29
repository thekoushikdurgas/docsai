---
title: "graphql/UpdateAddon"
source_json: mutation_update_addon_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/UpdateAddon

## Overview

Update an existing addon package. Accepts id (String!, required) and UpdateAddonInput with optional fields: name (String), credits (Int), ratePerCredit (Float), price (Float), isActive (Boolean). Returns object with message and id. SuperAdmin only. Only provided fields are updated (partial update).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_update_addon_graphql |
| _id | mutation_update_addon_graphql-001 |
| endpoint_path | graphql/UpdateAddon |
| method | MUTATION |
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
| service_file | appointment360/app/graphql/modules/billing/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/billingService.ts |


## Service / repository methods

### service_methods

- updateAddon

## Inventory

- **page_count:** 0
- **Source:** `mutation_update_addon_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation & Pre-Product Stabilization (Billing bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `addon_packages` | READ / WRITE | [addon_packages.sql](../database/tables/addon_packages.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Direct update on `addon_packages` via BillingRepository. No downstream service calls.

## Related endpoint graph

- **Inbound**: `Admin Billing Page` (Frontend SuperAdmin).
- **Outbound**: `GetAddons` (verify update), `GetAdminAddons` (admin listing).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_update_addon_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
