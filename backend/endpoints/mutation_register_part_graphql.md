---
title: "graphql/RegisterPart"
source_json: mutation_register_part_graphql.json
generator: json_to_markdown_endpoints.py
---

# graphql/RegisterPart

## Overview

Register a successfully uploaded part with its ETag. Accepts RegisterPartInput with uploadId (required, String), partNumber (required, Int, 1-based index), etag (required, String, returned by S3 after part upload). Returns RegisterPartResponse with status (String: 'registered'), partNumber (Int). Stores ETag in session for CompleteUpload. Required before completing upload. Raises NotFoundError (404) if upload session not found. Raises ValidationError (422) if partNumber < 1.

## Identity

| Field | Value |
| --- | --- |
| endpoint_id | mutation_register_part_graphql |
| _id | mutation_register_part_graphql-001 |
| endpoint_path | graphql/RegisterPart |
| method | MUTATION |
| api_version | graphql |
| endpoint_state | development |


## Lifecycle

| Field | Value |
| --- | --- |
| created_at | 2026-01-20T00:00:00.000000+00:00 |
| updated_at | 2026-01-21T00:00:00.000000+00:00 |
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
| service_file | appointment360/app/graphql/modules/upload/mutations.py |
| router_file | contact360/dashboard/src/services/graphql/uploadService.ts |


## GraphQL operation

```graphql
mutation RegisterPart($input: RegisterPartInput!) { upload { registerPart(input: $input) { status partNumber } } }
```

## Service / repository methods

### service_methods

- registerPart

## Inventory

- **page_count:** 0
- **Source:** `mutation_register_part_graphql.json`

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `0.x` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

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

*Generated from `mutation_register_part_graphql.json`. Re-run `python json_to_markdown_endpoints.py`.*
