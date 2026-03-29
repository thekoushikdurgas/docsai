# S3 Storage Service — Era `6.x` Reliability & Scaling Task Pack

### Context

**s3storage** (multipart uploads, metadata, lifecycle) requires **idempotent complete/abort**, **durable multipart session** state, **metadata CAS** (compare-and-swap), **reconciliation utilities** for object-vs-metadata consistency, and **SLO dashboard targets** (upload success, complete latency, metadata lag).

**Codebase reference:** [`docs/codebases/s3storage-codebase-analysis.md`](../codebases/s3storage-codebase-analysis.md) — use the **`6.x.x`** reliability section as implementation truth.

---

## Track A — Contract

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| A-6.1 | **Idempotency keys** | `complete` and `abort` accept `X-Idempotency-Key`; duplicate → same HTTP semantics + stable ETag reference (`version_6.6.md`). | Backend |
| A-6.2 | **Multipart session durability** | Session state survives process crash; TTL for abandoned sessions; replay-safe `complete`. | Backend |
| A-6.3 | **Metadata CAS** | Updates require `If-Match` / version column; conflict returns `409` with remediation hints. | Backend |
| A-6.4 | **Reconciliation contract** | Define drift types: **object exists / row missing**, **row exists / object missing**, **size mismatch**; severity classes. | Backend + SRE |
| A-6.5 | **SLO targets** | **Upload success %**; **complete latency P95**; **metadata lag** (DB timestamp vs S3 `LastModified`). | SRE |

---

## Track B — Service

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| B-6.1 | **Session store** | Durable store (Redis/DB) for uploadId → parts list; periodic cleanup job. | Backend |
| B-6.2 | **Concurrency-safe metadata** | Serialize updates per `object_id`; avoid lost updates under concurrent complete. | Backend |
| B-6.3 | **Reconciliation job** | Scheduled scan + optional on-demand `?dry_run=true`; metrics `s3storage_drift_total{type}`. | Backend |
| B-6.4 | **Lifecycle hooks** | Integrate bucket lifecycle (IA/Glacier) with DB state — document in `performance-storage-abuse.md`. | DevOps |
| B-6.5 | **Orphan cleanup** | Delete incomplete multipart + metadata after policy window; audit log entries. | Backend |

---

## Track C — Surface

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| C-6.1 | **Upload UX** | Resume after network drop; progress bar; CAS conflict user message (refresh + retry). | Frontend |
| C-6.2 | **Admin tooling** | Internal UI for reconciliation report summary (ops-only). | Platform |

---

## Track D — Data

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| D-6.1 | **Metadata tables** | Document columns for version/etag/part count; migrations versioned. | Docs |
| D-6.2 | **Integrity reports** | Store last reconciliation run id + summary JSON in DB or object store. | Backend |

---

## Track E — Ops

| ID | Task | Description | Owner |
| --- | --- | --- | --- |
| E-6.1 | **SLO dashboard** | Panels: upload success, complete P95, metadata lag, reconciliation drift count, orphan sweep results. | SRE |
| E-6.2 | **Alerts** | Spike in drift; complete latency SLO breach; failed multipart GC. | SRE |
| E-6.3 | **Runbooks** | S3 regional outage: pause completes; drain sessions; failover bucket policy (if multi-region). | SRE |
| E-6.4 | **RC evidence** | [`reliability-rc-hardening.md`](reliability-rc-hardening.md) storage smoke + screenshots. | Release Eng |

---

## Reconciliation utilities (checklist)

| Utility | Purpose |
| --- | --- |
| Dry-run scan | Report only; no deletes |
| Repair `missing_object` | Mark DB row deleted or quarantine |
| Repair `missing_row` | Create stub row or delete orphan object |
| Metrics export | Push drift counters to dashboards |

---

## Completion gate

- [ ] Duplicate `complete` with same idempotency key does not double-charge storage or metadata.
- [ ] Crash test: mid-upload resume works or fails closed safely.
- [ ] CAS conflict path tested end-to-end.
- [ ] Reconciliation job shows zero unexplained drift post-cleanup on staging bucket.
