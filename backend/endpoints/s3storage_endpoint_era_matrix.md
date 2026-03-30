---
title: "s3storage — era matrix"
source_json: s3storage_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# s3storage

## Service metadata

| Field | Value |
| --- | --- |
| service | s3storage |
| base_path | /api/v1 |

## EC2 Go satellite

| Field | Value |
| --- | --- |
| implementation | `EC2/s3storage.server/` (`contact360.io/s3storage`) |
| route detail | [EC2_GO_SATELLITE_ROUTES.md#ec2-s3storage](EC2_GO_SATELLITE_ROUTES.md#ec2-s3storage) |

## era_focus

| Era | Focus |
| --- | --- |
| 0.x | bootstrap contract and key taxonomy |
| 1.x | user and billing artifact policy |
| 2.x | multipart durability and metadata freshness |
| 3.x | ingestion/export lineage quality |
| 4.x | extension and sales navigator provenance |
| 5.x | AI artifact governance |
| 6.x | idempotency, reconciliation, SLO |
| 7.x | authz and retention/deletion governance |
| 8.x | versioned endpoint and event contracts |
| 9.x | entitlements and quota controls |
| 10.x | campaign compliance and reproducibility artifacts |


## known_gaps

- S3S-0.1: auth enforcement not complete across all non-health paths
- S3S-0.3: multipart session state is in-memory and non-durable
- S3S-0.5: idempotency contract required on upload initiate/complete paths

## references

- docs/codebases/s3storage-codebase-analysis.md
- docs/backend/apis/S3STORAGE_ERA_TASK_PACKS.md
- lambda/s3storage/docs/API.md

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `s3storage`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `s3storage_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
