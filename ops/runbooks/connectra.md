# Connectra Runbook

## Health endpoints and expected healthy payload
- `GET /health`
- Expected payload: `status=ok` (extend to include `service` and `version` where available)

## Required environment variables and secret sources
- `API_KEY`
- `ALLOWED_ORIGINS`
- `PG_DB_*`, `ELASTICSEARCH_*`, `S3_*`
- Source: environment variables (`contact360.io/sync/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: build and run current server binary/container
- Rollback: redeploy previous image/binary tag and restore previous env snapshot

## Smoke checks to validate post-deploy behavior
- `GET /health` returns success without auth
- Auth-protected routes reject missing/invalid `X-API-Key`
- Basic contact/company query route responds successfully with valid key

## Escalation path and ownership
- Owner: Connectra backend maintainers
- Escalate to search/data platform owners for index/query failures
