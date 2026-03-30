---
title: "lambda/logs.api — era matrix"
source_json: logsapi_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# lambda/logs.api

## Service metadata

| Field | Value |
| --- | --- |
| service | lambda/logs.api |

## EC2 Go satellite

| Field | Value |
| --- | --- |
| implementation | `EC2/log.server/` (`contact360.io/logsapi`) |
| route detail | [EC2_GO_SATELLITE_ROUTES.md#ec2-logsapi](EC2_GO_SATELLITE_ROUTES.md#ec2-logsapi) |

## HTTP / route inventory

| method | path | eras |
| --- | --- | --- |
| POST | /logs | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /logs/batch | 2.x, 6.x, 8.x, 10.x |
| GET | /logs | 1.x, 2.x, 3.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /logs/search | 3.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /logs/{log_id} | 1.x, 2.x, 3.x, 7.x, 8.x, 10.x |
| PUT | /logs/{log_id} | 7.x, 8.x |
| DELETE | /logs/{log_id} | 7.x, 8.x, 10.x |
| POST | /logs/delete | 7.x, 8.x, 9.x, 10.x |
| DELETE | /logs | 7.x, 8.x, 9.x, 10.x |
| GET | /health | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /health/info | 0.x, 6.x, 7.x |


## known_gaps

- LOG-0.2: response-envelope parity tests required
- LOG-0.3: idempotency for POST ingest endpoints
- LOG-1.x: scoped keys and usage quotas

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `lambda/logs.api`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `logsapi_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
