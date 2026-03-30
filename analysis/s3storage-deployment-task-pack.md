# s3storage deployment task pack (`7.x`)

## Contract track

- [ ] Define service-to-service auth contract for storage endpoints.
- [ ] Define retention/deletion policy contract for object classes.

## Service track

- [ ] Enforce endpoint authz and environment-driven worker routing config.
- [ ] Remove static/hardcoded deployment-specific function bindings.

## Surface track

- [ ] Document role-gated storage controls in admin/app surfaces.
- [ ] Validate lifecycle-policy status and failure messaging for operators.

## Data track

- [ ] Ensure retention/deletion operations produce auditable evidence.
- [ ] Validate lineage fields for object lifecycle actions.

## Ops track

- [ ] Run authz coverage checks for storage action matrix.
- [ ] Publish retention/deletion control validation report for release gate.

