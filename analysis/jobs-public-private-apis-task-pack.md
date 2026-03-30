# Jobs Public/Private APIs Task Pack (8.x)

## Contract
- versioned `/api/v1/jobs/` contract
- callback + webhook lifecycle schema

## Service
- partner-safe submission validation
- scoped `X-API-Key` credentials
- callback retry with DLQ

## Data
- external callback lineage in `job_events`
- API version trace in `job_response`

## Ops
- backward compatibility gate per release
- deprecation and replay runbook
