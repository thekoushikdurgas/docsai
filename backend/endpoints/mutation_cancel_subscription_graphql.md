---
title: "graphql/CancelSubscription"
source_json: mutation_cancel_subscription_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/CancelSubscription

## Overview

Cancel the current user subscription. No input required. Sets subscriptionStatus to 'cancelled', subscription remains active until subscriptionEndsAt date. Returns CancelSubscriptionResponse with success (Boolean), message (String), subscriptionEndsAt (DateTime, when access will end). Raises BadRequestError (400) if no active subscription exists. Activity logged (non-blocking).

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_cancel_subscription_graphql |
| _id | mutation_cancel_subscription_graphql-001 |
| endpoint_path | graphql/CancelSubscription |
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
mutation CancelSubscription { billing { cancelSubscription { success message subscriptionEndsAt } } }
```

## Service / repository methods

### service_methods

- cancelSubscription

### repository_methods

- update_user_subscription

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /billing | Billing Page | billingService | useBilling | secondary | data_mutation | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_cancel_subscription_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation & Pre-Product Stabilization (Billing bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `user_profiles` | READ / WRITE | [user_profiles.sql](../database/tables/user_profiles.sql) |
| `user_activities` | WRITE | [user_activities.sql](../database/tables/user_activities.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Updates `subscriptionStatus` to 'cancelled' and sets `subscriptionEndsAt` on `user_profiles` via UserProfileRepository.
- **Activity Pipeline**: Async activity logging for billing audit trail.

## Related endpoint graph

- **Inbound**: `Billing Page` (Frontend), `Subscribe` (active subscription required).
- **Outbound**: `GetBilling` (verify status change), `GetUsage` (credit freeze check).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_cancel_subscription_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
