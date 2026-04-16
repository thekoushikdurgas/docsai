# Lead / enrichment ownership — email.server vs sync.server vs CRM

| Concern | Owner |
|--------|--------|
| **Lead scores, recommendation rank, campaign stage** | Contact360 CRM DB + sync.server (OpenSearch) as configured for contacts/companies — **not** computed inside email.server |
| **Email finder / verify / pattern** | **email.server** (Go + Asynq + Redis + `emailapi_jobs`) |
| **Contact/company search and CRUD for Connectra** | **sync.server** (`POST /contacts/`, etc.) |
| **Gateway orchestration** | **contact360.io/api** — GraphQL, `scheduler_jobs`, `EmailServerClient` |

Use **email.server** outputs (verified email, finder source, pattern metadata) as **inputs** to enrichment pipelines that **write** lead fields in the main API or sync.server, rather than expecting email.server to store CRM lead scores.
