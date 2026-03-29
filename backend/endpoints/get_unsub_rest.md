---
title: "GET /unsub"
source_json: get_unsub_rest.json
generator: json_to_markdown_endpoints.py
---

# GET /unsub

## Overview

Process unsubscribe request. Accepts JWT token as query parameter (?token=...). Validates JWT (HS256, 30-day expiry), extracts email and campaign_id claims, inserts email into suppression_list, updates recipients.status to 'unsubscribed', returns HTML confirmation page.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | get_unsub_rest |
| _id | get_unsub_rest-001 |
| endpoint_path | GET /unsub |
| method | GET |
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
| 0.x | JWT unsubscribe token generated per recipient in worker |
| 2.x | Bounce/complaint suppression also feeds same suppression_list |
| 9.x | GDPR compliance: unsubscribe must be honoured within 10 business days |


## Security & limits

| Field | Value |
| --- | --- |
| auth_required | False |
| auth_scheme | JWT in query parameter ?token=... |


## Implementation

| Field | Value |
| --- | --- |
| service | backend(dev)/email campaign |
| service_file | api/handlers.go:Unsubscribe |


## Response

```json
{
  "200": "HTML unsubscribe confirmation page",
  "401": "Invalid or expired token"
}
```

## Data & infrastructure

### db_tables_read

- recipients (GetUnsubToken — currently buggy: uses DB.Exec instead of DB.Get)

### db_tables_write

- suppression_list (insert)
- recipients (update status=unsubscribed)

### used_by_pages

- Email footer link (not a dashboard page)

### frontend_page_bindings

| page_path | via_component | usage_type | usage_context |
| --- | --- | --- | --- |
| Email body (link in sent email) | UnsubscribeLink in email body | external_link | email_footer |


## Additional metadata

```json
{
  "token_service_file": "utils/token.go:ParseUnsubToken",
  "query_params": {
    "token": "string (JWT, required)"
  },
  "known_bugs": [
    "GetUnsubToken uses DB.Exec not DB.Get \u2014 token is never retrieved correctly"
  ]
}
```

## Inventory

- **page_count:** 0
- **Source:** `get_unsub_rest.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `Milestone` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

### Read
- `recipients` — *no `tables/recipients.sql` snapshot in docs; see service lineage below*

### Write
- `suppression_list` — *no `tables/suppression_list.sql` snapshot in docs; see service lineage below*
- `recipients` — *no `tables/recipients.sql` snapshot in docs; see service lineage below*

## Lineage & infrastructure docs

- [Appointment360 lineage](../database/appointment360_data_lineage.md) (default GraphQL owner)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `get_unsub_rest.json`. Re-run `python json_to_markdown_endpoints.py`.*
