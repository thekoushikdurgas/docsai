# Email APIs Runbook

## Health endpoints and expected healthy payload
- Service health endpoint (`/health` where exposed)
- Expected payload fields: `status`, `service`, `version`

## Required environment variables and secret sources
- Provider credentials/API keys
- Upstream service URLs and timeout settings
- Source: environment variables (`lambda/emailapis/.env`)

## Deploy command(s) and rollback command(s)
- Deploy: lambda deploy for `emailapis`
- Rollback: restore previous lambda release

## Smoke checks to validate post-deploy behavior
- Health check succeeds
- Single finder/verifier request succeeds with valid auth
- Error handling contract remains stable on provider failures

## Escalation path and ownership
- Owner: Email APIs maintainers
- Escalate to provider-integration owners for upstream outages
