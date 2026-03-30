---
title: "graphql/listCampaigns"
source_json: query_list_campaigns.json
generator: json_to_markdown_endpoints.py
---

# graphql/listCampaigns

## Overview

listCampaigns operation for backend docs expansion.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_campaigns |
| _id | query_list_campaigns-001 |
| endpoint_path | graphql/listCampaigns |
| method | QUERY |
| api_version | graphql |
| endpoint_state | planned |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-03-24T00:00:00.000000+00:00 |
| updated_at | 2026-03-29T00:00:00.000000+00:00 |
| era | 9.x-10.x |
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
| service_file | contact360.io/api/app/graphql/modules/campaigns/queries.py |
| router_file | contact360/dashboard/src/services/graphql/campaignService.ts |


## GraphQL operation

```graphql
query listCampaigns
```

## Service / repository methods

### service_methods

- listCampaigns

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /campaigns | Campaigns Page | campaignService | useCampaigns | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_list_campaigns.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x-10.x` — Campaign Automation (Email).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `email_campaigns` | READ | [email_campaigns.sql](../database/tables/email_campaigns.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Email Campaign Services](../database/emailcampaign_data_lineage.md)

## Downstream services (cross-endpoint)

- **Email APIs**: List metadata from `lambda/emailapis` or `lambda/emailapigo`.

## Related endpoint graph

- **Inbound**: `Campaigns Page`.
- **Outbound**: `GetCampaign`, `CreateCampaign`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_campaigns.json`. Re-run `python json_to_markdown_endpoints.py`.*
