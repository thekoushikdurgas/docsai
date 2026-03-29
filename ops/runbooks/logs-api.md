# Logs API Runbook

## Health endpoints and expected healthy payload
- `GET /health` (or service-specific root probe)
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- Logs API key and storage settings
- S3/CSV persistence configuration
- Source: environment variables (`lambda/logs.api/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: lambda build/deploy pipeline for `logs.api`
- Rollback: redeploy previous known-good lambda artifact

## Smoke checks to validate post-deploy behavior
- Health check succeeds
- Log ingest endpoint accepts valid payload with valid key
- Invalid key requests are rejected

## Escalation path and ownership
- Owner: Logging service maintainers
- Escalate to observability/platform owners for ingestion backlog or storage errors
