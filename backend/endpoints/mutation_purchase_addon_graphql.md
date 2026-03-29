---
title: "graphql/PurchaseAddon"
source_json: mutation_purchase_addon_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/PurchaseAddon

## Overview

Purchase an addon credits package. Accepts PurchaseAddonInput with addonId (required, String, valid addon ID). Validates addon exists and is active. Adds credits to user's account. Returns PurchaseAddonResponse with success (Boolean), message (String), creditsAdded (Int), newCreditBalance (Int). Raises NotFoundError (404) if addon not found. Raises BadRequestError (400) if addon inactive. Activity logged (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_purchase_addon_graphql |
| _id | mutation_purchase_addon_graphql-001 |
| endpoint_path | graphql/PurchaseAddon |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 1.x |
| introduced_in | 1.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/billing/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/billingService.ts |


## GraphQL operation

```graphql
mutation PurchaseAddon($input: PurchaseAddonInput!) { billing { purchaseAddon(input: $input) { success message creditsAdded newCreditBalance } } }
```

## Service / repository methods

### service_methods

- purchaseAddon

### repository_methods

- add_user_credits

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /billing | Billing Page | billingService | useBilling | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_purchase_addon_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing (Addons).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `addons` | READ | [addons.sql](../database/tables/addons.sql) |
| `user_profiles` | WRITE | [user_profiles.sql](../database/tables/user_profiles.sql) |
| `billing_history` | WRITE | [billing_history.sql](../database/tables/billing_history.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Payment Gateway**: Triggers Stripe checkout/payment for one-time addon purchases.

## Related endpoint graph

- **Inbound**: `Marketplace Page`.
- **Outbound**: `GetBilling` (state update).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_purchase_addon_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
