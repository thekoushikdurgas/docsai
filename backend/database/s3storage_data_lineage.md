# `s3storage` Database and Data Lineage Scope

## Data model context

`s3storage` is object-storage centric and does not own core relational tables directly. It participates in lineage through:

- logical bucket references (`users.bucket` owned by gateway domain)
- object keys under bucket prefixes
- bucket metadata sidecar (`metadata.json`)
- workflow linkage to jobs, billing artifacts, AI artifacts, and campaign artifacts

## Key lineage entities

- `bucket_id` (logical tenant/user namespace)
- `file_key` (relative object path)
- object class prefix (`avatar/`, `upload/`, `photo/`, `resume/`, `export/`)
- multipart identifiers (`uploadId`, `partNumber`, `etag`)
- metadata entry fields (size, rows, columns, delimiter, encoding)

## Era-aware lineage requirements

- `1.x`: user and billing artifact traceability
- `2.x`: bulk CSV upload -> processing pipeline lineage
- `3.x`: ingestion/export lineage to data/search workflows
- `6.x`: reconciliation and consistency evidence between metadata and object state
- `7.x`+: retention/deletion governance evidence
- `10.x`: campaign compliance evidence lineage

## Operational checks

- metadata integrity sweep (metadata entries correspond to existing objects)
- orphan object detection (object exists without metadata entry where required)
- duplicate metadata entry detection by `file_key`
- stale metadata freshness check after upload completion

## References

- `docs/codebases/s3storage-codebase-analysis.md`
- `docs/roadmap.md` (`s3storage` cross-era execution stream)
- `docs/versions.md` (`s3storage` execution spine)

## 2026 lineage addendum

- Bucket metadata canonical artifact: `metadata.json` (bucket-level manifest).
- Multipart upload session state currently uses in-memory process structures and is non-durable without shared backing.
- Planned object classification metadata includes: `email_list`, `contact_import`, `campaign_asset`.
