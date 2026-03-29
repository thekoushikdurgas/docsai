# logs.api task pack (`7.x`)

This pack decomposes `lambda/logs.api` work into Contract, Service, Surface, Data, and Ops tracks.

## Contract track

- [ ] Define and freeze era `7.x` logging schema additions and compatibility notes.
- [ ] Update endpoint/reference matrix in `docs/backend/endpoints/logsapi_endpoint_era_matrix.json`.

## Service track

- [ ] Implement and validate service behavior for era `7.x` event sources and query expectations.
- [ ] Verify auth, error envelope, and health behavior for consuming services.

## Surface track

- [ ] Define concrete deployment-governance surfaces: `/admin/deployments`, audit/event explorer, retention report export.
- [ ] Document role-gated UI states for query/filter/export, including loading/error/retry states.

## Data track

- [ ] Document S3 CSV storage and lineage impact for era `7.x`.
- [ ] Record retention, trace ids, and query-window expectations.

## Ops track

- [ ] Add observability checks and release validation evidence for era `7.x`.
- [ ] Capture rollback and incident-runbook notes for logging-impacting releases.

