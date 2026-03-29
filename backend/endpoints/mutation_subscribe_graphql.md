---
title: "graphql/Subscribe"
source_json: mutation_subscribe_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/Subscribe

## Overview

Subscribe to a subscription plan. Returns subscription details and payment information.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_subscribe_graphql |
| _id | mutation_subscribe_graphql-001 |
| endpoint_path | graphql/Subscribe |
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


## Service / repository methods

### service_methods

- subscribeToPlan
- subscribe

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /billing | Billing Page | billingService | useBilling | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_subscribe_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing Maturity.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `subscriptions` | WRITE | [subscriptions.sql](../database/tables/subscriptions.sql) |
| `user_profiles` | READ | [user_profiles.sql](../database/tables/user_profiles.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Stripe Integration**: External call to create/update subscription in Stripe dashboard.

## Related endpoint graph

- **Inbound**: `Billing Page`.
- **Outbound**: `GetBilling` (refresh state).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_subscribe_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
