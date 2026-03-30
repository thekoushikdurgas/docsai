# Sales Navigator — 2.x Email System Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `2.x` — Contact360 Email System  
**Status:** Email field validation and enrichment handoff

## Codebase file map (high-value)

Grounded in [`docs/codebases/salesnavigator-codebase-analysis.md`](../codebases/salesnavigator-codebase-analysis.md).

| Area | Paths (start here) | Notes |
| --- | --- | --- |
| Entrypoint | `backend(dev)/salesnavigator/app/main.py` | FastAPI + Mangum wiring |
| Routes | `backend(dev)/salesnavigator/app/api/v1/endpoints/scrape.py` | `/v1/scrape` and `/v1/save-profiles` |
| Field mapping | `backend(dev)/salesnavigator/app/services/mappers.py` | **Primary** email/email_status mapping logic |
| Save orchestration | `backend(dev)/salesnavigator/app/services/save_service.py` | Dedup + chunk/parallel save to Connectra |
| Connectra client | `backend(dev)/salesnavigator/app/clients/connectra_client.py` | Bulk upsert calls and retry/timeouts |

---

## Contract track

- [ ] Define handoff contract: SN-ingested contacts with `email` field → eligible for email finder/verifier jobs
- [ ] Define handoff contract: SN-ingested contacts without `email` → auto-enqueue to `email_finder_export` job
- [ ] Lock `email`, `email_status`, `mobile_phone` field presence semantics in `save-profiles` request

## Service track

- [ ] In `mappers.py`: validate `email` field format if present; set `email_status=unverified` if email present but status absent
- [ ] After save: emit job creation event for email enrichment if `email` is absent (stub for `jobs` service)
- [ ] Confirm mapper behavior: SN profiles with `email=""` vs. absent field

### Email-status preservation risk (treat as a hard gate)

`2.x` depends on a stable `email_status` vocabulary across ingestion → enrichment → UI:

- [ ] If `email_status` is present in SN payload, preserve it without renaming.
- [ ] If `email` is present but `email_status` is absent, set `email_status=unverified` (explicit, not null).
- [ ] Never write placeholder sentinel values for absent `email` fields; use `null`/missing consistently.

## Surface track

- [ ] Extension popup: show "Email missing — will be found" indicator per profile if `email` is absent
- [ ] Dashboard contacts row: "Needs email enrichment" badge on SN-sourced contacts without email
- [ ] Email enrichment status chip: `email_status` display on contact row

## Data track

- [ ] Confirm `email` field is passed through correctly from SN lead card extraction
- [ ] Confirm `email_status` field is preserved when present (e.g., `verified`, `risky`, `invalid`)
- [ ] Define: contacts inserted with `email=null` should be eligible for email finder pipeline

## Ops track

- [ ] Add test: `save-profiles` with contacts that have `email` → verify `email` written to Connectra
- [ ] Add test: `save-profiles` with contacts that lack `email` → verify null written (not PLACEHOLDER)
- [ ] Monitor: downstream email API errors due to malformed SN email data

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
- `docs/backend/database/salesnavigator_data_lineage.md`

---

## Extension surface contributions (era sync)

**Extension surface note (era 2.x):** The extension logic layer (`auth/`, `utils/`) has no direct email system dependency. Profile data collected by the extension is sent to Connectra for indexing; email discovery for captured contacts is triggered via the dashboard, not the extension itself.

- Extension-captured contact objects may contain `email` fields if present in the SN profile DOM
- These emails are stored as-is (unverified); email verification is a dashboard-side workflow (Mailvetter / emailapis)