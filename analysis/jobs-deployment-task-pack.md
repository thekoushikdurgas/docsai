# jobs task pack (`7.x`)

This pack decomposes `contact360.io/jobs` work into Contract, Service, Surface, Data, and Ops tracks.

## Contract track

- [ ] Define per-role/per-service access model beyond shared API key.
- [ ] Tie role model to `docs/7. Contact360 deployment/rbac-authz.md` and gateway role semantics.
- [ ] Define deployment-time audit evidence contract for job lifecycle actions.

## Service track

- [ ] Add role-aware authorization path and key rotation support.
- [ ] Implement retention policy hooks and deletion governance controls.

## Surface track

- [ ] Document role-gated admin controls and retention/audit panels.
- [ ] Document deployment readiness checks visible in ops UI.

## Data track

- [ ] Use `job_events` as primary deployment/audit trail evidence.
- [ ] Document retention and legal-hold expectations for job timelines.

## Ops track

- [ ] Add CI/CD gates for processor registry and endpoint parity tests.
- [ ] Add deployment runbook for auth, retention, and queue health checks.

