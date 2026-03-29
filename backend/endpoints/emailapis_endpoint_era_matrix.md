---
title: "lambda/emailapis + lambda/emailapigo — era matrix"
source_json: emailapis_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# lambda/emailapis + lambda/emailapigo

## Service metadata

| Field | Value |
| --- | --- |
| service | lambda/emailapis + lambda/emailapigo |
| base_path | / |


## HTTP / route inventory

| method | path | eras |
| --- | --- | --- |
| POST | /email/finder/ | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /email/finder/bulk | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /email/single/verifier/ | 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /email/bulk/verifier/ | 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /email-patterns/add | 2.x, 3.x, 5.x, 6.x, 8.x, 9.x, 10.x |
| POST | /email-patterns/add/bulk | 2.x, 3.x, 5.x, 6.x, 8.x, 9.x, 10.x |
| POST | /web/web-search | 2.x, 3.x, 4.x, 5.x, 6.x, 8.x, 9.x, 10.x |
| GET | /health | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | / | 0.x, 7.x |


## era_focus

| Era | Focus |
| --- | --- |
| 0.x | runtime bootstrap and contract baseline |
| 1.x | credit-aware verification/search behavior |
| 2.x | email system maturity and bulk correctness |
| 3.x | contact/company enrichment linkage |
| 4.x | extension/sales navigator provenance |
| 5.x | AI-assisted email workflow support |
| 6.x | reliability, scaling, and failover hardening |
| 7.x | deployment and governance gates |
| 8.x | public/private API contract readiness |
| 9.x | ecosystem integration and tenant controls |
| 10.x | campaign deliverability and compliance evidence |


## references

- docs/codebases/emailapis-codebase-analysis.md
- docs/backend/apis/15_EMAIL_MODULE.md
- lambda/emailapis/app/api/v1/router.py
- lambda/emailapigo/internal/api/router.go

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `lambda/emailapis + lambda/emailapigo`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `emailapis_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
