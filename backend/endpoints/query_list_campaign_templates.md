---
title: "graphql/listCampaignTemplates"
source_json: query_list_campaign_templates.json
generator: json_to_markdown_endpoints.py
---

# graphql/listCampaignTemplates

## Overview

listCampaignTemplates operation for backend docs expansion.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | query_list_campaign_templates |
| _id | query_list_campaign_templates-001 |
| endpoint_path | graphql/listCampaignTemplates |
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
| service_file | contact360.io/api/app/graphql/modules/campaign_templates/queries.py |
| router_file | contact360/dashboard/src/services/graphql/templateService.ts |


## GraphQL operation

```graphql
query listCampaignTemplates
```

## Service / repository methods

### service_methods

- listCampaignTemplates

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /campaign-templates | Campaign Templates Page | templateService | useCampaignTemplates | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `query_list_campaign_templates.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x-10.x` — Campaign Automation (Email).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `email_templates` | READ | [email_templates.sql](../database/tables/email_templates.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Email Campaign Services](../database/emailcampaign_data_lineage.md)

## Downstream services (cross-endpoint)

- **Email APIs**: Template synchronization via `lambda/emailapis` or `lambda/emailapigo`.

## Related endpoint graph

- **Inbound**: `Campaign Templates Page`.
- **Outbound**: `SaveCampaignTemplate`, `RenderTemplatePreview`.

<!-- AUTO:db-graph:end -->
---

*Generated from `query_list_campaign_templates.json`. Re-run `python json_to_markdown_endpoints.py`.*
