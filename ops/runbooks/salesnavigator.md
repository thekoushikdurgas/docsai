# SalesNavigator Runbook

## Health endpoints and expected healthy payload
- `GET /v1/health`
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- `API_KEY`
- `ALLOWED_ORIGINS`
- Rate-limit settings
- Source: environment variables (`backend(dev)/salesnavigator/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: service deploy for current FastAPI/Lambda packaging mode
- Rollback: restore previous deployment artifact and env snapshot

## Smoke checks to validate post-deploy behavior
- `/v1/health` responds healthy
- Auth-protected scrape/save route rejects invalid key
- Valid keyed request to save route succeeds

## Escalation path and ownership
- Owner: SalesNavigator backend maintainers
- Escalate to extension/channel owners for ingestion path failures
