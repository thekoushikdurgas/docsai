---
title: "graphql/GetBilling"
source_json: get_billing_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetBilling

## Overview

Get current user billing information. No input required. Returns BillingInfo with subscriptionPlan, subscriptionStatus, subscriptionPeriod, subscriptionStartedAt, subscriptionEndsAt, credits, creditLimit, currentPlan, features. User isolation enforced.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_billing_graphql |
| _id | get_billing_graphql-001 |
| endpoint_path | graphql/GetBilling |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-19T12:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 1.x |
| introduced_in | 1.1.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limit | 50 requests/minute |
| rate_limited | True |


## Implementation

| Field | Value |
| --- | --- |
| service_file | contact360.io/api/app/graphql/modules/billing/queries.py |
| router_file | contact360/dashboard/src/services/graphql/billingService.ts |


## GraphQL operation

```graphql
query GetBilling { billing { billing { subscriptionPlan subscriptionStatus credits creditLimit currentPlan { id name } } } }
```

## Service / repository methods

### service_methods

- billing

### repository_methods

- get_user_profile

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /billing | Billing Page | billingService | useBillingPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `get_billing_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing Maturity.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `subscriptions` | READ | [subscriptions.sql](../database/tables/subscriptions.sql) |
| `plans` | READ | [plans.sql](../database/tables/plans.sql) |
| `user_profiles` | READ | [user_profiles.sql](../database/tables/user_profiles.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Payment Gateway**: Integrates with Stripe for subscription verification.

## Related endpoint graph

- **Inbound**: `Billing Page`.
- **Outbound**: `GetInvoices`, `Subscribe`.

<!-- AUTO:db-graph:end -->
---

*Generated from `get_billing_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
