# s3storage — era `2.x` email system task pack

Grounded in [`docs/codebases/s3storage-codebase-analysis.md`](../codebases/s3storage-codebase-analysis.md).

## Codebase file map (high-value for `2.x`)

| Area | Paths (start here) | Notes |
| --- | --- | --- |
| API entrypoint | `lambda/s3storage/app/main.py` | FastAPI app bootstrap |
| Router | `lambda/s3storage/app/api/v1/router.py` | Endpoint grouping and mounting |
| Storage facade | `lambda/s3storage/app/services/storage_service.py` | Business-level storage operations |
| Backends | `lambda/s3storage/app/services/storage_backends.py` | **Risk:** in-memory multipart session store |
| Upload worker | `lambda/s3storage/app/utils/worker.py` | Invoked after complete to compute metadata |
| Metadata computation | `lambda/s3storage/app/utils/metadata_job.py` | CSV schema/preview/stats build |
| Metadata merge | `lambda/s3storage/app/utils/update_bucket_metadata.py` | **Risk:** read-modify-write race |

## Scope

- Multipart **CSV upload** reliability for finder/verifier **bulk** workflows  
- **Output artifacts** for job processors (export files)  
- **Metadata** freshness after upload completion (downstream jobs)

---

## Contract track

- [ ] Freeze multipart lifecycle API contract: `initiate`, presigned **part URL**, `register` part, `complete`, `abort`.  
- [ ] Define **retry/idempotency** expectations for `complete` and `abort` (duplicate complete safe?).  
- [ ] Document **output prefix** convention for email exports: link `job_id`, `user_uuid`, and optional `tenant` in key path.  
- [ ] Define **lifecycle policy** (retention, transition to cold storage) for email CSV objects containing PII.

## Service track

- [ ] Replace **in-memory** multipart session tracking with **durable shared storage** (Redis/Postgres/Dynamo — pick per implementation).  
- [ ] Harden **missing-part** and **duplicate-registration** failure handling.  
- [ ] **Bulk failure recovery:** client retry strategy, server-side cleanup of abandoned multipart sessions.  
- [ ] Ensure **metadata worker** runs reliably after `complete` — `metadata.json` merge for email artifacts.

### Codebase risks to treat as hard gates

1. **Multipart session state is in-process only**: `_MULTIPART_SESSIONS` map in `lambda/s3storage/app/services/storage_backends.py` must be replaced for any production-scale `2.4.x` bulk work.
2. **Hardcoded metadata worker function name**: `uploads.py` calls `FunctionName="s3storage-metadata-worker"` directly; must become environment-driven to avoid drift across envs.
3. **Metadata write race**: `update_bucket_metadata.py` read-modify-write without optimistic locking; must become concurrency-safe as bulk increases parallel completions.

## Database / data lineage track

- [ ] Ensure `metadata.json` **freshness SLA** after upload completion (jobs should not start until metadata ready — or explicit gate).  
- [ ] Add reconciliation tooling for **file vs metadata** drift on email prefixes.  
- [ ] Document **encryption** (SSE-S3, SSE-KMS) for buckets holding email CSV.

## Flow / graph track

- [ ] Document end-to-end: client chunks → S3 parts → `complete` → **metadata worker** → **jobs** pickup.

## Release gate evidence

- [ ] E2E bulk upload tests: success, **resume**, retry, **abort**, missing-part error.  
- [ ] Metadata worker **success rate** and **lag** metrics on dashboard.  
- [ ] Sample **output object** retrieved by job completion flow (signed URL or proxy).

## Related

- [`email_system.md`](email_system.md) — async CSV pipeline  
- `version_2.4` — Bulk Processing minor

## UI bindings (where this appears in the product)

- `docs/frontend/s3storage-ui-bindings.md` (primary)
- `docs/frontend/pages/files_page.json` (upload controls + progress UI)
