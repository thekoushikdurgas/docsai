---
title: "graphql/GetAdminPlans"
source_json: query_get_admin_plans_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetAdminPlans

## Overview

Get all subscription plans for admin management. Accepts optional includeInactive (Boolean, default: false). Returns array of SubscriptionPlan with tier, name, category (STARTER, PROFESSIONAL, BUSINESS, ENTERPRISE), and periods (monthly, quarterly, yearly) each with period, credits, ratePerCredit, price, and savings (amount, percentage). SuperAdmin only. Tries to get plans from database first, falls back to hardcoded SUBSCRIPTION_PLANS if database fails.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_admin_plans_graphql |
| _id | query_get_admin_plans_graphql-001 |
| endpoint_path | graphql/GetAdminPlans |
| method | QUERY |
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
| service_file | contact360.io/api/app/graphql/modules/billing/queries.py |
| router_file | contact360/dashboard/src/services/graphql/billingService.ts |


## Service / repository methods

### service_methods

- getAdminPlans
- plans

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /billing | Billing Page | billingService | useBilling | conditional | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_admin_plans_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing Maturity.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `plans` | READ / WRITE | [plans.sql](../database/tables/plans.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Admin Control**: Allows SuperAdmins to manage tiers and pricing.

## Related endpoint graph

- **Inbound**: `Admin Plans Page`.
- **Outbound**: `CreatePlan`, `UpdatePlan`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_admin_plans_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
