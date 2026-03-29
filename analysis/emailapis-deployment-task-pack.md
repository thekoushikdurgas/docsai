# emailapis task pack — era 7.x

This pack decomposes lambda/emailapis and lambda/emailapigo work into Contract, Service, Surface, Data, and Ops tracks.

## Contract tasks
- Define and freeze era 7.x email endpoint and payload compatibility notes.
- Update endpoint/reference matrix in docs/backend/endpoints/emailapis_endpoint_era_matrix.json.
- Define RBAC requirements for who can invoke email finder/verifier and related bulk operations; map roles using `docs/7. Contact360 deployment/rbac-authz.md`.

## Service tasks
- Implement/validate runtime behavior for era 7.x finder, verifier, pattern, and fallback paths.
- Verify auth, provider routing, error envelope, and health diagnostics behavior.
- Ensure gateway-enforced role checks are respected for finder/verifier operations (no privileged behavior based on client-supplied role).
- Emit audit/trace events to `logs.api` for bulk verify operations (include actor identity + trace/correlation ids; do not store raw PII in audit payloads).

## Surface tasks
- Document impacted pages/tabs/buttons/inputs/components for era 7.x.
- Document relevant hooks/services/contexts and UX states (loading/error/progress/checkbox/radio).

## Data tasks
- Document email_finder_cache and email_patterns lineage impact for era 7.x.
- Record provider, status, and traceability expectations for this era (what audit fields exist, and how they are correlated).

## Ops tasks
- Add observability checks and release validation evidence for era 7.x (trace ids present in logs + audit viewable in logs.api).
- Capture rollback and incident-runbook notes for email-impacting releases (including how to identify/roll back problematic bulk verify batches).
