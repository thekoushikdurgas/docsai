---
title: "POST /templates"
source_json: mutation_create_template_rest.json
generator: json_to_markdown_endpoints.py
---

# POST /templates

## Overview

Create a new email template. Uploads HTML body to S3 under key templates/{id}.html, inserts metadata row to templates table, invalidates in-memory cache. Template variables ({{.FirstName}}, {{.LastName}}, {{.Email}}, {{.UnsubscribeURL}}) supported via Go html/template.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_template_rest |
| _id | mutation_create_template_rest-001 |
| endpoint_path | POST /templates |
| method | POST |
| api_version | rest-v1 |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-03-24T00:00:00.000000+00:00 |
| updated_at | 2026-03-24T00:00:00.000000+00:00 |
| era_introduced | 0.x |


### era_milestones

| Era | Milestone |
| --- | --- |
| 0.x | Basic template create with S3 upload |
| 5.x | AI-generated flag, ai_prompt, ai_model stored with template |
| 10.x | Template analytics binding (open/click attribution) |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| auth_scheme | JWT Bearer (planned; currently missing middleware) |


## Implementation

| Field | Value |
| --- | --- |
| service | backend(dev)/email campaign |
| service_file | template/handlers.go:CreateTemplate |


## GraphQL operation

```graphql
mutation CreateCampaignTemplate($input: CreateCampaignTemplateInput!) { campaignTemplates { createTemplate(input: $input) { id name subject } } }
```

## Request body

| Field | Value |
| --- | --- |
| name | string (required) |
| subject | string (required, Go template syntax supported) |
| html_body | string (required, HTML with Go template variables) |


## Response

```json
{
  "201": {
    "id": "string",
    "name": "string",
    "subject": "string",
    "s3_key": "templates/{id}.html",
    "created_at": "RFC3339"
  },
  "400": "Bad request",
  "401": "Unauthorized"
}
```

## Data & infrastructure

### db_tables_write

- templates

### used_by_pages

- /campaigns/templates
- /campaigns/new

### frontend_page_bindings

| page_path | page_title | via_hook | via_service | usage_type | usage_context |
| --- | --- | --- | --- | --- | --- |
| /campaigns/templates | Campaign Templates | useTemplates | campaignTemplatesService | primary | form_submission |


## Additional metadata

```json
{
  "template_service_file": "template/service.go:UploadTemplate",
  "s3_write": [
    "templates/{id}.html"
  ]
}
```

## Inventory

- **page_count:** 2
- **Source:** `mutation_create_template_rest.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `Milestone` — Multi-era (0.x basic, 5.x AI-generated, 10.x analytics).

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `campaign_templates` | WRITE | [campaign_templates.sql](../database/tables/campaign_templates.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Email Campaign Backend** (`backend(dev)/email campaign`): Template creation via Go/Gin REST handler. HTML body uploaded to S3 under `templates/{id}.html`.
- **S3 Storage**: Template HTML body stored as S3 object.

## Related endpoint graph

- **Inbound**: `Campaign Templates Page` (Frontend form), `Campaign Wizard` (inline template creation).
- **Outbound**: `ListCampaignTemplates` (verify creation), `RenderTemplatePreview` (preview), `CreateCampaign` (template selection).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_template_rest.json`. Re-run `python json_to_markdown_endpoints.py`.*
