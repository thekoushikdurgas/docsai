---
title: "graphql/CreateAddon"
source_json: mutation_create_addon_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CreateAddon

## Overview

Create a new addon credits package. Accepts CreateAddonInput with id (required, String, unique identifier), name (required, String), credits (required, Int, number of credits), ratePerCredit (required, Float), price (required, Float), isActive (optional, Boolean, default true). Returns CreateAddonResponse with message (String), id (String). Raises ConflictError (409) if addon ID already exists. Raises ForbiddenError (403) if not SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_addon_graphql |
| _id | mutation_create_addon_graphql-001 |
| endpoint_path | graphql/CreateAddon |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
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


## GraphQL operation

```graphql
mutation CreateAddon($input: CreateAddonInput!) { billing { createAddon(input: $input) { message id } } }
```

## Service / repository methods

### service_methods

- createAddon

### repository_methods

- create_addon

## Inventory

- **page_count:** 0
- **Source:** `mutation_create_addon_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation & Pre-Product Stabilization (Billing bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `addon_packages` | WRITE | [addon_packages.sql](../database/tables/addon_packages.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Direct insert into `addon_packages` via BillingRepository. No downstream service calls.

## Related endpoint graph

- **Inbound**: `Admin Billing Page` (Frontend SuperAdmin).
- **Outbound**: `GetAddons` (verify creation), `GetAdminAddons` (admin listing).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_addon_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
