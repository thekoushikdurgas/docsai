# Sales Navigator — 0.x Foundation Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `0.x` — Foundation and pre-product stabilization  
**Status:** Scaffold only — no user-facing ingest in this era

---

## Contract track

- [ ] Define `POST /v1/save-profiles` OpenAPI spec stub (request/response schema, auth header) (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Define `POST /v1/scrape` OpenAPI spec stub (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Document UUID5 generation algorithm as canonical contract: `uuid5(NAMESPACE_URL, linkedin_url + email)` and `uuid5(NAMESPACE_URL, company_name + company_url)` (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Define `X-API-Key` header authentication contract (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Add `GET /v1/health` health endpoint spec to service catalog (patch assignment: `0.9.0`–`0.9.2`)

## Service track

- [ ] Create FastAPI + Mangum application scaffold (`app/main.py`, `app/api/`, `app/core/`) (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Wire `pydantic-settings` config with all required env vars (`API_KEY`, `CONNECTRA_API_URL`, `CONNECTRA_API_KEY`) (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Implement `GET /` info endpoint and `GET /v1/health` liveness endpoint (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Add exception handler stubs for `ValidationError` and `ConnectraClientError` (patch assignment: `0.9.3`–`0.9.6`)
- [ ] Create `requirements.txt` with pinned `fastapi`, `mangum`, `httpx`, `pydantic`, `beautifulsoup4`, `tenacity` (patch assignment: `0.9.3`–`0.9.6`)

## Surface track

- [ ] No user-facing UI in `0.x` (extension only; no dashboard pages/routes) (patch assignment: `0.9.3`–`0.9.6`)
- [ ] Extension hook stub: define interface contract that extension will use in `4.x` (patch assignment: `0.9.3`–`0.9.6`)

## Data track

- [ ] Document deterministic UUID generation rules in `docs/backend/database/salesnavigator_data_lineage.md` (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Define field mapping skeleton: SN profile → Connectra contact fields (patch assignment: `0.9.0`–`0.9.2`)
- [ ] Confirm `PLACEHOLDER_VALUE` sentinel behavior for unconvertible SN URLs (patch assignment: `0.9.3`–`0.9.6`)

## Ops track

- [ ] Create `template.yaml` AWS SAM skeleton with Lambda + API Gateway (patch assignment: `0.9.3`–`0.9.6`)
- [ ] Set Lambda timeout: 60s, memory: 1024 MB (patch assignment: `0.9.3`–`0.9.6`)
- [ ] Add health probe to CI pipeline (patch assignment: `0.9.7`–`0.9.9`)
- [ ] Add `pytest` baseline with one smoke test (patch assignment: `0.9.7`–`0.9.9`)
- [ ] Create `.example.env` with all required variables (patch assignment: `0.9.7`–`0.9.9`)

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
- `docs/backend/database/salesnavigator_data_lineage.md`
