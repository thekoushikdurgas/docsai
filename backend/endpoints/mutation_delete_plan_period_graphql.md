---
title: "graphql/DeletePlanPeriod"
source_json: mutation_delete_plan_period_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/DeletePlanPeriod

## Overview

Delete a subscription plan period. Accepts tier (String!, required) and period (String!, required - monthly, quarterly, yearly). Returns object with message, tier, and period. SuperAdmin only.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_delete_plan_period_graphql |
| _id | mutation_delete_plan_period_graphql-001 |
| endpoint_path | graphql/DeletePlanPeriod |
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

- deletePlanPeriod

## Inventory

- **page_count:** 0
- **Source:** `mutation_delete_plan_period_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — Foundation & Pre-Product Stabilization (Billing bootstrap).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `subscription_plans` | READ | [subscription_plans.sql](../database/tables/subscription_plans.sql) |
| `subscription_plan_periods` | DELETE | [subscription_plan_periods.sql](../database/tables/subscription_plan_periods.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Gateway DB**: Direct delete from `subscription_plan_periods` via BillingRepository. No downstream service calls.

## Related endpoint graph

- **Inbound**: `Admin Billing Page` (Frontend SuperAdmin).
- **Outbound**: `GetPlans` (verify deletion), `GetAdminPlans` (admin listing).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_delete_plan_period_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
