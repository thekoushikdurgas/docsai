# Connectra deployment task pack (`7.x`)

## Contract track

- [ ] Freeze RBAC and API key scope for write and export endpoints.
- [ ] Define tenant-safe request/response and failure semantics for privileged paths.

## Service track

- [ ] Enforce privileged path checks for `batch-upsert`, job creation, and filter mutations.
- [ ] Ensure handler-level authz mirrors gateway role checks (no role bypass).

## Surface track

- [ ] Document role-gated admin/app controls tied to Connectra privileged actions.
- [ ] Validate tenant-safe user messaging for deny/error/retry flows.

## Data track

- [ ] Record audit events for sensitive writes and mapping/schema changes.
- [ ] Validate lineage fields: actor, tenant, trace id, and action outcome.

## Ops track

- [ ] Validate tenant isolation on all query/write paths through gateway + Connectra.
- [ ] Publish release gate evidence: security checklist, authz tests, and retention/audit proof.

