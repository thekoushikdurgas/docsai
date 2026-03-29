# Jobs Runbook

## Health endpoints and expected healthy payload
- `GET /health`
- `GET /health/live`
- `GET /health/ready`
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- `DATABASE_URL`
- `KAFKA_*`
- `X_API_KEY` / jobs API key setting
- Source: environment variables (`contact360.io/jobs/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: start API + scheduler + workers with current release
- Rollback: stop new workers, restore previous release binaries/images, restart in order

## Smoke checks to validate post-deploy behavior
- Health endpoints are green
- `POST /api/v1/jobs` succeeds with valid key
- Timeline/status endpoints return expected lifecycle states

## Escalation path and ownership
- Owner: Jobs service maintainers
- Escalate to queue/platform owners for lag/stuck-processing incidents
