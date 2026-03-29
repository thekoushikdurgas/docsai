# Contact AI — 3.x Contact/Company Data Task Pack

**Service:** `backend(dev)/contact.ai`  
**Era:** `3.x` — Contact and company data system  
**Status:** `parseContactFilters` + `generateCompanySummary` contracts locked; aligned with Connectra VQL

---

## Contract track

- [ ] Lock `POST /api/v1/ai/parse-filters` response schema — must map to Connectra VQL fields:
  - `jobTitles`, `companyNames`, `industry`, `location`, `employees` (range), `seniority`
- [ ] Lock `POST /api/v1/ai/company/summary` response: `{"summary": "<string>"}`
- [ ] Confirm `LambdaAIClient` paths use `/api/v1/ai/parse-filters` and `/api/v1/ai/company/summary`.
- [ ] Align `ParseFiltersResponse` fields in `17_AI_CHATS_MODULE.md` with Connectra VQL filter taxonomy (`docs/3. Contact360 contact and company data system/vql-filter-taxonomy.md`).
- [ ] Document `messages.contacts[]` JSONB sub-schema alignment with Connectra contact index fields.

## Service track

- [ ] Implement `POST /api/v1/ai/company/summary` in `app/api/v1/endpoints/ai.py`.
- [ ] Implement `POST /api/v1/ai/parse-filters` with structured JSON output from HF.
- [ ] Write prompt for `parseContactFilters`: extract job titles, company names, industry, location, employee count range, seniority.
- [ ] Validate `employees` field as `[min, max]` integer array; handle single value or missing range.
- [ ] Write prompt for `generateCompanySummary`: comprehensive summary from company name + industry.
- [ ] Handle `contacts[]` JSONB in message schema: validate field names match Connectra contact index.

## Surface track

- [ ] Implement `CompanySummaryTab` on company detail page: trigger on tab click, show shimmer while loading.
- [ ] Implement `AIFilterInput` on contact search page: NL text box above filter panel; on submit, populate filter chips.
- [ ] Add chip display for parsed filter values (job title chips, company chips, location chips, seniority chips).
- [ ] Show `useParseFilters` hook output as pre-selected filter values; allow user to deselect individual chips.
- [ ] Confirm `ContactsInMessage` component in chat renders fields from Connectra contact index.

## Data track

- [ ] Confirm `messages.contacts[]` JSONB field names align with `contacts` index fields used in Connectra responses.
- [ ] Test round-trip: NL query → `parseContactFilters` → filters applied to Connectra VQL → contacts returned in chat message.
- [ ] Confirm company name + industry are not logged or persisted outside `ai_chats.messages` JSONB.
- [ ] Add `3.x` lineage note to `docs/backend/database/contact_ai_data_lineage.md`.

## Ops track

- [ ] Integration test: `parseContactFilters` → VQL query → contact search end-to-end.
- [ ] Load test `generateCompanySummary` with p95 < 3s; tune Lambda timeout accordingly.
- [ ] Add all three utility endpoints to contact.ai Postman collection.

---

**References:**  
`docs/codebases/contact-ai-codebase-analysis.md` · `docs/backend/apis/17_AI_CHATS_MODULE.md` · `docs/frontend/contact-ai-ui-bindings.md` · `docs/3. Contact360 contact and company data system/vql-filter-taxonomy.md`
