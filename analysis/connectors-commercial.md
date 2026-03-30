# Connector framework + integration observability + commercial controls (Era 8 — Stages 8.6–8.8)

## Connector framework (baseline)

Treat each **external system** as a connector with:

| Artifact | Description |
| -------- | ----------- |
| **Client module** | `contact360.io/api/app/clients/<name>_client.py` (or service-specific Lambda) |
| **Config** | `Settings` fields + env vars; no secrets in code |
| **Contract** | Request/response shapes documented; version pinned when upstream changes |
| **Health** | Callable health check or smoke test in `scripts/test_external_services.py` where applicable |

New connectors must follow `docs/integration-partner-governance.md` for identity and tenant safety.

## Integration observability

- **Correlation:** `X-Trace-Id` end-to-end — `docs/6. Contact360 Reliability and Scaling/queue-observability.md`.
- **SLO:** Gateway `/health/slo`; downstream SLOs owned per service — `docs/6. Contact360 Reliability and Scaling/slo-idempotency.md`.
- **Structured logs:** Include connector name, operation, latency, and error class (transient vs permanent).

## Commercial controls (integrations)

- **Metering:** Billable usage tied to successful user-visible outcomes (e.g. verified email, export row) — align with `usage` / credits modules.
- **Entitlements:** Feature flags per plan tier before calling expensive connectors — roadmap to Era 9.
- **Rate limits:** Per-tenant or per-partner caps in addition to gateway abuse guards — `docs/6. Contact360 Reliability and Scaling/performance-storage-abuse.md`.

## Era 9 connector extensions

### Partner token validation

- Require partner identity binding (`client_id`, scoped secret/token, tenant binding) at gateway ingress.
- Reject connector requests that provide tenant identifiers without authenticated cryptographic binding.
- Add key rotation and compromise runbook alignment with partner governance controls.

### Per-connector SLO targets

- Define p95 latency and success-rate targets by connector class (sync ingestion, async webhook callback, bulk export).
- Segment SLO reporting by tenant and plan tier.
- Escalate when connector-specific error budget burn exceeds threshold.

### Entitlement-aware metering contract

- Meter only successful user-visible outcomes (verified email, persisted contact, completed async task).
- Persist entitlement decision lineage (`feature`, `plan`, `tenant_id`, `decision`, `request_id`) for billing reconciliation.
- Ensure fallback provider usage is metered and auditable.

### DLQ and replay requirements

- Require dead-letter queue behavior for webhook delivery and async connector processing.
- Define replay API semantics with idempotency keys and bounded replay windows.
- Add operator dashboard requirements for DLQ depth, replay attempts, and final disposition.
