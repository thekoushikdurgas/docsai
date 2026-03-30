---
title: "graphql/DeleteAddon"
source_json: mutation_delete_addon_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeleteAddon

## Overview

Delete an addon credits package. Accepts DeleteAddonInput with addonId (required, String). Permanently removes addon package. Returns DeleteAddonResponse with message (String), id (String). Raises NotFoundError (404) if addon not found. Raises ForbiddenError (403) if not SuperAdmin.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_addon_graphql |
| _id | mutation_delete_addon_graphql-001 |
| endpoint_path | graphql/DeleteAddon |
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
mutation DeleteAddon($input: DeleteAddonInput!) { billing { deleteAddon(input: $input) { message id } } }
```

## Service / repository methods

### service_methods

- deleteAddon

### repository_methods

- delete_addon

## Inventory

- **page_count:** 0
- **Source:** `mutation_delete_addon_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation & Pre-Product Stabilization (Billing bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `addon_packages` | DELETE | [addon_packages.sql](../database/tables/addon_packages.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Direct delete from `addon_packages` via BillingRepository. No downstream service calls.

## Related endpoint graph

- **Inbound**: `Admin Billing Page` (Frontend SuperAdmin).
- **Outbound**: `GetAddons` (verify deletion), `GetAdminAddons` (admin listing).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_addon_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
