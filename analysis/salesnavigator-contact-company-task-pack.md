# Sales Navigator — 3.x Contact & Company Data Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `3.x` — Contact360 Contact and Company Data System  
**Status:** Full field mapping and provenance tagging locked  

---

## Contract track

- [ ] Lock Connectra contact field contract for SN-sourced contacts (all fields in `mappers.py` explicitly documented)  
- [ ] Lock company field contract (name, uuid, linkedin_sales_url, technologies)  
- [ ] Define provenance fields: `source="sales_navigator"`, `lead_id`, `search_id`, `connection_degree`, `data_quality_score`  
- [ ] Align field names with Connectra VQL filter taxonomy (confirm `seniority` and `departments` enum values)  
- [ ] Document: `employees_count`, `industries`, `annual_revenue` are always `null` from SN (enrichment required separately)  

## Service track

- [ ] Implement and test full `mappers.py` field coverage:  
  - [ ] `parse_name()` — first/last name split  
  - [ ] `parse_location()` — city/state/country comma split  
  - [ ] `infer_seniority()` — executive/director/manager/senior_ic/entry  
  - [ ] `extract_departments_from_title_about()` — keyword match  
- [ ] Validate `generate_contact_uuid()` and `generate_company_uuid()` determinism under all edge cases  
- [ ] Handle **`PLACEHOLDER_VALUE` / SN URL → standard LinkedIn URL** gaps — document as **known dedup quality risk**; mitigation options: enrichment pass, exclude-from-UUID until resolved, or explicit `linkedin_url` null policy (coordinate with Data/Connectra)  

### Idempotency and retries

- [ ] Add **chunk-level idempotency token** (header or body) for save/bulk paths so Lambda retries do not duplicate Connectra writes — maps to `version_3.6` / `6.x` analysis gap.  
- [ ] Define behavior when same chunk is submitted twice: HTTP status + Connectra idempotency expectations.  

## Surface track

- [ ] Contact detail page: `ContactSourceBadge` ("Source: Sales Navigator")  
- [ ] Contact row: `SeniorityChip`, `DepartmentChips`, `ConnectionDegreeBadge`  
- [ ] Company detail: SN company URL link  
- [ ] Contact filter: `ContactSourceFilter` (radio: all / SN / organic)  
- [ ] Contacts table: `SeniorityFilter` checkbox multi-select, `DepartmentFilter` checkbox multi-select  

## Data track

- [ ] Add `source`, `lead_id`, `search_id`, `connection_degree`, `data_quality_score` to provenance fields written to Connectra  
- [ ] Confirm `recently_hired`, `is_premium`, `mutual_connections_count` fields stored in Connectra contact extended attrs  
- [ ] Test: same profile URL → same UUID on second save (idempotency)  
- [ ] Test: profile with different email → different UUID (confirm intended behavior)  

## Ops track

- [ ] Run integration test: 100-profile batch → Connectra → verify created/updated counts  
- [ ] **Reconciliation report:** `input profile count = created + updated + errors (+ duplicates_skipped)` — publish with every release candidate touching mappers  
- [ ] Parity check: all profiles in input appear in Connectra by UUID  
- [ ] **Provenance gate:** reject or flag records missing `source="sales_navigator"` when ingest claims SN origin (configurable strict mode)  

---

## References:

- `docs/codebases/salesnavigator-codebase-analysis.md`  
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`  
- `docs/backend/database/salesnavigator_data_lineage.md`  

## Completion gate

- [ ] Reconciliation equation holds on 1k profile golden batch.  
- [ ] PLACEHOLDER / URL policy documented and signed off by Data owner.  
- [ ] Idempotency retry test: duplicate chunk → no duplicate Connectra rows.
