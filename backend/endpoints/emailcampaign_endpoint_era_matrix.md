---
title: "email campaign — era matrix"
source_json: emailcampaign_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# email campaign

## Service metadata

| Field | Value |
| --- | --- |
| service | email campaign |
| runtime | Go 1.24, Gin, Asynq, Redis, PostgreSQL, AWS S3 |
| description | Campaign delivery engine — bulk email send, template management, unsubscribe/suppression, IMAP inbox, and async worker via Asynq/Redis. |
| data_lineage_reference | docs/backend/database/emailcampaign_data_lineage.md |

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `email campaign`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `emailcampaign_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
