# Platform productization (Era 9 — Stages 9.1–9.9)

Roadmap-level baseline for **multi-tenant SaaS maturity**: tenant model, admin, entitlements, SLA ops, support, residency, cost, lifecycle.

## Tenant model

- **Current:** user-scoped data with JWT — `docs/tenant-security-observability.md`.
- **Target:** explicit `tenant_id` / org entity; row-level enforcement; partner tokens scoped to tenant — `docs/integration-partner-governance.md`.

## Self-serve admin

- Role separation: `SuperAdmin` vs tenant admin (future role) for org-level settings without global superuser access.

## Entitlements engine

- Map **plan tier** → feature flags and quotas (credits, API caps, connector access).
- Single source of truth: avoid duplicating limits in multiple services.

## SLA / SLO operations

- Gateway SLO: `/health/slo` — `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md`.
- Define per-tier SLAs in contracts; alert on error budget burn.

## Support and residency

- **Support:** export minimal diagnostic bundle (trace id, user id, feature, timestamp); no bulk PII in tickets by default.
- **Data residency:** region-pinned stacks for regulated tenants (infrastructure choice; document per deployment).

## Cost and lifecycle

- Chargeback visibility: cost per tenant for expensive jobs (AI, bulk, exports).
- Lifecycle: offboarding workflow deletes or exports tenant data per policy — `docs/audit-compliance.md`.

## 9.x actionable checklist

### Tenant model

- 📌 Planned: Introduce explicit tenant entity and `tenant_id` propagation across gateway, async jobs, and connector adapters.
- 📌 Planned: Enforce row-level checks in resolver/service boundaries before storage/query operations.
- 📌 Planned: Publish tenant leak-test evidence for new endpoints and event pipelines.

### Self-serve admin

- 📌 Planned: Define tenant admin role capabilities separate from `SuperAdmin`.
- 📌 Planned: Add tenant-level controls for connector setup, disable, and policy override requests.
- 📌 Planned: Add audit entries for every control-plane mutation with actor, reason, and trace id.

### Entitlements engine

- 📌 Planned: Finalize single source of truth for plan tiers, feature flags, and quotas.
- 📌 Planned: Enforce entitlements at both synchronous gateway and asynchronous worker execution points.
- 📌 Planned: Publish reconciliation report for entitlement decisions vs billed usage.

### SLA / SLO operations

- 📌 Planned: Define per-tier SLAs for core ecosystem features (connectors, webhooks, async jobs).
- 📌 Planned: Alert on per-tenant error budget burn with escalation ownership.
- 📌 Planned: Produce monthly SLA evidence bundle using logs + trace correlation data.

### Support and residency

- 📌 Planned: Standardize support bundle format (`tenant_id`, `request_id`, `trace_id`, timestamp, feature).
- 📌 Planned: Redact PII by default in exported diagnostics for ticket workflows.
- 📌 Planned: Define region pinning checklist and exception process for residency-constrained tenants.

### Cost and lifecycle

- 📌 Planned: Add cost attribution model per tenant and connector class.
- 📌 Planned: Add offboarding runbook: data export, verification, deletion, and post-delete evidence.
- 📌 Planned: Validate lifecycle controls in RC gate before 10.x handoff.
