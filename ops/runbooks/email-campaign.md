# Email Campaign Runbook

## Health endpoints and expected healthy payload
- `GET /health`
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- `ADMIN_API_KEY`
- `DATABASE_URL`, `REDIS_ADDR`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_FROM`, `SMTP_USERNAME`, `SMTP_PASSWORD`
- `S3_TEMPLATE_BUCKET`
- Source: environment variables (`backend(dev)/email campaign/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: build and release API + worker
- Rollback: restore previous API/worker release and run health check

## Smoke checks to validate post-deploy behavior
- Health endpoint reports healthy
- Admin-key-protected campaign routes reject invalid/missing key
- Queue enqueue + worker send path executes for test campaign

## Escalation path and ownership
- Owner: Email campaign maintainers
- Escalate to messaging/platform owners for SMTP or queue failures
