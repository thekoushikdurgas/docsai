# Sales Navigator — 1.x User & Billing Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `1.x` — Contact360 User and Billing and Credit System  
**Status:** Actor context and audit stubs

---

## Codebase evidence (backend(dev)/salesnavigator)

- Runtime: FastAPI (async) on AWS Lambda via Mangum
- Auth model: `X-API-Key` only (validated in `api/dependencies.py` via `verify_api_key`)
- Route surface:
  - `GET /v1/health`
  - `POST /v1/scrape` (parse HTML → optionally save)
  - `POST /v1/save-profiles` (bulk save profiles directly)
- Core orchestration:
  - `services/save_service.py` (`SaveService`) performs dedup + chunking + parallel save
  - `clients/connectra_client.py` provides `ConnectraClient` + connection pooling
- Downstream Connectra writes (billing-relevant because they can amplify volume):
  - `POST /contacts/bulk`
  - `POST /companies/bulk`
- Gap (important for 1.x guardrails): no rate limiting is implemented in this service today; gateway/job-layer must enforce credit + limit policy.

## Contract track

- [ ] Define whether SN profile saves consume user credits (decision: yes/no/separate quota)
- [ ] Add optional `X-User-ID` and `X-Org-ID` headers to `save-profiles` request contract for actor traceability
- [ ] Define credit deduction rate if applicable: e.g., 1 credit per contact saved from SN
- [ ] Document: unauthenticated saves still require `X-API-Key`; user context is additive

## Service track

- [ ] Pass `user_id`/`org_id` from request headers into Connectra bulk upsert `metadata` field
- [ ] Emit billing event stub on each successful save (or no-op stub that will be implemented in billing module)
- [ ] Validate that `X-API-Key` is required; return `403` if missing or invalid

## Surface track

- [ ] No new SN-specific UI in this era
- [ ] If credits apply: show "SN ingest costs X credits" tooltip in settings (billing section)
- [ ] Profile save confirmation: display remaining credit balance post-save (optional indicator)

## Data track

- [ ] Attach `actor_id` and `org_id` to ingestion event metadata sent to Connectra
- [ ] Stub: `api_usage` entry for SN save call (to be wired fully in `8.x`)
- [ ] Confirm `ai_chats.user_id` FK pattern does NOT apply to SN (no local DB)

## Ops track

- [ ] Add billing event emission smoke test (or confirm no-op stub is acceptable)
- [ ] Add IAM policy for Lambda to emit billing events if event bus is used
- [ ] Secret rotation: add `CONNECTRA_API_KEY` to rotation schedule

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
