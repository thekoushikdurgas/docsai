# `s3storage` Task Pack - Era `1.x.x`

## Scope
- User artifacts and billing-proof related storage paths
- Validation policy for object classes

## Codebase evidence (lambda/s3storage)

- Entrypoint: `lambda/s3storage/app/main.py`
- Router: `lambda/s3storage/app/api/v1/router.py`
- Service facade: `lambda/s3storage/app/services/storage_service.py`
- Backends:
  - `lambda/s3storage/app/services/storage_backends.py` → `S3Backend`, `FilesystemBackend`
- Config selector:
  - `lambda/s3storage/app/core/config.py` with `S3STORAGE_STORAGE_BACKEND=s3|filesystem`
- Endpoint groups (API surface):
  - `health`, `buckets`, `files`, `uploads`, `analysis` (schema/preview/stats/metadata), `avatars`
- Async metadata pipeline:
  - upload complete triggers `s3storage-metadata-worker`
  - worker handler: `lambda/s3storage/app/utils/worker.py`

## Bucket prefix model (proof-aligned)

Single-bucket, prefix-based object layout:
- `{bucket_id}/avatar/`
- `{bucket_id}/photo/`
- `{bucket_id}/resume/` (or resume-equivalent prefix used by runtime)
- `{bucket_id}/upload/` (used for billing proof screenshots and user uploads)
- `{bucket_id}/export/` (csv/exports)
- `{bucket_id}/metadata.json` (canonical per-upload metadata index)

## Small tasks
- Contract:
  - define object-class policy contract (`avatar`, `photo`, `resume`, `upload`)
  - define max size/content-type rules per object class
- Service:
  - enforce path-specific validation at upload endpoints
  - add retry-safe semantics for overwrite/delete flows
- Database/Data lineage:
  - store actor/source metadata for compliance and audit trails
- Flow/Graph:
  - billing proof flow: upload proof -> approval workflow linkage
  - profile avatar flow: upload/replace/read URL
- Release gate evidence:
  - validation matrix pass (allowed vs blocked types)
  - audit field presence checks

## Billing-proof alignment checks (1.x)

- Billing proof object class must map to the upload prefix (`{bucket_id}/upload/`) and produce a stable `proof_url` that `payment_submissions.proof_url` can persist.
- `metadata.json` must include enough fields to:
  - verify content-type and size,
  - link actor/source metadata (user id / request id / upload origin).
- Retry-safe overwrite/delete:
  - re-submitting proof should not create multiple conflicting proof objects for the same submission idempotency key (gateway-controlled idempotency is still required).

## Reference

- [`docs/codebases/s3storage-codebase-analysis.md`](../codebases/s3storage-codebase-analysis.md)
