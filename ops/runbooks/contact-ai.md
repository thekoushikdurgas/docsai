# Contact AI Runbook

## Health endpoints and expected healthy payload
- `GET /health` (or `/api/v1/health` per deployment mode)
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- Model/provider API keys
- Database connection and auth settings
- Source: environment variables (`backend(dev)/contact.ai/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: build and release current Contact AI service artifact
- Rollback: restore previous release and restart workers/API

## Smoke checks to validate post-deploy behavior
- Health endpoint succeeds
- Basic chat/create message call succeeds with valid auth
- Utility endpoint call returns expected schema

## Escalation path and ownership
- Owner: Contact AI maintainers
- Escalate to AI platform owners for model/provider incidents
