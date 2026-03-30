# Contact AI — 1.x User/Billing Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `1.x` — User and billing and credit system  
**Status:** Schema integrity + IAM hardening; no AI features live

---

## Codebase evidence (backend(dev)/contact.ai)

- Runtime:
  - FastAPI (async) deployed on AWS Lambda via Mangum adapter
- Authentication model:
  - `X-API-Key` (service-to-service)
  - `X-User-ID` (user-scoped chat ownership; must map to `users.uuid`)
- Rate limiting:
  - `TokenBucketRateLimiter` middleware (token bucket per IP/key)
- Observability:
  - `/health`, `/health/db`, `/metrics`
  - SSE streaming via `StreamingResponse`
- Data model:
  - `ai_chats` table in shared PostgreSQL:
    - columns include `uuid`, `user_id`, `title`, `messages` (JSONB)
- Cross-service:
  - Appointment360 uses `LambdaAIClient` (env: `LAMBDA_AI_API_URL`) to call this service.

## Contract track

- [ ] Document `X-User-ID` header binding: must resolve to a valid `users.uuid` in the shared Postgres DB.
- [ ] Document `X-API-Key` dependency: must validate service-to-service calls (cannot be bypassed).
- [ ] Define which user roles (FreeUser, ProUser, Admin, SuperAdmin) are permitted to use AI chat in `5.x`+.
- [ ] Document billing guard stubs: placeholder check that AI features are plan-gated.
- [ ] Confirm no credit deduction applies to contact.ai calls in `1.x` (deferred to `5.x`).

## Service track

- [ ] Validate `ai_chats.user_id` FK constraint against live `users` table in shared Postgres.
- [ ] Define cascade strategy for user deletion: `ON DELETE CASCADE` vs. soft-delete `ai_chats`.
- [ ] Log warning in `AIChatService` if `X-User-ID` does not match any existing user (observability only; do not block in `1.x`).
- [ ] Review `dependencies.py` `api_key_dep` to confirm it cannot be bypassed.

## Surface track

- [ ] No AI chat UI in `1.x`; confirm billing pages do not reference AI features.
- [ ] Stub plan-gate feature flag for AI chat: `ENABLE_AI_CHAT=false` in dashboard env.

## Data track

- [ ] Confirm `ai_chats` table exists in staging DB with correct FK to `users.uuid`.
- [ ] Run `add_ai_chats.sql` migration in staging; verify idempotency.
- [ ] Document user-deletion cascade behavior in `docs/backend/database/contact_ai_data_lineage.md`.

## Ops track

- [ ] Rotate `API_KEY` secret in secrets manager alongside other `1.x` secret rotation.
- [ ] Add `LAMBDA_AI_API_URL` to `appointment360` deploy environment (value may be placeholder in `1.x`).
- [ ] IAM policy review: Lambda execution role for contact.ai has least-privilege RDS/Secrets access.
- [ ] Add contact.ai health endpoint to monitoring dashboard health grid.

---

## 1.x — `user_id` integrity and credit hook preparation

| Task | Priority | Notes |
| --- | --- | --- |
| Enforce **`ai_chats.user_id` → `users.uuid` FK** in all envs | P0 | Staging proof before prod |
| **ON DELETE** policy: `CASCADE` vs soft-delete — document and implement one | P0 | Align with GDPR/product retention |
| `X-User-ID` must match JWT user when call originates from gateway | P1 | Spoof resistance when extension bypasses gateway |
| **1.x credit hook:** stub only — document future `5.x` **`deduct_credit`** integration; no silent billing in `1.x` | P0 | |
| Structured log when `X-User-ID` unknown | P1 | observability for abuse |

## IAM hardening (1.x)

- [ ] Lambda role: **no** s3:* or admin; RDS **least** privilege.
- [ ] Secrets: `API_KEY`, provider keys from Secrets Manager only in prod.

**References:**  
[`docs/codebases/contact-ai-codebase-analysis.md`](../codebases/contact-ai-codebase-analysis.md) · [`docs/backend/database/contact_ai_data_lineage.md`](../backend/database/contact_ai_data_lineage.md) · [`1.x-master-checklist.md`](1.x-master-checklist.md)
