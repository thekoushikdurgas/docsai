# Mailvetter — 7.x Deployment Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `7.x` — Deployment and governance hardening

## Contract track

- [ ] Versioning policy: `/v1` remains stable; legacy routes officially deprecated.
- [ ] Release checklist contract for schema and API compatibility.
- [ ] Define audit event contract for verification outcomes and privileged override actions.
- [ ] Define retention/deletion policy contract for verification evidence artifacts.

## Service track

- [ ] Separate schema migrations from app startup execution.
- [ ] Add startup readiness checks for Redis/Postgres dependencies.
- [ ] Ensure worker drain logic without message loss.
- [ ] Emit audit events to `logs.api` for verifier write/update/reprocess flows.

## Surface track

- [ ] Disable legacy static UI in production unless explicit flag is enabled.

## Data track

- [ ] Backup/restore and retention runbooks for `jobs` and `results`.
- [ ] Add migration rollback scripts and test evidence.
- [ ] Validate retention policy execution and GDPR erasure cascade for verifier artifacts.

## Ops track

- [ ] CI gates: lint, unit, integration, contract tests.
- [ ] CD gates: health checks and canary traffic checks.
- [ ] Add secrets isolation (`API_SECRET_KEY` vs `WEBHOOK_SECRET_KEY`).
- [ ] Add secret rotation runbook and quarterly validation drill for verifier credentials.
