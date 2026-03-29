# ResumeAI Runbook

## Health endpoints and expected healthy payload
- `GET /health` (or equivalent probe route)
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- ResumeAI provider credentials and service config
- Database/storage settings if enabled
- Source: environment variables (`backend(dev)/resumeai/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: release ResumeAI service artifact
- Rollback: restore previous release and validate health

## Smoke checks to validate post-deploy behavior
- Health endpoint responds healthy
- One representative resume parse/analyze request succeeds
- Error payload remains contract-compatible

## Escalation path and ownership
- Owner: ResumeAI maintainers
- Escalate to AI workflow owners for service degradation
