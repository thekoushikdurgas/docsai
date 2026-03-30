# Pre-deployment RC gate (Era 7 — Stage 6.9)

Pre-flight checklist for the **6.9 -> 7.0 transition**: entry conditions for the deployment/governance era. Complements `docs/6. Contact360 Reliability and Scaling/reliability-rc-hardening.md` and ensures any ongoing reporting/usage surfaces are safe under the stricter RBAC/authz/audit posture introduced in `7.0.0`.

## Preconditions

| Check | Notes |
| ----- | ----- |
| Usage and activity APIs stable | GraphQL `usage` / `activities` modules; no breaking schema changes without version bump |
| Sampling / PII | No raw PII in aggregate analytics payloads |
| RBAC | Admin-only analytics exports use `require_profile_roles` — `docs/7. Contact360 deployment/rbac-authz.md` |
| Traceability | `X-Trace-Id` on export and batch jobs — `docs/6. Contact360 Reliability and Scaling/queue-observability.md` |
| Admin settings wiring | Settings forms in `contact360.io/admin` must be wired beyond placeholder mode before 7.x governance sign-off |

## Smoke

1. Usage dashboard loads for FreeUser and ProUser; admin views require Admin+.
2. Export jobs (if any) complete and appear in job list with correct user scope.
3. Error path does not leak other tenants’ identifiers.

## Sign-off

| Role | Name | Date |
| ---- | ---- | ---- |
| Engineering | | |
| Analytics / Product | | |
