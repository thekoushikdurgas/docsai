# Sales Navigator — 5.x AI Workflows Task Pack

**Service:** `backend(dev)/salesnavigator`  
**Era:** `5.x` — Contact360 AI Workflows  
**Status:** AI-field quality and enrichment for downstream AI usage

---

## Contract track

- [ ] Define minimum field requirements for a SN contact to be eligible for AI context:
  - `title` present
  - `data_quality_score >= 50`
  - `about` present (for richer AI context)
- [ ] Define `parse-filters` payload contract compatibility: SN field names vs. AI filter schema
- [ ] Contract: `company/summary` calls can use company data from SN-sourced contacts

## Service track

- [ ] Ensure `seniority` and `departments` inference outputs valid values for AI prompt construction
- [ ] Surface `data_quality_score` as a filterable field (confirm Connectra VQL supports `data_quality_score >= N`)
- [ ] Ensure `about` field passes through extraction without truncation (max length defined)
- [ ] Add test: SN-sourced contact with full `about` → valid AI company summary request

## Surface track

- [ ] `DataQualityBar` — thin progress bar on contact row showing AI-eligibility
- [ ] "AI-ready" indicator badge: displayed when `data_quality_score >= 50`
- [ ] AI chat panel: SN-sourced contacts can appear in `messages.contacts[]` payload
- [ ] "Recently saved from SN" filter chip in AI filter input context
- [ ] `AIFilterInput` parsing: NL → filter recognizes `source=sales_navigator` as a segment
- [ ] `CompanySummaryTab` can show summary for SN-imported companies

## Data track

- [ ] Confirm `messages.contacts[]` JSONB sub-schema covers SN contact fields (`seniority`, `departments`, `linkedin_sales_url`)
- [ ] Confirm `data_quality_score` is indexed in Connectra for VQL filter queries
- [ ] Validate `about` field max length and encoding in SN extraction

## Ops track

- [ ] Test: AI `parse-filters` with `source=sales_navigator` segment → correct VQL output
- [ ] Monitor: AI errors caused by low-quality SN contacts (missing title/company)
- [ ] Alert: high proportion of `data_quality_score < 30` from SN ingest sessions

---

**References:**
- `docs/codebases/salesnavigator-codebase-analysis.md`
- `docs/codebases/contact-ai-codebase-analysis.md`
- `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`

---

## Extension surface contributions (era sync)

**Extension surface note (era 5.x):** The extension logic layer (`auth/`, `utils/`) has no direct AI workflow dependency. However, profiles ingested by the extension feed Connectra, which is the primary data source for AI-assisted contact enrichment and AI email writing workflows.

- Extension-captured profiles provide the base data for AI enrichment (Contact AI service)
- AI enrichment fields (e.g., AI-generated summaries, inferred email patterns) flow back to contacts visible in the dashboard