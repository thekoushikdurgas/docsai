# ai.server — ecosystem boundary (Era 2)

| System | Role |
|--------|------|
| **ai.server** | NL → VQL / Apollo URL parsing; Hugging Face chat; optional Postgres chat history; orchestrates satellite HTTP calls. |
| **sync.server (Connectra)** | System of record: `POST /contacts/`, `POST /companies/` VQL search; `GET /contacts/:uuid`, `GET /companies/:uuid`. |
| **email.server** | `POST /email/finder/?first_name&last_name&domain` |
| **phone.server** | `POST /phone/finder/?first_name&last_name&domain` |
| **s3storage.server** | `GET /api/v1/objects/presign-download?key=...` |
| **contact360.io/api** | Calls ai.server via **`AIServerClient`** (`/api/v1/*`). |

```mermaid
flowchart LR
  Api[contact360.io_api]
  Ai[ai_server]
  HF[HF_router]
  Sync[sync_server]
  Email[email_server]
  Phone[phone_server]
  S3[s3storage_server]
  Api -->|X-API-Key| Ai
  Ai --> HF
  Ai -->|X-API-Key VQL| Sync
  Ai -->|email_finder| Email
  Ai -->|phone_finder| Phone
  Ai -->|presign| S3
```

Last updated: 2026-04-15.
