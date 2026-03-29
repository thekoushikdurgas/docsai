# Admin UI Bindings (`contact360.io/admin`)

## Core admin surfaces

- Billing: payment review, QR settings, approval/decline actions.
- Users: list, history, statistics, role-governed actions.
- Logs: query/search/update/delete/bulk-delete controls.
- Jobs: list, detail, retry operations.
- Storage: list/download/delete and upload support.

## Backend bindings

- `admin_client.py` -> Appointment360 GraphQL.
- `logs_api_client.py` -> `lambda/logs.api`.
- `s3storage_client.py` -> `lambda/s3storage`.

## Auth and role chain

`JWT cookie -> Appointment360AuthMiddleware -> SuperAdminMiddleware -> decorators(require_super_admin / require_admin_or_super_admin) -> view`

## Known integration gap

- `s3storage_client.py` auth-header behavior must stay aligned with `S3S-0.1` storage auth hardening.
