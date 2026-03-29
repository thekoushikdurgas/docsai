---
title: "graphql/saveTemplate"
source_json: mutation_save_campaign_template.json
generator: json_to_markdown_endpoints.py
---

# graphql/saveTemplate

## Overview

saveTemplate operation for backend docs expansion.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_save_campaign_template |
| _id | mutation_save_campaign_template-001 |
| endpoint_path | graphql/saveTemplate |
| method | MUTATION |
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
| service_file | contact360.io/api/app/graphql/modules/campaign_templates/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/templateService.ts |


## GraphQL operation

```graphql
mutation saveTemplate
```

## Service / repository methods

### service_methods

- saveTemplate

### used_by_pages

| page_path | page_title | via_service | via_hook | usage_type | usage_context | updated_at |
| --- | --- | --- | --- | --- | --- | --- |
| /campaign-templates | Campaign Templates Page | templateService | useCampaignTemplates | primary | data_fetching | 2026-03-24T00:00:00.000000+00:00 |


## Inventory

- **page_count:** 1
- **Source:** `mutation_save_campaign_template.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `9.x-10.x` — Campaign Automation (Email).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `email_templates` | WRITE | [email_templates.sql](../database/tables/email_templates.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)
- [Email Campaign Services](../database/emailcampaign_data_lineage.md)

## Downstream services (cross-endpoint)

- **Email APIs**: Template rendering via `lambda/emailapis` or `lambda/emailapigo`.

## Related endpoint graph

- **Inbound**: `Campaign Templates Page`.
- **Outbound**: `CreateCampaign`, `RenderTemplatePreview`.

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_save_campaign_template.json`. Re-run `python json_to_markdown_endpoints.py`.*
