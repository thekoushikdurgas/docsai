---
title: "contact360.io/admin — era matrix"
source_json: admin_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# contact360.io/admin

## Service metadata

| Field | Value |
| --- | --- |
| service | contact360.io/admin |
| runtime | Django + DRF |


## route_groups

### public

- GET /
- GET /login
- POST /login
- GET /logout

### admin_or_super_admin

- GET /admin/users
- GET /admin/user/{id}/history
- GET /admin/statistics

### super_admin

- GET /admin/billing/payments
- POST /admin/billing/payments/{id}/approve
- POST /admin/billing/payments/{id}/decline
- GET /admin/logs
- POST /admin/logs/bulk-delete
- GET /admin/jobs
- POST /admin/jobs/{id}/retry
- GET /admin/storage/files
- DELETE /admin/storage/files

### api_v1

- GET /api/v1/health
- GET /api/v1/health/database
- GET /api/v1/health/cache
- GET /api/v1/health/storage

## known_gaps

- ADM-8.1 explicit public/private API split and versioning
- ADM-1.1 resolved: billing payment review actions (`POST /admin/billing/payments/{id}/approve|decline`) now emit actor/reason/status transition/timestamp/request-id audit evidence

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `contact360.io/admin`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `admin_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
