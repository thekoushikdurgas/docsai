# `s3storage` API Task Packs (`0.x`-`10.x`)

This document supplements `07_S3_MODULE.md` and `10_UPLOAD_MODULE.md` with era-aligned task packs for `lambda/s3storage`.

## API scope

- Buckets: create logical bucket namespaces
- Files: list/info/download-url/delete
- Uploads: multipart lifecycle + single-shot upload endpoints
- Analysis: schema/preview/stats/metadata
- Avatars: upload/download-url

## Era task packs

- `0.x`: baseline contract freeze and backend parity checks
- `1.x`: user artifact and billing-proof policy enforcement
- `2.x`: multipart durability, retries, and metadata freshness guarantees
- `3.x`: ingestion artifact quality and lineage requirements
- `4.x`: extension/SN provenance and access policy
- `5.x`: AI artifact classes and retention/access controls
- `6.x`: idempotency, reconciliation, and SLO contracts — `docs/6. Contact360 Reliability and Scaling/` patches `6.N.P — *.md` (**Service task slices**)
- `7.x`: service authz and retention/deletion governance — `docs/7. Contact360 deployment/` patches `7.N.P — *.md` (**Service task slices**)
- `8.x`: versioning/deprecation and event delivery contracts — `docs/8. Contact360 public and private apis and endpoints/` patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-api-endpoint-task-pack.md` merged)
- `9.x`: entitlement/quota policy and tenant economics — `docs/9. Contact360 Ecosystem integrations and Platform productization/` patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-ecosystem-productization-task-pack.md` merged)
- `10.x`: campaign reproducibility and compliance artifact controls — `docs/10. Contact360 email campaign/` patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `s3storage-email-campaign-task-pack.md` merged)

## Contract quality checklist

For any storage contract change:

1. Update both module docs (`07_S3_MODULE.md`, `10_UPLOAD_MODULE.md`).
2. Update endpoint metadata under `docs/backend/endpoints/`.
3. Update Postman collections for GraphQL and backend REST storage paths.
4. Update `docs/codebases/s3storage-codebase-analysis.md` and `docs/versions.md` references.
