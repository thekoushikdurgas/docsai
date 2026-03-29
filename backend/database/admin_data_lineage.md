# Admin data lineage (`contact360.io/admin`)

## Local state stores

- SQLite (default dev) for Django internals.
- PostgreSQL (production profile) for durable admin/service metadata.
- Redis for cache/session helpers and Django-Q task coordination.

## External lineage dependencies

- Appointment360 GraphQL (`contact360.io/api`) for auth, role, billing, and user data.
- `lambda/logs.api` for log query/statistics/update/delete operations.
- `contact360.io/jobs` / tkdjob for job operations visibility and retry actions.
- `lambda/s3storage` for file listing/download/delete and media uploads.

## Auth lineage

- Access/refresh JWT cookies are authoritative user session artifacts.
- Super-admin role checks are cached and must be traceable to source token identity.

## Governance notes

- Destructive admin actions require immutable audit evidence with actor and request metadata.
