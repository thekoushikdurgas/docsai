---
title: "graphql/GetInvoices"
source_json: query_get_invoices_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetInvoices

## Overview

Get invoice history for the current user with pagination. Returns invoices with amount, status, and creation date.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_invoices_graphql |
| _id | query_get_invoices_graphql-001 |
| endpoint_path | graphql/GetInvoices |
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

- getInvoices
- invoices

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /billing | Billing Page | billingService | useBillingPage | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_get_invoices_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `1.x` — Billing (Invoices).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `billing_history` | READ | [billing_history.sql](../database/tables/billing_history.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Audit**: Linked to Stripe invoice retrieval for PDF generation.

## Related endpoint graph

- **Inbound**: `Billing Page`.
- **Outbound**: `GetBilling` (context sync).

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_invoices_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
