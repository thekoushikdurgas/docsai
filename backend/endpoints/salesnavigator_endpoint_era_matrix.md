---
title: "backend(dev)/salesnavigator — era matrix"
source_json: salesnavigator_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# backend(dev)/salesnavigator

## Service metadata

| Field | Value |
| --- | --- |
| service | backend(dev)/salesnavigator |
| base_path | /v1 |


## HTTP / route inventory

| method | path | eras |
| --- | --- | --- |
| GET | / | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| GET | /v1/health | 0.x, 1.x, 2.x, 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /v1/scrape | 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /v1/save-profiles | 3.x, 4.x, 5.x, 6.x, 7.x, 8.x, 9.x, 10.x |
| POST | /v1/scrape-html-with-fetch |  |


## era_focus

| Era | Focus |
| --- | --- |
| 0.x | Scaffold — health only |
| 1.x | Actor context headers stub |
| 2.x | Email field validation |
| 3.x | save-profiles active; full field mapping |
| 4.x | PRIMARY ERA — scrape + save, full extension UX |
| 5.x | AI-ready field quality |
| 6.x | Rate limiting, idempotency, CORS hardening |
| 7.x | Per-tenant keys, audit events, GDPR |
| 8.x | Versioned path, rate-limit headers, usage tracking |
| 9.x | Connector adapter, webhook delivery |
| 10.x | Campaign audience provenance |


## known_gaps

- POST /v1/scrape-html-with-fetch documented but not implemented
- README.md incorrectly states scraping is removed
- Single global API_KEY — no per-tenant scoping until 7.x
- No rate limiting implemented until 6.x
- CORS wide-open (*) until 6.x
- No X-Request-ID correlation header until 6.x
- PLACEHOLDER_VALUE in linkedin_url for many SN contacts
- employees_count, industries, annual_revenue always null for SN companies

## references

- docs/codebases/salesnavigator-codebase-analysis.md
- docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md
- docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md
- docs/backend/database/salesnavigator_data_lineage.md
- backend(dev)/salesnavigator/app/api/v1/endpoints/scrape.py
- backend(dev)/salesnavigator/docs/api.md

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `backend(dev)/salesnavigator`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `salesnavigator_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
