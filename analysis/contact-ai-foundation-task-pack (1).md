# Contact AI — 0.x Foundation Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `0.x` — Foundation and pre-product stabilization  
**Status:** Infrastructure baseline only; no AI features live

---

## Contract track

- [ ] Define `contact.ai` OpenAPI spec stub (paths, auth headers, version prefix `/api/v1`). (patch assignment: `0.3.0`–`0.3.2`)
- [ ] Document `X-API-Key` and `X-User-ID` header contracts in `docs/backend/apis/17_AI_CHATS_MODULE.md`. (patch assignment: `0.3.0`–`0.3.2`)
- [ ] Stub health endpoint contract: `GET /health` → `{"status":"ok"}`, `GET /health/db` → DB connectivity. (patch assignment: `0.3.0`–`0.3.2`)
- [ ] Lock base URL convention: `LAMBDA_AI_API_URL` env var in `appointment360`. (patch assignment: `0.3.3`–`0.3.6`)

## Service track

- [ ] Scaffold FastAPI app in `backend(dev)/contact.ai/app/main.py` with Mangum Lambda handler. (patch assignment: `0.3.0`–`0.3.2`)
- [ ] Wire `app/core/config.py` for all env vars (`DATABASE_URL`, `API_KEY`, `HF_API_KEY`, `GEMINI_API_KEY`, `HF_CHAT_MODEL`). (patch assignment: `0.3.0`–`0.3.2`)
- [ ] Implement `GET /health` and `GET /health/db` endpoints. (patch assignment: `0.3.0`–`0.3.2`)
- [ ] Create `app/api/v1/router.py` with placeholder route mounts for `ai_chats` and `ai`. (patch assignment: `0.3.3`–`0.3.6`)
- [ ] Add CORS, GZip compression, and `TokenBucketRateLimiter` middleware stubs. (patch assignment: `0.3.3`–`0.3.6`)

## Surface track

- [ ] No UI surface in `0.x`; confirm no dashboard routes reference AI chat. (patch assignment: `0.3.3`–`0.3.6`)
- [ ] Add `LAMBDA_AI_API_URL` to dashboard env config stub (unused in `0.x`). (patch assignment: `0.3.3`–`0.3.6`)

## Data track

- [ ] Create `docs/backend/tables/ai_chats.sql` DDL file. (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Create `docs/backend/migrations/add_ai_chats.sql` additive migration. (patch assignment: `0.2.0`–`0.2.2`)
- [ ] Validate `ai_chats.user_id` FK reference to `users.uuid` in migration script. (patch assignment: `0.2.3`–`0.2.6`)
- [ ] Review JSONB `messages` column default value and index strategy. (patch assignment: `0.2.3`–`0.2.6`)

## Ops track

- [ ] Add `backend(dev)/contact.ai` to monorepo CI lint pipeline. (patch assignment: `0.10.3`–`0.10.6`)
- [ ] Create AWS SAM template stub for Lambda deployment. (patch assignment: `0.10.3`–`0.10.6`)
- [ ] Add `contact.ai` health endpoint probe to CI smoke test suite. (patch assignment: `0.10.0`–`0.10.2`)
- [ ] Document required IAM permissions (Secrets Manager, VPC, RDS) for Lambda execution. (patch assignment: `0.10.0`–`0.10.2`)

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/backend/database/contact_ai_data_lineage.md`

---

## Codebase-analysis alignment (foundation risks)

Address during **`0.3`** (gateway client contract) and **`0.2`** (schema) as applicable.

### `ModelSelection` enum freeze

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Align Pydantic/schema `ModelSelection` with DB CHECK constraint or ORM enum — **one source of truth** | P0 | Analysis: enum mismatch risk | `0.2.0`–`0.2.2` |
| Migration or backfill if legacy rows violate enum | P0 | | `0.2.0`–`0.2.2` |
| Document allowed values in `docs/backend/apis/17_AI_CHATS_MODULE.md` | P0 | | `0.2.0`–`0.2.2` |

### Global `API_KEY` → parameterized config

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Ensure **no** committed default secrets; load from env / Secrets Manager only | P0 | | `0.10.0`–`0.10.2` |
| Separate **service** API key vs **provider** keys (`HF_*`, `GEMINI_*`) in settings docs | P0 | | `0.10.0`–`0.10.2` |
| Key rotation playbook stub for `0.10` | P1 | | `0.10.3`–`0.10.6` |

### JSONB `messages` schema versioning

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Add schema `$schema` or `version` field inside JSONB messages blob | P0 | Analysis: loose JSONB | `0.2.0`–`0.2.2` |
| Read path: tolerate unknown minor versions; write path: pin current version | P0 | | `0.2.0`–`0.2.2` |
| Optional JSON Schema file checked into `docs/backend/` or `app/schemas/` | P1 | | `0.2.3`–`0.2.6` |

### Silent provider fallback (e.g. Gemini) — logging

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| When falling back across inference providers, emit **structured log** + user-visible degraded flag where product allows | P0 | Avoid silent swaps | `0.3.0`–`0.3.2` |
| Metric counter: `ai_provider_fallback_total{from,to}` | P1 | | `0.3.3`–`0.3.6` |

### Distributed tracing stub

| Task | Priority | Notes | Patch assignment |
| --- | --- | --- | --- |
| Honor incoming `X-Request-ID` / trace headers from Appointment360; emit on outbound calls | P1 | Analysis: no distributed tracing | `0.3.3`–`0.3.6` |
| Document header contract in `17_AI_CHATS_MODULE.md` | P1 | | `0.3.3`–`0.3.6` |

**Reference:** [`docs/codebases/contact-ai-codebase-analysis.md`](../codebases/contact-ai-codebase-analysis.md)
