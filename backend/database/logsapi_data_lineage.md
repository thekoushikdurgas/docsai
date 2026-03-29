# logs.api data lineage (S3 CSV)

## Storage model
- Backend: S3 objects under `logs/` prefix.
- Object pattern: `logs/logs-YYYY-MM-DD-HH-MM-SS.csv`.
- Retention: 90-day lifecycle policy (as defined in `lambda/logs.api/template.yaml`).

## Lineage fields
- `timestamp`, `request_id`, `trace_id`, `service`, `level`, `message`, `metadata`.
- Correlates to gateway, jobs, extension, AI, integrations, and campaign flows by era.

## Era lineage concerns
- `1.x` user/billing traceability
- `2.x` bulk email throughput and status lineage
- `6.x` reliability/SLO evidence and incident timelines
- `7.x` deployment/audit governance evidence
- `10.x` campaign compliance and immutable audit retention

## 2026 lineage addendum

- Canonical persistence is S3 CSV, not MongoDB.
- Recommended logical partition pattern for investigation queries: `logs/{service}/{YYYY}/{MM}/{DD}/logs.csv`.
- Query paths may use in-memory cache windows, but immutable source-of-truth remains S3 objects.
