# `lambda/s3storage` — era `3.x` contact and company data

**Era:** `3.x.x` — Contact360 **contact and company data system**  
**Goal:** Storage artifacts are **first-class inputs** for Connectra ingestion, enrichment, and export replay — with clear **naming**, **metadata**, and **lineage** from upload through job/index operations.

Cross-reference: [`docs/codebases/s3storage-codebase-analysis.md`](../codebases/s3storage-codebase-analysis.md) (section **`3.x.x` - Contact360 contact and company data system**), [`docs/frontend/s3storage-ui-bindings.md`](../frontend/s3storage-ui-bindings.md), [`connectra-service.md`](connectra-service.md) (`GET /common/upload-url`), [`jobs-contact-company-task-pack.md`](jobs-contact-company-task-pack.md).

---

## Scope

- Multipart and metadata flows that feed **`contact360_import_prepare`** / export artifacts.
- High-cardinality CSV **preview**, **schema**, and **stats** used to validate imports before Connectra upsert.

---

## Contract track

- [ ] Define **dataset artifact classes** for contacts vs companies imports (prefixes, content-types, max size).  
- [ ] Define **naming and versioning** policy for ingestion files (e.g. tenant/workspace/date/run id).  
- [ ] Define **minimum metadata** required for “ingestion ready” (row count estimate, delimiter, encoding, header hash).  
- [ ] Align presign / callback contracts with dashboard and gateway — see frontend s3storage bindings.  
- [ ] Document retry-safe **complete** semantics (idempotent complete, stale part cleanup).

## Service track

- [ ] Optimize **preview / schema / stats** for large, high-cardinality CSVs (memory bounds).  
- [ ] Improve **encoding** and **delimiter** detection; malformed-row reporting with row numbers.  
- [ ] Replace or harden **in-memory multipart session** store with durable shared state where analysis flags risk (per codebase analysis **`2.x.x`** learnings — apply to **`3.x`** contact/company uploads).  
- [ ] Checksum / **ETag** consistency between client parts and recorded metadata.

## Surface track

- [ ] Dashboard: upload progress, error recovery, and “ready for import” state — [`docs/frontend/s3storage-ui-bindings.md`](../frontend/s3storage-ui-bindings.md).  
- [ ] Expose **ingestion-ready metadata** fields to **Appointment360** / Jobs consumers (no hidden required fields).  
- [ ] Operator-facing copy for **resume** after partial failure.

## Data track

- [ ] **Lineage:** `s3_key` → **`job_id`** (import prepare) → Connectra **batch-upsert** run → optional **export** artifact key.  
- [ ] Metadata reconciliation: command or job to fix **upload vs metadata drift** (analysis recommendation).  
- [ ] Retention classes for staging vs long-lived exports (coordinate [`docs/audit-compliance.md`](../audit-compliance.md) if PII).

## Ops track

- [ ] **Quality checks** and **anomaly alerts** on ingestion metadata (sudden schema shift, zero-row files).  
- [ ] E2E resilience tests: partial upload, **abort**, **resume**, duplicate complete.  
- [ ] Runbook: “file shows complete but job never started” triage.

---

## Small-task breakdown (from codebase analysis `3.x.x`)

| Track | Examples |
| --- | --- |
| Contract | Artifact taxonomy doc + versioning |
| Service | Delimiter/encoding robustness |
| Surface | Gateway-visible metadata |
| Data | upload → ingestion run → index operation links |
| Ops | Anomaly alerts on bad metadata |

---

## Completion gate

- [ ] Sample jobs: **`s3_key`** traceable in **`job_response`** / logs event (`contact360.import.*` per [`logsapi-contact-company-data-task-pack.md`](logsapi-contact-company-data-task-pack.md)).  
- [ ] At least one **large-file** preview completes within agreed latency budget.  
- [ ] [`docs/backend/endpoints/`](../backend/endpoints/) or service README updated if presign paths change.

---

## References

- [`docs/codebases/s3storage-codebase-analysis.md`](../codebases/s3storage-codebase-analysis.md)  
- [`jobs-contact-company-task-pack.md`](jobs-contact-company-task-pack.md)  
- [`version_3.5.md`](version_3.5.md) — Import/Export Pipeline minor
