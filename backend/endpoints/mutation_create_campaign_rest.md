---
title: "POST /campaign"
source_json: mutation_create_campaign_rest.json
generator: json_to_markdown_endpoints.py
---

# POST /campaign

## Overview

Create and enqueue a new email campaign. Accepts template_id, name, audience_source (csv|segment|vql|sn_batch), optional segment_id, vql_query, filepath, and scheduled_at. Creates a campaigns row, enqueues campaign:send Asynq task on Redis. The worker resolves audience, inserts recipients, and dispatches 5 concurrent EmailWorker goroutines.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_create_campaign_rest |
| _id | mutation_create_campaign_rest-001 |
| endpoint_path | POST /campaign |
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
| 0.x | Basic campaign create with CSV filepath |
| 1.x | Auth middleware, credit guard, user_id/org_id attribution |
| 2.x | Rate limit, provider auth |
| 3.x | Audience source: segment/VQL via Connectra |
| 4.x | Audience source: sn_batch |
| 10.x | Scheduled send, A/B test flag |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | True |
| auth_scheme | JWT Bearer (planned; currently missing middleware) |
| rate_limit | planned (9.x entitlement guard) |


## Implementation

| Field | Value |
| --- | --- |
| service | backend(dev)/email campaign |
| service_file | api/handlers.go:CreateCampaign |
| task_file | tasks/campaign.go:CampaignPayload |
| worker_file | worker/campaign_worker.go:HandleCampaignTask |


## GraphQL operation

```graphql
mutation CreateCampaign($input: CreateCampaignInput!) { campaigns { createCampaign(input: $input) { id status } } }
```

## Request body

| Field | Value |
| --- | --- |
| template_id | string (UUID, required) |
| name | string (required) |
| filepath | string (CSV path, deprecated 3.x+) |
| audience_source | csv \\| segment \\| vql \\| sn_batch |
| segment_id | string (optional) |
| vql_query | string (optional) |
| scheduled_at | RFC3339 timestamp (optional) |


## Response

```json
{
  "201": {
    "campaign_id": "string",
    "status": "pending"
  },
  "400": "Bad request",
  "401": "Unauthorized (missing/invalid JWT)",
  "402": "Insufficient credits (1.x+)",
  "429": "Entitlement limit exceeded (9.x+)"
}
```

## Data & infrastructure

### db_tables_read

- templates

### db_tables_write

- campaigns

### redis_write

- Asynq task queue (campaign:send)

### used_by_pages

- /campaigns/new

### frontend_page_bindings

| page_path | page_title | via_hook | via_service | usage_type | usage_context |
| --- | --- | --- | --- | --- | --- |
| /campaigns/new | Campaign Wizard | useCampaignWizard | campaignsService | primary | form_submission |


## Inventory

- **page_count:** 1
- **Source:** `mutation_create_campaign_rest.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `10.x` — Email Campaign.

## Database tables → SQL snapshots

| Table | Operation | Lineage / Snapshot |
| --- | --- | --- |
| `campaigns` | WRITE | [campaigns.sql](../database/tables/campaigns.sql) |
| `campaign_sequences` | WRITE | [campaign_sequences.sql](../database/tables/campaign_sequences.sql) |
| `campaign_templates` | READ | [campaign_templates.sql](../database/tables/campaign_templates.sql) |

## Lineage & infrastructure docs

- [Contact360 API Lineage](../database/appointment360_data_lineage.md)

## Downstream services (cross-endpoint)

- **Email Campaign Backend** (`backend(dev)/email campaign`): Campaign creation via Go/Gin REST API with Redis + Asynq task queuing.

## Related endpoint graph

- **Inbound**: `Campaign Wizard Page` (Frontend form_submission).
- **Outbound**: `GetCampaign` (verify creation), `ScheduleCampaign` (activate), `EnrollContactsSequence` (add contacts).

<!-- AUTO:db-graph:end -->
---

*Generated from `mutation_create_campaign_rest.json`. Re-run `python json_to_markdown_endpoints.py`.*
