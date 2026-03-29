# Appointment360 Runbook

## Health endpoints and expected healthy payload
- `GET /health`
- `GET /health/db`
- `GET /health/logging`
- Expected core payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- `SECRET_KEY`, `DATABASE_URL`, `POSTGRES_*`
- `LAMBDA_*_API_URL`, `LAMBDA_*_API_KEY`
- Source: environment variables (`contact360.io/api/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: `sam build && sam deploy`
- Rollback: redeploy previous known-good artifact/template revision

## Smoke checks to validate post-deploy behavior
- `GET /health` returns `status=healthy`
- GraphQL introspection disabled/enabled based on environment policy
- Representative query + mutation succeeds

## Escalation path and ownership
- Owner: Appointment360 backend maintainers
- Escalate to platform/on-call if health or GraphQL availability degrades
