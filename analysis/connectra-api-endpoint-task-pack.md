# Connectra API Endpoint Task Pack (8.x)

## Contract
- versioned REST contract for partner/private usage
- partner key scope model by endpoint family
- webhook-ready job event envelope for async handoffs

## Service
- per-tenant rate limiting and `X-RateLimit-*` headers
- persistent job queue backing for ingestion/search jobs
- ES-PG reconciliation strategy with consistency checks

## Data
- API usage counters keyed by partner key + endpoint + version
- compatibility evidence artifacts for each released contract

## Ops
- deprecation playbook for legacy route retirement
- compatibility regression suite in CI
- incident triage runbook for queue lag and mismatch incidents
