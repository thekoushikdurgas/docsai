---
title: "mailvetter — era matrix"
source_json: mailvetter_endpoint_era_matrix.json
generator: json_to_markdown_endpoints.py
---

# mailvetter

## Service metadata

| Field | Value |
| --- | --- |
| service | mailvetter |
| codebase | backend(dev)/mailvetter |
| runtime | Go + Gin + Redis + PostgreSQL |
| description | Deep verifier service with single and bulk validation, async jobs, and webhook callbacks. |


## HTTP / route inventory

| method | path | eras |
| --- | --- | --- |
| GET | /v1/health |  |
| POST | /v1/emails/validate |  |
| POST | /v1/emails/validate-bulk |  |
| GET | /v1/jobs/:job_id |  |
| GET | /v1/jobs/:job_id/results |  |


## era_by_era

### 0.x

- **focus:** service bootstrap and baseline contracts
**changes**

- health endpoint
- api+worker split
- jobs/results base schema


### 1.x

- **focus:** plan and ownership controls
**changes**

- rate limits by plan
- bulk/concurrency policy
- owner key lineage


### 2.x

- **focus:** email system primary delivery
**changes**

- v1 verify endpoints
- bulk job lifecycle
- score/status contract


### 3.x

- **focus:** contact/company data integration
**changes**

- optional contact/company linkage in result lineage


### 4.x

- **focus:** extension and SN provenance
**changes**

- source-tagged verification workflows


### 5.x

- **focus:** AI explainability
**changes**

- reason-code and factor exposure for AI consumers


### 6.x

- **focus:** reliability and scaling
**changes**

- distributed limiter
- idempotency
- retry/DLQ
- SLO visibility


### 7.x

- **focus:** deployment governance
**changes**

- migration discipline
- release gates
- legacy route deprecation governance


### 8.x

- **focus:** public/private API maturity
**changes**

- scoped API keys
- OpenAPI contract
- audit policy


### 9.x

- **focus:** ecosystem connectors
**changes**

- webhook replay
- partner adapter contract
- delivery logs


### 10.x

- **focus:** email campaign integration
**changes**

- campaign preflight verification
- recipient snapshot traceability

<!-- AUTO:db-graph:start -->

## Era alignment

See **era_focus** and route tables above — themes match [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints).

## Database & lineage

- Service: `mailvetter`
- Use the matching row in [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md#lambda--worker-services-by-path) and the lineage file linked there.

## Related

- [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)
- [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `mailvetter_endpoint_era_matrix.json`. Re-run `python json_to_markdown_endpoints.py`.*
