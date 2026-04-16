# phone.server — gateway client vs HTTP routes

Source of truth for parity checks:

- **Gateway:** [`contact360.io/api/app/clients/phone_server_client.py`](../../../../contact360.io/api/app/clients/phone_server_client.py)
- **Server:** [`EC2/phone.server/internal/api/router.go`](../../../../EC2/phone.server/internal/api/router.go)

Auth for protected routes: header **`X-API-Key`** must equal **`API_KEY`** (gateway: **`PHONE_SERVER_API_KEY`**).

| `PhoneServerClient` method | HTTP | Notes |
|----------------------------|------|--------|
| `find_emails` | `POST /phone/finder/` | Query params: `first_name`, `last_name`, `domain` |
| `find_emails_bulk` | `POST /phone/finder/bulk` | JSON `items[]` |
| `verify_single_email` | `POST /phone/single/verifier/` | JSON `email`, `provider` |
| `verify_emails_bulk` | `POST /phone/bulk/verifier/` | JSON `emails[]`, `provider` |
| `create_verifier_s3_job` | `POST /phone/verify/s3` | JSON S3 + `csv_columns` |
| `create_finder_s3_job` | `POST /phone/finder/s3` | JSON S3 + `csv_columns` |
| `create_pattern_s3_job` | `POST /phone/pattern/s3` | JSON S3 + `csv_columns` |
| `get_job_status` | `GET /jobs/:id/status` | Returns `{ success, data }` |
| `list_jobs` | `GET /jobs` | Last 50 rows from `phoneapi_jobs` |
| `pause_job` / `resume_job` / `terminate_job` | `POST /jobs/:id/pause|resume|terminate` | |
| `web_search` | `POST /web/web-search` | JSON `full_name`, `company_domain` |
| `add_email_pattern` | `POST /phone-patterns/add` | |
| `add_email_pattern_bulk` | `POST /phone-patterns/add/bulk` | |
| `predict_email_pattern` | `POST /phone-patterns/predict` | |
| `predict_email_pattern_bulk` | `POST /phone-patterns/predict/bulk` | |

**Implementation note:** This service was derived from the email satellite stack; internal packages may still reference “email” in names. HTTP paths above are the public contract.

**Public (no API key):** `GET /health`, `GET /`.

Last reviewed: 2026-04-15.
