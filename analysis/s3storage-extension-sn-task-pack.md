# `lambda/s3storage` — Era 4.x.x Extension & Sales Navigator Task Pack

**Service:** `lambda/s3storage`  
**Era:** `4.x.x` — Contact360 Extension and Sales Navigator maturity per [`docs/codebases/s3storage-codebase-analysis.md`](../codebases/s3storage-codebase-analysis.md) § `4.x.x`.

---

## Scope

- Extension-origin and Sales Navigator artifact storage with **tight access controls**, **URL TTL policy**, and **channel-level observability**.
- Align object prefixes and provenance with [`docs/governance.md`](../governance.md) storage controls where referenced.

---

## Contract track

| Task | Priority |
| --- | --- |
| Define **extension-safe presigned URL TTL** and maximum grant duration by object class (upload vs download vs preview) | P0 |
| Define **extension-origin prefix schema** (e.g. tenant / channel / session segments) — no collision with dashboard-only prefixes | P0 |
| Document **access constraint matrix**: extension session vs server-side job vs operator admin (who may `GET`/`PUT` which prefix) | P0 |
| Cross-reference **governance** retention classes for SN scrape artifacts vs extension uploads | P1 |

---

## Service track

| Task | Priority |
| --- | --- |
| Enforce **stricter auth context checks** on extension-origin operations (API key scope, optional JWT claims) | P0 |
| **Download URL policy** by object class: short-lived for PII-adjacent SN HTML snapshots; stricter signing when exposing to browser | P0 |
| Extension-friendly **error + retry** semantics (403 vs 404 vs expired URL) — surface copy in extension pack | P1 |

---

## Surface track

| Task | Priority |
| --- | --- |
| Ensure dashboard **SN ingestion** and **jobs** UIs show linked artifact id when an object exists in s3storage | P1 |
| Extension: progressive disclosure — user-visible “upload failed / link expired” states tied to telemetry | P1 |

---

## Data track

| Task | Priority |
| --- | --- |
| Persist **provenance tags** on metadata: `source=extension|salesnavigator` on write paths | P0 |
| **Provenance tag validation procedure:** sample job — verify every extension-origin object has required tags before mark-complete | P0 |
| Lineage: link **S3 object key → SN save batch id / request id** in metadata sidecar or jobs record | P1 |

---

## Ops track

| Task | Priority |
| --- | --- |
| **Channel-level telemetry:** dashboards split **extension** vs **dashboard** vs **Lambda SN** traffic (requests, 4xx/5xx, latency) | P0 |
| Reliability: success rate for **complete / abort** flows originating from extension channel; alarms on stuck multipart | P1 |
| Runbook: leaked object or wrong prefix — revoke URL class, audit tag gaps, backfill metadata | P1 |

---

## References

- [docs/frontend/s3storage-ui-bindings.md](../frontend/s3storage-ui-bindings.md)
- [`docs/codebases/s3storage-codebase-analysis.md`](../codebases/s3storage-codebase-analysis.md) § `4.x.x`  
- [`extension-telemetry.md`](extension-telemetry.md)  
- [`sales-navigator-ingestion.md`](sales-navigator-ingestion.md)  
- [`docs/governance.md`](../governance.md)
