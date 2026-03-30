# Connectra — Era `6.x` Reliability & Scaling Task Pack

### Context

**Connectra** (search + sync + GraphQL API) must meet **query P95 SLO**, reliable **job success SLIs**, **Elasticsearch vs PostgreSQL drift detection**, **batch-upsert idempotency** evidence, **CORS hardening** for edge clients, and a **per-tenant rate limiter** aligned to commercial tiers.

**Codebase reference:** [`docs/codebases/connectra-codebase-analysis.md`](../codebases/connectra-codebase-analysis.md).

---

## Track A — Contract

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| A-6.1 | **Query P95 SLO** | Named SLI for primary read paths (e.g. `ListByFilters`, entity resolution); error-rate budget; document in `slo-idempotency.md`. | SRE + Search |
| A-6.2 | **Job success SLI** | Export/sync jobs: success ratio, lag P95; tie to jobs plane where Connectra emits work. | Backend |
| A-6.3 | **ES/PG drift contract** | Define acceptable lag; fields of truth (PG canonical vs ES search); reconciliation triggers alerts. | Backend |
| A-6.4 | **Batch-upsert idempotency** | Batch upserts accept stable keys; duplicate batch → same outcome (align 6.2 era). | Backend |
| A-6.5 | **CORS policy** | Explicit allowlist; no wildcard in production with credentials; document breaking changes. | Security |
| A-6.6 | **Per-tenant rate limit** | Token bucket keyed by `tenant_id` (Redis or gateway); 429 behavior + `Retry-After`. | Platform |

---

## Track B — Service

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| B-6.1 | **Query path optimization** | DataLoader / batching; eliminate N+1 on hot GraphQL fields (roadmap 6.5). | Backend |
| B-6.2 | **ES refresh strategy** | Balance search freshness vs load; document for operators. | Backend |
| B-6.3 | **Drift detector job** | Periodic compare: doc counts / checksum sample; write report + metric `connectra_es_pg_drift`. | Backend |
| B-6.4 | **Replay / rebuild** | Tooling to reindex tenant slice from PG after drift (read-only first). | Backend |
| B-6.5 | **Worker resilience** | Retry with jitter on transient ES/DB errors; DLQ for poison batches (see jobs pack). | Backend |

---

## Track C — Surface

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| C-6.1 | **API consumer UX** | Clients handle 429 with backoff; show degraded search banner if ES fallback mode (if any). | Frontend |
| C-6.2 | **Admin diagnostics** | Optional internal page: drift status, last reindex (ops-only). | Platform |

---

## Track D — Data

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| D-6.1 | **PG lineage** | Document core entity tables touched by upsert paths. | Docs |
| D-6.2 | **ES indices** | Mapping changes versioned; reindex playbook. | Backend |
| D-6.3 | **Idempotency evidence** | Store upsert batch id or hash for reconciliation audits. | Backend |

---

## Track E — Ops

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| E-6.1 | **Dashboards** | Panels: GraphQL P95, ES error rate, PG replica lag, drift job result. | SRE |
| E-6.2 | **Alerts** | P95 breach; drift detected; rate-limit FP review workflow. | SRE |
| E-6.3 | **Chaos** | ES yellow/red simulation — verify graceful degradation per policy. | SRE |
| E-6.4 | **RC** | [`reliability-rc-hardening.md`](reliability-rc-hardening.md) Connectra smoke row green. | Release Eng |

---

## ES / PG drift detection (runbook sketch)

| Signal | Threshold | Action |
| --- | --- | --- |
| Count mismatch | > **X** % per tenant | Trigger reindex job; page search owner |
| Stale documents | `updated_at` lag > **Y** min | Check indexer worker |
| ES cluster health | `red` | Fail readiness; serve minimal mode if configured |

---

## Completion gate

- [ ] Query P95 SLO baseline captured in dashboards.
- [ ] Batch-upsert idempotency test passes (duplicate submission).
- [ ] Drift detector runs on schedule with last success timestamp exported.
- [ ] CORS + per-tenant rate limit reviewed by security; no wildcard prod misconfig.
