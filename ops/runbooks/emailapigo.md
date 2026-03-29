# Email API Go Worker Runbook

## Health endpoints and expected healthy payload
- Worker/process health endpoint (or process heartbeat probe)
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- Worker concurrency and queue settings
- Provider and storage integration credentials
- Source: environment variables (`lambda/emailapigo/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: release updated Go worker artifact
- Rollback: restore previous worker artifact and restart

## Smoke checks to validate post-deploy behavior
- Health/heartbeat probe reports healthy
- One sample bulk batch starts and reaches terminal state
- Failure path logs include correlation identifiers

## Escalation path and ownership
- Owner: Email API Go maintainers
- Escalate to async/queue owners for throughput or stuck-job issues
