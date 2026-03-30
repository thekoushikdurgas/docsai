# Logs.api — Era `6.x` Reliability & Scaling Task Pack

### Context

**lambda/logs.api** powers centralized log query, cache behavior, and streaming/export patterns for incident response. Era `6.x` locks **query/cache/stream SLO evidence**, runbooks for **hot partitions** and **cache churn**, a **log-derived reliability dashboard** spec, and keeps [`logsapi_endpoint_era_matrix.json`](../backend/endpoints/logsapi_endpoint_era_matrix.json) authoritative.

**Codebase reference:** [`docs/codebases/logsapi-codebase-analysis.md`](../codebases/logsapi-codebase-analysis.md).

---

## Track A — Contract

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| A-6.1 | **Query SLO** | SLI: P95 for search/time-range queries; max result set; timeout behavior (`504` vs partial). | SRE |
| A-6.2 | **Cache SLO** | Hit ratio target; TTL semantics; stampede protection contract. | Backend |
| A-6.3 | **Stream / export SLO** | If streaming supported: max concurrent streams; backpressure signals. | Backend |
| A-6.4 | **Evidence bundle** | For RC: 7-day P95 screenshot + error rate + cache hit rate (roadmap 6.4 KPI alignment). | SRE |
| A-6.5 | **Schema / era `6.x`** | Document additive fields (`trace_id`, `tenant_id`) in matrix JSON. | Backend + Docs |

---

## Track B — Service

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| B-6.1 | **Hot partition mitigation** | Shard S3 CSV partitions; avoid single prefix thundering herd; prefix shuffling. | Backend |
| B-6.2 | **Cache churn control** | LRU + single-flight; negative caching for missing keys (short TTL). | Backend |
| B-6.3 | **Query guardrails** | Max time range; max rows; cancel long queries server-side. | Backend |
| B-6.4 | **AuthZ** | Tenant isolation on all query paths; audit access patterns. | Security |
| B-6.5 | **Health** | Readiness depends on backing store connectivity + cache warm enough. | DevOps |

---

## Track C — Surface

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| C-6.1 | **Ops UI** | If present: loading states, query timeout messaging, export progress (`components.md` Era 6). | Frontend |
| C-6.2 | **Embedded dashboards** | Iframe or API feed for reliability tiles fed from logs (see Track E). | Platform |

---

## Track D — Data

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| D-6.1 | **S3 CSV lineage** | Partition layout; retention; PII redaction in exported columns. | Data |
| D-6.2 | **Index metadata** | Bloom filters / manifest files; rebuild procedure after corruption. | Backend |

---

## Track E — Ops

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| E-6.1 | **Hot-partition runbook** | **Detect:** latency P95 spike on specific tenant/date prefix. **Mitigate:** temporary partition split, rate limit heavy tenant, scale readers. **Verify:** P95 recovers. | SRE |
| E-6.2 | **Cache-churn runbook** | **Detect:** hit ratio collapse + CPU spike. **Mitigate:** increase TTL, deploy single-flight fix, block abusive query pattern. | SRE |
| E-6.3 | **Log-derived reliability dashboard** | Panels: error rate by `service`, trace_id completeness, top noisy tenants, gateway 429/5xx counts ingested from logs. | SRE |
| E-6.4 | **On-call** | Link from [`queue-observability.md`](queue-observability.md) for trace correlation into logs. | SRE |

---

## Endpoint matrix reference

- Maintain and extend **[`logsapi_endpoint_era_matrix.json`](../backend/endpoints/logsapi_endpoint_era_matrix.json)** with `6.x` rows: query, export, health, cache-bypass flags (internal), stream endpoints if any.

---

## Reliability dashboard specification (minimum widgets)

| Widget | Query / metric | Purpose |
| --- | --- | --- |
| Ingest lag | `now - max(event_time)` by pipeline | MTTD for logging delays |
| Query P95 | Histogram of `/query` latency | User-facing logs UX |
| Cache hit % | `hits / (hits + misses)` | Cost + stability |
| Error budget burn | Derived from 5xx + timeouts | Tie to `/health/slo` story |
| Top traces | Count by `trace_id` tail | Incident triage |

---

## Completion gate

- [ ] Query/cache SLO evidence captured for staging + production baseline.
- [ ] Hot-partition and cache-churn runbooks tabletop-approved.
- [ ] Dashboard spec implemented or exported to Grafana/Datadog.
- [ ] `logsapi_endpoint_era_matrix.json` updated for era `6.x`.
