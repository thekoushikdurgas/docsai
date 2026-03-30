# `s3storage` task pack — era `0.x` (`lambda/s3storage`)

Foundation work: service bootstrap, core REST contract, logical key taxonomy, and deployment sanity before multipart and campaign-scale usage in later eras.

| Track | Owner (default) | Priority |
| --- | --- | --- |
| Contract | Platform + arch | P0 |
| Service | Backend | P0 |
| Data / lineage | Platform | P0 |
| Ops | DevOps | P0 |

## Contract tasks

- Lock base endpoint semantics: **`health`**, **`buckets`**, **`files`**, **`uploads`**, **`analysis`** (or actual route set in code) with success/error shapes. (patch assignment: `0.5.0`–`0.5.2`)
- Freeze **logical key prefixes** for `0.x`: e.g. `avatar`, `upload`, `photo`, `export` — and document forbidden keys. (patch assignment: `0.5.0`–`0.5.2`)
- Document **auth**: API key header name, who may call from gateway vs internal Lambdas only. (patch assignment: `0.5.0`–`0.5.2`)

## Service tasks

- Verify **`s3`** vs **`filesystem` backend parity** on: list, metadata read, presigned upload/download where applicable. (patch assignment: `0.5.0`–`0.5.2`)
- Standardize errors through **`StorageError`** (or equivalent) with stable `error_code` values for clients. (patch assignment: `0.5.0`–`0.5.2`)
- Confirm **CORS** and **payload size** limits for local vs deployed environments. (patch assignment: `0.5.0`–`0.5.2`)

## Data / lineage tasks

- Establish **`metadata.json` v1** baseline shape (fields, required keys, versioning). (patch assignment: `0.5.0`–`0.5.2`)
- Document bucket/prefix naming per environment (dev/stage/prod) without secrets. (patch assignment: `0.5.0`–`0.5.2`)

## Flow / graph

- Validate **bootstrap flow**: ensure bucket (or local dir) → upload → list → download/presign works in CI or manual script. (patch assignment: `0.5.3`–`0.5.6`)

## Ops tasks

- Capture **SAM/template** or deploy artifact version used for `0.x` smoke. (patch assignment: `0.5.3`–`0.5.6`)
- Add **health** check to compose or deploy pipeline; record expected response body. (patch assignment: `0.5.3`–`0.5.6`)

## Release gate evidence (`0.x`)

- [ ] API smoke pass (automated or signed checklist) (patch assignment: `0.5.7`–`0.5.9`)
- [ ] Contract excerpt checked into `docs/backend` or linked from `docs/architecture.md` (patch assignment: `0.5.7`–`0.5.9`)
- [ ] No plaintext secrets in docs or committed `.env` (patch assignment: `0.5.7`–`0.5.9`)

## Surface track

Surface track scope for the storage upload UX (0.x foundation era):

- [ ] `FilesUploadModal` stub present (drag-drop zone renders) (patch assignment: `0.5.3`–`0.5.6`)
- [ ] Upload progress bar wired to upload state transitions and uses design-token references from `docs/frontend/design-system.md` (patch assignment: `0.5.3`–`0.5.6`)
- [ ] TTL-expired presign recovery UX shows “re-initiate upload” message (patch assignment: `0.5.3`–`0.5.6`)

---

## High-impact gaps (`docs/codebases/s3storage-codebase-analysis.md`) — prioritize in **`0.5`**

### Durable multipart session state

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Replace in-memory multipart session map with **durable** store (DynamoDB, Redis, or Postgres) | P0 | Survive Lambda cold start / scale-out | `0.5.0`–`0.5.2` |
| TTL + cleanup job for abandoned sessions | P0 | | `0.5.0`–`0.5.2` |
| Document session key format | P0 | | `0.5.0`–`0.5.2` |

### Env-driven metadata worker function name

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Remove hardcoded `s3storage-metadata-worker` (or equivalent); use **env** / SSM | P0 | Enables stage/prod separation | `0.5.0`–`0.5.2` |
| IAM: invoke permission scoped to named function(s) | P0 | | `0.5.0`–`0.5.2` |

### Concurrency-safe `metadata.json`

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| RMW race mitigation: optimistic locking (ETag), or per-prefix merge lambda, or S3 object lock review | P0 | Analysis: metadata write race | `0.5.0`–`0.5.2` |
| Define **`metadata.json` v1** schema version field | P0 | Already in Data track — enforce in worker | `0.5.0`–`0.5.2` |

### E2E and failure-path tests

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| CI or scripted: initiate → upload parts → complete → worker → readable metadata | P0 | | `0.5.0`–`0.5.2` |
| Failure: **incomplete** multipart, **expired** presign, worker **timeout** | P0 | Expected user/API errors documented | `0.5.0`–`0.5.2` |
| Filesystem vs S3 backend parity suite (same tests, two envs) | P1 | | `0.5.3`–`0.5.6` |

### CORS and auth tightening

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Restrict CORS to known dashboard/extension origins in non-dev | P0 | Permissive CORS cited as gap | `0.5.0`–`0.5.2` |
| Presign: verify **Content-Type** / max size where applicable | P1 | Upload security checklist | `0.5.3`–`0.5.6` |

### SLO / observability baseline

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Dashboards or CloudWatch: 4xx/5xx, multipart completion latency, worker failures | P1 | Tie to `0.10` ops gate | `0.5.3`–`0.5.6` |
| Structured logs: `upload_id`, `bucket_id`, correlation id | P0 | | `0.5.0`–`0.5.2` |

**References:** [`docs/codebases/s3storage-codebase-analysis.md`](../codebases/s3storage-codebase-analysis.md), [`version_0.5.md`](version_0.5.md)
