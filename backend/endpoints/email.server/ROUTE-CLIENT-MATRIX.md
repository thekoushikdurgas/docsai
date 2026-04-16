# email.server — gateway client vs HTTP routes

Source of truth for parity checks:

- **Gateway:** [`contact360.io/api/app/clients/email_server_client.py`](../../../../contact360.io/api/app/clients/email_server_client.py)
- **Server:** [`EC2/email.server/internal/api/router.go`](../../../../EC2/email.server/internal/api/router.go)

Auth for protected routes: header **`X-API-Key`** must equal **`API_KEY`** (gateway: **`EMAIL_SERVER_API_KEY`**).

| `EmailServerClient` method | HTTP | Notes |
|----------------------------|------|--------|
| `find_emails` | `POST /email/finder/` | Query params: `first_name`, `last_name`, `domain` |
| `find_emails_bulk` | `POST /email/finder/bulk` | JSON `items[]` |
| `verify_single_email` | `POST /email/single/verifier/` | JSON `email`, `provider` |
| `verify_emails_bulk` | `POST /email/bulk/verifier/` | JSON `emails[]`, `provider` |
| `create_verifier_s3_job` | `POST /email/verify/s3` | JSON S3 + `csv_columns` |
| `create_finder_s3_job` | `POST /email/finder/s3` | JSON S3 + `csv_columns` |
| `create_pattern_s3_job` | `POST /email/pattern/s3` | JSON S3 + `csv_columns` |
| `get_job_status` | `GET /jobs/:id/status` | Returns `{ success, data }` |
| `list_jobs` | `GET /jobs` | Last 50 rows from `emailapi_jobs` |
| `pause_job` / `resume_job` / `terminate_job` | `POST /jobs/:id/pause|resume|terminate` | |
| `web_search` | `POST /web/web-search` | JSON `full_name`, `company_domain` |
| `add_email_pattern` | `POST /email-patterns/add` | |
| `add_email_pattern_bulk` | `POST /email-patterns/add/bulk` | |
| `predict_email_pattern` | `POST /email-patterns/predict` | |
| `predict_email_pattern_bulk` | `POST /email-patterns/predict/bulk` | |

**Public (no API key):** `GET /health`, `GET /`.

Last reviewed: 2026-04-15.
