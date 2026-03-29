---
title: "graphql/GetMarketingPage"
source_json: query_get_marketing_page_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/GetMarketingPage

## Overview

Get marketing page content by pageId. Returns page metadata, hero section, sections, and access control. Falls back to static content if API fails.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_get_marketing_page_graphql |
| _id | query_get_marketing_page_graphql-001 |
| endpoint_path | graphql/GetMarketingPage |
| method | QUERY |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-20T00:00:00.000000+00:00 |
| era | 9.x |
| introduced_in | 9.0.0 |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| rbac_roles | user |
| rate_limited | False |


## Implementation

| Field | Value |
| --- | --- |
| service_file | appointment360/app/graphql/modules/marketing/queries.py |
| router_file | contact360/dashboard/src/services/graphql/marketingService.ts |


## Service / repository methods

### service_methods

- getMarketingPage
- fetchMarketingPage

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /about | About Page | marketingService | useMarketingPage | conditional | data_fetching | 2025-01-27T12:00:00.000000+00:00 |
| /admin/marketing/[pageId] | Admin Marketing Pageid Page | marketingService | useMarketingPageEditor | primary | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /api | Api Docs Page | marketingService | useMarketingPage | conditional | data_fetching | 2025-01-27T12:00:00.000000+00:00 |
| /careers | Careers Page | marketingService | useMarketingPage | conditional | data_fetching | 2025-01-27T12:00:00.000000+00:00 |
| /chrome-extension | Chrome Extension Page | marketingService | useMarketingPage | conditional | data_fetching | 2025-01-27T12:00:00.000000+00:00 |
| /integrations | Integrations Page | marketingService | useMarketingPage | conditional | data_fetching | 2025-01-27T12:00:00.000000+00:00 |
| /privacy | Privacy Page | marketingService | useMarketingPage | conditional | data_fetching | 2025-01-27T12:00:00.000000+00:00 |
| /products/ai-email-writer | Products Ai Email Writer Page | marketingService | useMarketingPage | conditional | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /products/cfo-email-list | Products Cfo Email List Page | marketingService | useMarketingPage | conditional | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /products/chrome-extension | Products Chrome Extension Page | marketingService | useMarketingPage | conditional | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /products/email-finder | Products Email Finder Page | marketingService | useMarketingPage | conditional | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /products/email-verifier | Products Email Verifier Page | marketingService | useMarketingPage | conditional | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /products/prospect-finder | Products Prospect Finder Page | marketingService | useMarketingPage | conditional | data_fetching | 2026-01-20T00:00:00.000000+00:00 |
| /terms | Terms Page | marketingService | useMarketingPage | conditional | data_fetching | 2025-01-27T12:00:00.000000+00:00 |


## Inventory

- **page_count:** 14
- **Source:** `query_get_marketing_page_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

- *No `db_tables_read` / `db_tables_write` in this spec — gateway-only or metadata TBD; see lineage.*

## Lineage & infrastructure docs

- [Appointment360 (gateway DB)](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `query_get_marketing_page_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
