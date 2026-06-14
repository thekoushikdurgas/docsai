# Contact360 project documentation analysis
_Exported on 6/14/2026 at 07:59:00 GMT+5:30 from Cursor (3.7.27)_

---

**User**

@docs/DECISIONS-GOVERNANCE.md @docs/DECISIONS.md @docs/DEPLOYMENT-MATRIX.md @docs/DOC-GATE-CHECKLIST.md @docs/DOC-HYGIENE-CHECKLIST.md @docs/hiring-analytics.md @docs/OBSERVABILITY-BASELINE.md @docs/OPEN-DECISIONS-RESOLVED.md @docs/PHASE-DOCS-INDEX.md @docs/README.md @docs @docs/0.Foundation and pre-product stabilization and codebase setup @docs/1.Contact360 user and billing and credit system @docs/2.Contact360 phone number and email system @docs/3.Contact360 contact and company data system @docs/4.Contact360 Extension and Sales Navigator maturity @docs/5.Contact360 AI workflows @docs/6.Contact360 Reliability and Scaling @docs/7.Contact360 deployment @docs/8.Contact360 public and private apis and endpoints @docs/9.Contact360 Ecosystem integrations and Platform productization @docs/10.Contact360 campaign and sequence and template and builder system @docs/11.Lead generation and user recommendation engine @docs/backend @docs/codebases @docs/docs @docs/flowchart @docs/frontend @docs/prd @docs/runbooks @docs/scripts @docs/tech read this files and then think about my contact360 project
0.x.x - Foundation and pre-product stabilization and codebase setup
1.x.x - Contact360 user and billing and credit system
2.x.x - Contact360 phone number and email system
3.x.x - Contact360 contact and company data system
4.x.x - 4.Contact360 Extension and jobs maturity 
5.x.x - Contact360 AI workflows
6.x.x - Contact360 Reliability and Scaling
7.x.x - Contact360 deployment
8.x.x - Contact360 public and private apis and endpoints and mcps
9.x.x - Contact360 Ecosystem integrations and Platform productization
10.x.x - Contact360 campaign and sequence and template and builder system
11.x.x - Contact360 lead generation and recommendation engine
Learn, understand, and analyse this deeply, and then break your tasks into smaller tasks.

---

**Cursor**

I'll read the governance docs and phase index first, then work through the numbered phase folders to build a structured picture of Contact360.


# Contact360 — Deep Analysis & Task Breakdown

After reading your governance docs, phase indexes, `DECISIONS.md`, deployment matrix, and foundation handoff roadmap, here is a structured picture of the project and how to break work into smaller tasks.

---

## What Contact360 Is

Contact360 is a **multi-tenant B2B sales/CRM platform** with:

- A **Python FastAPI + Strawberry GraphQL gateway** (`contact360.io/api`) as the product API hub
- A **Next.js dashboard** (`contact360.io/app`) and **Django admin** (`contact360.io/admin`)
- A **Chrome MV3 extension** for LinkedIn / Sales Navigator capture and enrichment
- **Go satellites on EC2** for specialized workloads (Connectra, email, phone, AI, campaigns, extension, jobs, storage, logs, proxy)
- **ECS Fargate** as the default deploy target for stateless apps; satellites stay on EC2

The docs are organized as a **12-phase roadmap (0–11)** with machine-readable `index.json` per phase. Most phase markdown is still **`stub`**; the **as-built reality** lives in `DECISIONS.md`, `docs/backend/endpoints/*`, and working code under `contact360.io/*` and `EC2/*`.

---

## Architecture (Hub-and-Spoke)

```mermaid
flowchart TB
  subgraph clients [Clients]
    Web[Next.js Dashboard]
    Ext[Chrome Extension MV3]
    Admin[Django Admin]
    Partners[Public REST v1 - future]
  end

  GW[Gateway API<br/>JWT + RLS Postgres]

  subgraph satellites [EC2 Go Satellites - X-API-Key]
    Connectra[sync.server / Connectra<br/>Postgres + OpenSearch VQL]
    ExtSrv[extension.server]
    Email[email.server]
    Phone[phone.server]
    AI[ai.server]
    Campaign[campaign.server]
    Job[job.server - hiring signals]
    S3[s3storage.server]
    Log[log.server]
    Proxy[proxy.server]
  end

  Web --> GW
  Ext --> GW
  Admin --> GW
  Partners -.-> GW

  GW --> Connectra
  GW --> ExtSrv
  GW --> Email
  GW --> Phone
  GW --> AI
  GW --> Campaign
  GW --> Job
  GW --> S3
  GW --> Log
```

**Key contracts** (from `DECISIONS.md`):

| Concern | Decision |
|--------|----------|
| Product API | GraphQL on gateway for web + extension |
| Public API | REST + OpenAPI only (gateway-shaped DTOs, not raw Connectra) |
| Satellite auth | `X-API-Key`; gateway holds all keys |
| Contact identity | UUID5 from normalized fields; merge never silently rewrites UUID5 |
| Cross-service events | Kafka; intra-service jobs | BullMQ/Asynq |
| AI runtime | Planner in `ai.server`; gateway = JWT, allowlist, SSE proxy |
| Campaigns | CQL + `campaign.server` only for MVP |
| Billing | Stripe global + Razorpay India via `BillingPort` |
| India SMS | TRAI DND checks, ~24h Redis cache |

**Five canonical flows** anchor everything:

| Flow | Path |
|------|------|
| FLOW-1 | Contact create/list (gateway → Connectra VQL) |
| FLOW-2 | Email enrichment waterfall |
| FLOW-3 | AI / RAG / tools |
| FLOW-4 | Campaign execution |
| FLOW-5 | Extension capture → gateway → extension.server → Connectra |

---

## Phase Maturity Snapshot

| Phase | Focus | Doc maturity | Code/doc reality |
|-------|--------|--------------|------------------|
| **0** | Foundation | Partial (21 populated / 55 stub) | As-built map, FLOW-1/5, CI table, readiness checklist done |
| **3** | Contact/company data | **Best documented** (26 populated backend refs) | Connectra, VQL filters UI, satellite schemas/routes |
| **4** | Extension + SN (+ jobs in your naming) | Mostly stub (1 populated pipeline doc) | Extension + `extension.server` exist; SN stubs need filling |
| **1** | Billing/credits | All stub (45 sections) | Gateway auth exists; billing not built |
| **2** | Email/phone | All stub (84 sections) | `email.server` / `phone.server` satellites exist |
| **5** | AI workflows | All stub (~130 sections) | `ai.server` exists; LangGraph docs not written |
| **6** | Reliability | Mostly stub | SLO-BY-SLICE + runbooks started |
| **7** | Deployment | Mostly stub | DEPLOYMENT-MATRIX populated; Terraform stubs |
| **8** | Public/private APIs | Mostly stub | GraphQL live; REST v1 subset referenced |
| **9** | Integrations | Mostly stub | Future iPaaS/CRM |
| **10** | Campaigns/CQL | Mostly stub | `campaign.server` exists |
| **11** | Lead gen / recommendations | Mostly stub | `job.server` + hiring analytics partially live |

**Note:** Your label for phase 4 (“Extension and **jobs** maturity”) overlaps two systems in the repo: **Sales Navigator / extension** (phase 4) and **hiring signals** (`job.server`, dashboard `/hiring-signals`, `hiring-analytics.md`). The official phase folder title is still “Sales Navigator maturity”; job ingest is documented under `DECISIONS.md` § job.server and `docs/codebases/job.md`.

---

## Recommended Execution Order

From `15-ops/04-phase-roadmap-handoff.md` — **not** numeric 0→11 order:

```
1. Phase 3 + 4  →  data plane + extension capture
2. Phase 1      →  billing/credits (needs usage signals)
3. Phase 2      →  email/phone enrichment
4. Phase 10     →  campaigns/CQL
5. Phase 5      →  AI workflows
6. Phase 8      →  public REST v1
7. Phase 6 + 7  →  SLOs + ECS/EC2 hardening (parallel)
8. Phase 9      →  integrations
9. Phase 11     →  lead scoring / recommendations
```

Foundation (phase 0) is largely **exit-ready** except CI green on `main` and Connectra `satelliteHealth` in target envs (both marked 🟡).

---

## Task Breakdown (Smaller Tasks)

### Cross-cutting (do continuously)

**Governance & docs hygiene**
1. Run `python docs/scripts/verify-index-json-paths.py` quarterly
2. On every contract PR: tick `DOC-GATE-CHECKLIST.md` (DECISIONS, satellite parity, VQL triple-sync, GraphQL schema regen)
3. Keep `SATELLITE-PARITY.md` aligned when gateway clients change
4. Promote stubs → `populated` only with owner + `last_reviewed` front matter

**Observability**
5. Propagate `X-Request-ID` gateway → all satellite clients
6. Wire `health.satelliteHealth` checks for every configured satellite in staging/prod
7. Instrument RED metrics per `OBSERVABILITY-BASELINE.md`
8. Track SLOs in `SLO-BY-SLICE.md` (contacts list p95, SN save p95, enrichment p95, campaign lag, AI TTFB)

---

### Phase 0 — Foundation (finish remaining)

**Vision & domain (stubs)**
9. Write product vision + v0 scope/non-goals (`00-vision/*`)
10. Document CRM + agentic ubiquitous language (`01-domain/*`)
11. Document event naming (align with `DECISIONS.md` dot-case topics)

**Devex & ops (stubs)**
12. `docker-compose` local stack doc (`10-devex/01-local-environment-setup.md`)
13. Env vars + secrets strategy doc
14. Testing strategy overview (unit / integration / E2E / AI evals)
15. CI promotion strategy (dev → stage → prod)
16. Security baseline checklist (OWASP, JWT, RLS, PII)
17. Developer onboarding guide

**Foundation exit**
18. Verify `main` green on all CI workflows in Phase 0 README
19. Confirm `satelliteHealth` returns ok for Connectra in staging
20. Complete remaining stub flows: search sync, CSV upload, import lifecycle

---

### Phase 3 + 4 — Vertical slice 1 (highest priority)

This is the **core product loop**: capture → store → search → enrich.

**Phase 3 — Connectra / CRM data**
21. Verify batch-upsert response docs (`contact_uuids`, `company_uuids`, error semantics) in `sync.server-schema.md`
22. Postman note for `POST /contacts/batch-upsert` and `/companies/batch-upsert`
23. Finish contacts VQL UI backlog (`docs/docs/contacts-filter-vql-ui.md`)
24. Implement/stub contact entity schema, dedup/merge UX (UUID5 policy already decided)
25. Contact source tracking (manual, import, extension, enrichment)
26. Import pipeline: CSV parse → column map → bulk upsert to Connectra
27. OpenSearch index sync pipeline (Kafka → worker)
28. Activity feed + engagement scoring (feeds phase 11 later)

**Phase 4 — Extension + Sales Navigator (+ jobs surface)**
29. Document SN pipeline end-to-end (extend `63-sales-navigator/00-pipeline-gateway-connectra.md`)
30. Document `chrome.storage` keys (`c360_last_capture_preview`, preview merge)
31. Align `flowchart/extension-capture.md` with GraphQL fields (`contactUuids`, `savedContacts`, etc.)
32. MV3 manifest + folder structure docs (match `contact360.extension` as-built)
33. OAuth2 / JWT token management in extension
34. LinkedIn profile selectors + extraction logic (content scripts)
35. Sales Navigator page structure + batch scrape queue
36. Popup/side panel UI specs (link `frontend/extension/eras/`)
37. Extension SSE sidebar for progressive enrichment (FLOW-5)
38. Extension unit + integration tests
39. **Jobs maturity:** document `job.server` ↔ Connectra read-through; extend hiring analytics (`/demands-and-trends`, `/market-insights`); gateway `hireSignal` filter parity

**Slice 1 acceptance**
40. E2E: SN save → Connectra UUIDs → contacts list with VQL filters → preview merge in extension
41. SLO: SN save p95 &lt; 5s per chunk; contacts list p95 &lt; 800ms

---

### Phase 1 — Billing & credits

42. Define org/user/role model + account lifecycle states
43. Plan catalog (FREE/STARTER/PRO/ENTERPRISE) + feature entitlements
44. Implement `BillingPort` abstraction (Stripe + Razorpay)
45. Subscription lifecycle + webhook handlers (`invoice.paid`, `payment_failed`)
46. Credit types (email, phone, AI, enrichment) + balance/refill policy
47. Usage meters + recording pipeline (sync vs async, idempotent)
48. Pre-flight credit checks before enrichment, campaigns, AI tools
49. Map billing state → auth (suspended, read-only)
50. Billing UI: overview, plan change, credit visualization, dunning UX
51. Billing ops: reconciliation, audit logs, finance reporting (MRR, churn)

---

### Phase 2 — Email & phone system

52. Document email.server routes ↔ gateway GraphQL `email` module (parity exists; phase stubs need filling)
53. Email discovery waterfall: Pattern → Hunter → Apollo → SMTP verify → ZeroBounce
54. Bulk validation orchestration + job status polling
55. Phone normalization (E.164) + carrier lookup
56. TRAI DND compliance + Redis 24h cache (already in DECISIONS — implement + document)
57. Enrichment trigger model (on create, on-demand, bulk CSV)
58. Credit reservation/settlement per `EnrichmentJob.json`
59. Pre-campaign email/SMS validation hooks (feeds phase 10)
60. Extension content scripts for email/phone detection on web pages
61. AI tools: `email.find`, `phone.find`, `email.validate` specs
62. Compliance: unsubscribe/consent, PII encryption, audit logs

---

### Phase 10 — Campaigns, sequences, templates

63. Document `campaign.server` CQL parser/validator + gateway `campaignSatellite` parity
64. Sequence step model + Asynq task types (`campaign:send`, `campaign:email`, etc.)
65. Template builder (HTML/JSON in S3)
66. Audience selection from VQL contact lists (phase 3 dependency)
67. Multi-channel orchestration (email + phone + LinkedIn steps)
68. Send progress SSE for dashboard
69. Pre-flight audience health check (phase 2 dependency)
70. Credit consumption rules for sends

---

### Phase 5 — AI workflows

71. LangGraph topology in `ai.server` (gateway stays thin per OPEN-DECISIONS topic G)
72. Agent state model + checkpointing (Redis/Postgres)
73. Tool surface: read (search, analytics) + write (campaign.create, update_contact) with allowlist
74. Forbidden tools + safety rules
75. Memory layers (session / long-term / vector)
76. SSE token stream for chat (already decided transport)
77. Credit check before tool execution (phase 1 dependency)
78. RAG: Connectra VQL + pgvector embeddings
79. Use-case prompt templates (campaign, VQL, follow-up)

---

### Phase 8 — Public/private APIs & MCPs

80. Document REST vs GraphQL split (`public-private.md`)
81. Ship REST v1 subset (`REST-V1-SUBSET.md`) with gateway-shaped DTOs
82. OpenAPI generation + partner auth (API keys vs JWT)
83. Rate limiting + idempotency for public routes
84. Regenerate `GRAPHQL-SCHEMA.md` in CI when Strawberry types change
85. MCP module inventory under `backend/graphql.modules/` (future federation)
86. Webhook outbound design (Kafka fan-out)

---

### Phase 6 + 7 — Reliability & deployment (parallel)

**Phase 6**
87. Per-slice runbooks (Connectra down, enrichment failures, campaign backlog)
88. Kafka vs BullMQ boundary enforcement in new features
89. Circuit breakers / retries on satellite HTTP clients
90. Load testing plan for Connectra VQL + batch-upsert
91. Multi-AZ / DB replication strategy (stub → populated, ECS-first not EKS)

**Phase 7**
92. Terraform module structure + state backend
93. ECS service definitions for gateway, app, admin
94. EC2 satellite deploy playbooks (existing `deploy.yml` per service)
95. Secrets rotation policy
96. Environment promotion (dev → stage → prod)
97. Chrome Web Store release pipeline for extension

---

### Phase 9 — Ecosystem integrations

98. CRM sync adapters (HubSpot, Salesforce) — extension stubs in phase 4 foreshadow this
99. iPaaS / n8n automation docs (`backend/n8n/`)
100. OAuth integration service (no standalone repo yet)
101. Webhook receivers for inbound partner events
102. Platform productization (multi-tenant API keys, partner portal)

---

### Phase 11 — Lead generation & recommendations

103. Lead qualification framework + scoring model ownership (see `LEAD-ENRICHMENT-SPLIT.md`)
104. `crm.rank_leads` AI tool
105. Lookalike audiences + similar contacts (OpenSearch / embeddings)
106. Resume → hire-signal filter suggestions (already partially built)
107. Company health scoring (hiring, funding signals from `job.server`)
108. Recommendation engine event ingestion (Kafka `contact.*`, engagement)
109. Next-best-action recommendations (phase 3 activities + phase 5 AI)

---

## Suggested Sprint Groupings

If you want **thin vertical slices** rather than finishing whole phases:

| Sprint theme | Tasks (from above) | Outcome |
|--------------|-------------------|---------|
| **SN capture hardening** | 29–31, 37, 40–41 | Reliable LinkedIn → CRM save |
| **Contacts list excellence** | 21–23, 40 | VQL filters + pagination production-ready |
| **Enrichment MVP** | 52–58, 61 | Single-contact email find + verify with credits |
| **Billing MVP** | 42–48 | Trial → paid with credit gates |
| **Campaign MVP** | 63–68, 70 | One sequence, email send, progress SSE |
| **AI chat MVP** | 71–77 | SSE chat with read-only CRM tools |
| **Hiring signals** | 39, 106–107 | job.server + analytics dashboards complete |

---

## Doc vs Code Gap (Important)

Your documentation is **architecturally mature** but **implementation-backlog heavy**:

- **Strong:** `DECISIONS.md`, deployment matrix, backend endpoint parity, phase 3 spine, foundation flows
- **Weak:** Phases 1, 2, 5, 6, 7, 8, 9, 10, 11 are almost entirely `stub` markdown — treat `index.json` as a **work breakdown structure**, not finished specs
- **Rule:** Do not duplicate route tables in phase docs; link to `docs/backend/endpoints/*`

---

## What I’d Do First (If Starting Execution)

1. **Close foundation gaps** (CI green, `satelliteHealth`, local dev doc)
2. **Ship slice 3+4** (SN save E2E + VQL contacts list) — this unlocks everything else
3. **Layer billing** once enrichment/capture emit usage signals
4. **Enrichment + campaigns** before heavy AI and public API
5. **Reliability/deployment** in parallel once you have traffic to protect

---

I’m in **Ask mode**, so I can’t edit docs or run validation scripts. If you want me to turn this into a tracked backlog (populate specific stubs, verify index paths, or draft a sprint plan for one slice), switch to **Agent mode** and say which slice to start with (e.g. “Phase 3+4 SN capture” or “Phase 1 billing MVP”).

---

**User**

now think about user can add their bench candiates , then you fetch all details about those candiates and user can show all job according to candiates fetch details for every bench candiates , Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

I'll search the codebase and docs for bench candidates, resume handling, and job-matching flows so the task breakdown fits what Contact360 already has.


# Bench Candidates → Job Matching — Deep Analysis & Task Breakdown

This feature is a **candidate-centric inversion** of what Contact360 mostly has today: a **job-centric** hiring-signals product. The marketing copy already describes it (“Match your bench candidates to live urgent needs”), but the **product app does not yet model a bench roster or per-candidate job feeds**.

---

## What the User Wants (Product Flow)

```mermaid
flowchart LR
  subgraph add [1. Add bench candidates]
    Manual[Manual form]
    Resume[Resume PDF/DOCX]
    LinkedIn[LinkedIn URL]
    CRM[Existing Connectra contact]
  end

  subgraph enrich [2. Fetch full details]
    Parse[Resume parse → structured JSON]
    Profile[LinkedIn / profile scrape]
    EmailPhone[Email + phone enrichment]
    Derive[Derive skills, titles, seniority, location]
  end

  subgraph match [3. Jobs per candidate]
    Filters[Map profile → job.server filters]
    Score[Keyword / AI match score]
    Rank[Ranked job list per candidate]
  end

  subgraph ui [4. UI]
    Roster[Bench roster]
    Detail[Candidate detail + matched jobs]
    Outreach[Bench presentation email]
  end

  add --> enrich --> match --> ui
```

**User outcome:** A staffing/agency user maintains many **available consultants on the bench**, each with a rich profile, and sees **which open jobs fit each person** — not one resume that temporarily tweaks a global job search.

---

## What Already Exists in Contact360

| Building block | Where | Relevance |
|----------------|-------|-----------|
| **Job corpus** | `job.server` (Mongo, Apify ingest) | Titles, skills, seniority, `experience_bucket`, `skill_tags`, company cohorts |
| **Job listing API** | GraphQL `hireSignal.jobs` | Rich filters + `extendedJobFilters`; gateway merges user prefs |
| **Resume → filter suggest** | `suggestHireSignalFiltersFromResumeUpload` + `resume_suggest.py` | Extracts titles, locations, skills, education from **one** resume |
| **Resume import UI** | `HiringSignalsResumeImport.tsx` | Upload → suggests filters for **global** job search (user must Apply filters) |
| **Resume parse + store** | `scraper.server` `/resume/v1` (OpenSearch) | PDF/DOCX → markdown → structured `processed_data` |
| **Resume ↔ job score** | `GET /resume/v1/resumes/{resume_id}/score?job_id=` | Keyword-style `match_percentage` for **one** job at a time |
| **Hiring analytics** | `/hiring-signals`, `/demands-and-trends` | Job KPIs, not candidate roster |
| **Contacts / CRM** | Connectra | Could hold person records; no `bench` segment yet |
| **Saved searches** | `savedSearches` GraphQL | Saved **job** filter sets, not per-candidate |
| **Bench messaging** | Hiring landing (`Bench Presentation` template) | Marketing only |

### Critical gaps

1. **No `BenchCandidate` entity** — nothing in gateway Postgres or GraphQL for an org-scoped bench roster.
2. **Resume store is not multi-tenant** — OpenSearch resumes in `scraper.server` have no `org_id` / `user_id`.
3. **Resume import is one-shot** — parses once, suggests filters, does not persist a candidate or re-run matching later.
4. **No batch “jobs for candidate X” API** — only global `hireSignal.jobs` with manual filters.
5. **No enrichment orchestration for bench** — resume parse exists; LinkedIn profile fetch, email/phone, and Connectra link are not wired as a single bench pipeline.

---

## Recommended Domain Model

Introduce an **org-scoped Bench Candidate** in the **gateway** (RLS on `org_id`), not in Connectra alone — bench is a **product/workflow** concept; Connectra remains canonical contact storage when linked.

| Field | Purpose |
|-------|---------|
| `id`, `org_id`, `created_by` | Tenant isolation |
| `display_name`, `email`, `phone`, `linkedin_url` | Identity + outreach |
| `status` | `available` \| `interviewing` \| `placed` \| `on_hold` |
| `source` | `manual` \| `resume_upload` \| `linkedin` \| `connectra_contact` |
| `connectra_contact_uuid` | Optional CRM link |
| `resume_id` | Pointer to `scraper.server` parsed resume |
| `parsed_profile` | Cached JSON (titles, skills, education, locations) |
| `match_profile` | Normalized tokens for job.server (`titles`, `skillTags`, `seniority`, `experienceBucket`, `locations`) |
| `enrichment_status` | `pending` \| `processing` \| `ready` \| `failed` |
| `last_matched_at` | For refresh scheduling |

Optional: **`bench_candidate_job_match`** table — `(candidate_id, linkedin_job_id, match_score, matched_at)` for fast UI and “hide already pitched”.

---

## Matching Strategy (Two Tiers)

### Tier A — Filter mapping (MVP, fast)

Reuse and extend `suggest_hire_filters_from_resume_payload()`:

- Candidate profile → `titles`, `locations`, `extendedJobFilters` (`skillsAll`, `educationLevelMins`, `seniority`, `experience_bucket`)
- Call existing `hireSignal.jobs` with those filters per candidate
- **Pros:** Uses existing job.server + gateway stack  
- **Cons:** Boolean filter match, not true relevance ranking

### Tier B — Score ranking (v2, accurate)

1. Tier A returns top **N** jobs (e.g. 200)
2. For each job, store JD text in `scraper.server` `/resume/v1/jobs/upload` (or use job description from Mongo)
3. Call `GET /resumes/{resume_id}/score?job_id=` (already implements keyword match)
4. Sort by `match_percentage`; surface top 25 per candidate
5. Optional: AI rerank via `ai.server` for explanations (“matches React + AWS”)

This aligns with phase **11** (recommendations) and existing **Resume Matcher** on `scraper.server`.

---

## End-to-End Flow (Target Architecture)

```
User adds candidate (UI)
  → Gateway mutation createBenchCandidate
  → Enqueue enrichment job (BullMQ/Kafka or scheduler_jobs pattern)

Enrichment worker:
  1. If resume file → scraper.server upload + parse → resume_id + processed_data
  2. If linkedin_url → extension.server / Apify profile (optional)
  3. If missing email/phone → email.server / phone.server (credit-gated, phase 1)
  4. Optionally upsert Connectra contact (UUID5 from linkedin)
  5. Build match_profile (extend resume_suggest.py)
  6. Run job match (filter query + optional score pass)
  7. Persist bench_candidate_job_match rows
  8. SSE or poll status to UI

UI:
  Bench roster → select candidate → "Matched jobs" tab (reuse HiringSignalsDataTable columns)
```

---

## Task Breakdown (Small Steps)

### Phase A — Product & data design (1–2 days)

1. **Write ADR / DECISIONS entry** — bench candidate ownership (gateway Postgres), Connectra link optional, resume_id external ref.
2. **Define `BenchCandidate` JSON schema** — align with resume `processed_data` shape from scraper.
3. **Define `match_profile` mapping spec** — resume fields → `job.server` query params (mirror `DECISIONS.md` hire-signal filter rules).
4. **Define statuses & lifecycle** — available → placed; whether placed candidates stay visible.
5. **Credit policy** — which enrichment steps consume credits (phase 1 dependency).

### Phase B — Gateway persistence & API (3–5 days)

6. **Alembic migration** — `bench_candidates` + optional `bench_candidate_job_matches`.
7. **RLS policies** — `org_id = current_setting('app.current_org_id')`.
8. **Repository** — CRUD, list by org, filter by status.
9. **GraphQL types** — `BenchCandidate`, `BenchCandidateMatch`, connection types.
10. **Mutations:**
    - `createBenchCandidate` (manual)
    - `uploadBenchCandidateResume` (base64 → scraper → link resume_id)
    - `linkBenchCandidateToContact` (Connectra UUID)
    - `updateBenchCandidateStatus`
    - `deleteBenchCandidate`
    - `refreshBenchCandidateMatches` (re-run matching)
11. **Queries:**
    - `benchCandidates(limit, offset, status)`
    - `benchCandidate(id)`
    - `benchCandidateMatchedJobs(candidateId, limit, offset)` — ranked list
12. **Activity logging** — bench add / match refresh in gateway activity table.

### Phase C — Enrichment pipeline (5–8 days)

13. **Extend scraper resume store** — add `org_id`, `owner_user_id` on resume docs (or gateway-only mapping table if you want minimal scraper change).
14. **Enrichment orchestrator** — gateway `scheduler_jobs` or BullMQ worker (pattern: email/phone job polling).
15. **Step: resume parse** — proxy to `resume_ai_parse_upload` / scraper upload; wait until `processing_status=ready`.
16. **Step: build `parsed_profile`** — normalize scraper JSON (reuse `extract_resume_document`).
17. **Step: build `match_profile`** — extend `resume_suggest.py` with seniority, `experience_bucket`, `function_category` heuristics from years of experience.
18. **Step: optional LinkedIn** — if URL present, fetch title/company via existing extension or `job.server` profile scrape.
19. **Step: optional Connectra upsert** — batch-upsert contact from bench fields (phase 3 UUID5 rules).
20. **Step: optional email/phone** — email.server finder when name+company/domain known.
21. **Error handling** — partial success (resume ok, LinkedIn failed); surface per-field errors in UI.
22. **Idempotency** — re-upload resume updates same candidate, not duplicate row.

### Phase D — Job matching engine (4–6 days)

23. **Filter mapper service** — `match_profile` → `JobListFilters` (same shape as `useHiringSignals`).
24. **Per-candidate job query** — internal call to `JobServerClient` with mapped filters + org prefs (hidden companies).
25. **Match persistence** — store `(candidate_id, job_id, score, filter_rank)`.
26. **Score pass (v2)** — batch score top N via scraper `resume_score_vs_job`; rate-limit LLM/keyword extraction.
27. **Incremental refresh** — cron: new jobs since `last_matched_at` → append matches; optional Kafka `job.ingested` consumer.
28. **Dedup** — don’t re-surface jobs user marked `applied` via `hire_signal_prefs`.
29. **Explainability** — return `match_reasons[]` (matched skills, title overlap) for UI chips.

### Phase E — Dashboard UI (5–7 days)

30. **New route** — `/bench` or hiring-signals sub-tab **“My bench”**.
31. **Bench roster table** — name, status, skills summary, match count, last refreshed, enrichment status.
32. **Add candidate modal** — tabs: Manual | Upload resume | Import from contacts | LinkedIn URL.
33. **Bulk upload** — multi-file resume drop → queue multiple candidates.
34. **Candidate detail drawer** — profile sections (experience, skills, education) from `parsed_profile`.
35. **Matched jobs panel** — reuse `HiringSignalsDataTable` / job row components; show `match_score` column.
36. **Actions** — “Refresh matches”, “Mark job pitched”, “Open job description”, “Bench presentation email”.
37. **Empty / loading states** — enrichment in progress spinner; failed parse retry.
38. **Wire outreach template** — port “Bench Presentation” from hiring landing into editable email (phase 10-ish).

### Phase F — Ops, credits, compliance (2–4 days)

39. **SLO** — bench enrichment p95 &lt; 60s; match refresh p95 &lt; 10s for filter-only tier.
40. **Audit** — who uploaded resume; don’t log raw resume bytes (`DECISIONS.md` hiring resume rule).
41. **PII** — bench data in gateway Postgres; retention policy; right-to-delete cascades resume in scraper.
42. **Credits** — charge per resume parse, enrichment, match refresh (phase 1 meters).
43. **Runbook** — scraper LLM down → `processing_status=failed` UX.

### Phase G — Docs & phase alignment (ongoing)

44. **Phase 11 stub** — populate “lead qualification / recommendation” with bench→job slice.
45. **Phase 3** — contact tags/segments: `tag:bench` for Connectra-linked candidates.
46. **Phase 4** — optional: add bench candidate from LinkedIn extension save.
47. **Update `hiring-analytics.md`** — bench KPIs (candidates on bench, avg matches, placement rate).

---

## Suggested MVP Slice (Smallest Shippable Version)

Ship in this order to validate the loop quickly:

| Step | Deliverable |
|------|----------------|
| **MVP-1** | Gateway `bench_candidates` table + `createBenchCandidate` + `uploadBenchCandidateResume` |
| **MVP-2** | On upload: parse resume → save `match_profile` using extended `resume_suggest` |
| **MVP-3** | `benchCandidateMatchedJobs` = one `hireSignal.jobs` call with mapped filters (no score yet) |
| **MVP-4** | UI: bench list + candidate drawer + matched jobs table |
| **MVP-5** | Manual refresh + match count badge |
| **v2** | Scraper score ranking + scheduled nightly re-match |
| **v3** | Connectra link + email enrichment + Bench Presentation outreach |

---

## How This Maps to Your Phase Roadmap

| Phase | Role in bench feature |
|-------|----------------------|
| **3** | Connectra contact link, UUID5, optional bench segment |
| **2** | Email/phone enrichment for candidates |
| **1** | Credits for parse/enrich/match refresh |
| **11** | Recommendation engine, ranking, next-best-job |
| **4** | LinkedIn capture → add to bench from extension |
| **10** | Outreach templates (“Bench Presentation”) |
| **5** | AI explanations + conversational “find jobs for Priya” |
| **6** | SLOs + runbooks for enrichment/matching workers |

Per your handoff doc, this feature is primarily **Phase 11 + hiring-signals (job.server) + scraper resume**, with dependencies on **3** (contacts) and **1** (credits) for production hardening.

---

## Key Design Choices to Decide Early

1. **Bench vs CRM contact** — Is every bench candidate also a Connectra contact, or only on placement?
2. **Resume tenancy** — Add `org_id` to scraper OpenSearch vs gateway-only `resume_id` mapping table?
3. **Matching default** — Filter-only MVP vs score-ranked from day one?
4. **Refresh model** — On-demand only vs daily cron when new jobs ingest?
5. **UI placement** — Separate `/bench` vs tab inside `/hiring-signals`?

---

## Summary

Contact360 already has **~70% of the plumbing** (resume parse, job corpus, filter mapping, single-resume suggest, per-job score API, hiring-signals UI components). What’s missing is the **persistent, org-scoped bench roster**, an **enrichment orchestrator per candidate**, and a **per-candidate job feed** (inverted query model).

The work breaks naturally into: **(A) data model → (B) GraphQL API → (C) enrichment pipeline → (D) matching engine → (E) UI**, with MVP achievable by wiring resume upload + `resume_suggest` → `hireSignal.jobs` before adding score-based ranking.

If you want this implemented, switch to **Agent mode** and say whether you prefer MVP at `/bench` or as a tab under `/hiring-signals` — that choice affects the first UI tasks.

---

**User**

in  @contact360.io/app  ,   create a route for /candiates where user can add bench candiates by giving candiate name and linkdin url and saved in candiate table in postgess via @contact360.io/api  in job modular , Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

I'll trace how routes and API modules are set up in the app and API, and check whether a candidates table or job-module pattern already exists.


# `/candidates` bench route — analysis & task breakdown

You want: **`contact360.io/app` → `/candidates`** where a user enters **name + LinkedIn URL**, persisted in **Postgres** via **`contact360.io/api`**.

Below is how that fits the repo today, where to put the API (important: not the scheduler `jobs` module), and a step-by-step build plan.

---

## Current state (nothing built yet)

| Layer | Status |
|-------|--------|
| **App route** `/candidates` | Does not exist (`routes.ts` has `/hiring-signals`, `/contacts`, etc.) |
| **Postgres `candidates` table** | Does not exist (no model in `app/models/`) |
| **GraphQL CRUD for bench candidates** | Does not exist |
| **Nav entry** | Not in `navConfig.ts` |

**What does exist (reuse patterns):**

- **Hiring signals** — `hireSignal` GraphQL → `job.server` (job listings, not candidates)
- **User-scoped Postgres tables** — `hire_signal_prefs`, `saved_searches` (same scoping model you want)
- **LinkedIn URL helper** — `linkedin_slug()` in `connectra_helpers.py`
- **Resume → job filters** — `suggestHireSignalFiltersFromResumeUpload` (future enrichment)
- **Profile scrape docs** — `EC2/job.server/docs/LinkedIn Profile Scraper*.md` (future “fetch all details”)

---

## Critical: which “job module”?

In this codebase there are **two different “job” concepts**:

| Module | Path | Purpose |
|--------|------|---------|
| **`jobs`** | `app/graphql/modules/jobs/` | **Scheduler jobs** — CSV export/import, email verify, `scheduler_jobs` table |
| **`hireSignal`** | `app/graphql/modules/hire_signal/` | **Hiring signals** — `job.server` listings, scrape runs, resume filter suggest |

Bench candidates belong with **hiring / staffing**, not scheduler jobs.

**Recommendation:**

- **Postgres + GraphQL:** extend **`hire_signal`** (same product area), **or** add a small sibling module `bench_candidates` / `candidates` and wire it in `schema.py` as `candidates: CandidateQuery`.
- **Do not** put bench CRUD in `jobs` — that module is for async export/import tickets.

If you said “job module” meaning **job.server / hiring**, use **`hireSignal`** (e.g. `hireSignal.createCandidate`) or a dedicated **`candidates`** root field for clarity with the `/candidates` route.

---

## Target architecture (MVP)

```mermaid
sequenceDiagram
  participant UI as app /candidates
  participant GW as api GraphQL
  participant PG as Postgres candidates

  UI->>GW: createCandidate(name, linkedinUrl)
  GW->>GW: require_auth + validate URL
  GW->>PG: INSERT user_id, name, linkedin_url, linkedin_slug
  PG-->>GW: row
  GW-->>UI: Candidate { id, name, linkedinUrl, createdAt }

  UI->>GW: candidates(limit, offset)
  GW->>PG: SELECT WHERE user_id = current user
  GW-->>UI: CandidateList
```

**Out of scope for MVP** (later): Apify profile scrape, resume upload, job matching per candidate.

---

## Suggested Postgres schema

Follow `hire_signal_prefs` / `saved_searches`: **`user_id`** scoping (no `org_id` on gateway models today).

**Table:** `bench_candidates` or `candidates` (pick one name; `bench_candidates` avoids confusion with Connectra “contacts”)

| Column | Type | Notes |
|--------|------|--------|
| `id` | `TEXT` PK | `uuid4()` |
| `user_id` | `TEXT` FK → `users.uuid` | CASCADE delete |
| `name` | `TEXT` NOT NULL | Display name user typed |
| `linkedin_url` | `TEXT` NOT NULL | Normalized on write |
| `linkedin_slug` | `TEXT` | From `linkedin_slug()` — dedup / future scrape |
| `status` | `TEXT` | Default `available` (optional MVP) |
| `created_at` | `timestamptz` | `server_default=now()` |
| `updated_at` | `timestamptz` | nullable, on update |

**Constraints (recommended):**

- `UNIQUE (user_id, linkedin_slug)` — same person not added twice per user
- Index on `user_id`

**Model file:** `contact360.io/api/app/models/bench_candidate.py`  
**Repository:** `app/repositories/bench_candidate.py`  
**Migration:** new Alembic revision (pattern: `20260429_0016_hire_signal_user_prefs.py`)

Register model in `app/models/__init__.py`.

---

## API design (GraphQL)

Place under **`hireSignal`** or new **`candidates`** namespace in `schema.py`.

### Types (`hire_signal/types.py` or `candidates/types.py`)

```graphql
type BenchCandidate {
  id: ID!
  name: String!
  linkedinUrl: String!
  linkedinSlug: String
  status: String
  createdAt: DateTime!
  updatedAt: DateTime
}

type BenchCandidateList {
  items: [BenchCandidate!]!
  total: Int!
}
```

### Mutations

| Mutation | Input | Behavior |
|----------|--------|----------|
| `createBenchCandidate` | `name`, `linkedinUrl` | Validate, normalize URL, insert |
| `updateBenchCandidate` | `id`, `name?`, `linkedinUrl?` | Owner check |
| `deleteBenchCandidate` | `id` | Owner check |

### Queries

| Query | Args | Behavior |
|-------|------|----------|
| `benchCandidates` | `limit`, `offset` | List for `user.uuid`, order `created_at DESC` |
| `benchCandidate` | `id` | Single row, 403 if not owner |

### Validation rules

1. **`name`** — non-empty, max 255 (`validate_string_length`)
2. **`linkedin_url`** — must look like LinkedIn profile:
   - Accept `https://www.linkedin.com/in/...` (and `http`, `www` variants)
   - Reject company URLs `/company/` for MVP (or allow with warning)
3. **Normalize** — store canonical URL; compute `linkedin_slug` via existing helper:

```465:488:contact360.io/api/app/utils/connectra_helpers.py
def linkedin_slug(raw_url: str | None) -> str:
    """Extract company/person slug from a LinkedIn URL (job.server compatible)."""
    ...
    for path_prefix in ("/company/", "/in/"):
        if s.startswith(path_prefix):
            s = s[len(path_prefix) :]
```

4. **Auth** — `require_auth(info.context.user)` on every resolver (same as `saved_searches`)

5. **Activity log** (optional MVP+) — `ActivityServiceType` entry; may need enum extension in migration like `hire_signal` activity type

### Schema registration

In `app/graphql/schema.py`:

```python
# Query
candidates: CandidateQuery = strawberry.field(resolver=lambda: CandidateQuery())

# Mutation  
candidates: CandidateMutation = strawberry.field(resolver=lambda: CandidateMutation())
```

Or nest under existing `hireSignal` to avoid new root fields.

### Docs / governance

Same PR should update:

- `docs/DECISIONS.md` — if new GraphQL fields are external contract
- `docs/backend/endpoints/contact360.io/` — if you document gateway-only tables
- Regenerate or patch `GRAPHQL-SCHEMA.md` per `DOC-GATE-CHECKLIST.md`

---

## App: `/candidates` route

**Spelling:** use **`/candidates`** (not `/candiates`) in `ROUTES` and filesystem.

### File layout (match hiring-signals pattern)

| File | Purpose |
|------|---------|
| `app/app/(dashboard)/candidates/page.tsx` | Thin page → client component |
| `src/components/feature/candidates/CandidatesPageClient.tsx` | Main UI |
| `src/components/feature/candidates/AddCandidateForm.tsx` | Name + LinkedIn URL form |
| `src/components/feature/candidates/CandidatesTable.tsx` | List with delete |
| `src/services/graphql/candidatesService.ts` | `gql` + `graphqlMutation` / `graphqlQuery` |

**Page shell** (same as hiring-signals):

```1:11:contact360.io/app/app/(dashboard)/hiring-signals/page.tsx
import { Suspense } from "react";
import HiringSignalsPageClient from "@/components/feature/hiring-signals/HiringSignalsPageClient";
import { ShellSuspenseFallback } from "@/components/shared/ShellSuspenseFallback";

export default function HiringSignalsPage() {
  return (
    <Suspense fallback={<ShellSuspenseFallback />}>
      <HiringSignalsPageClient />
    </Suspense>
  );
}
```

### Routing & nav

1. **`src/lib/routes.ts`** — `CANDIDATES: "/candidates"`
2. **`src/lib/navConfig.ts`** — under **Database** section, after Hiring Signals:

   ```ts
   { href: ROUTES.CANDIDATES, label: "Bench Candidates", icon: "UserCheck" }
   ```

3. **`NavCommandPalette`** — picks up via `NAV_SEARCH_INDEX` automatically

### UI behavior (MVP)

1. **Header** — “Bench candidates” + short subtitle
2. **Add form** — `name` (text), `linkedinUrl` (url), Submit
3. **On submit** — `createBenchCandidate` → toast success → refetch list
4. **Table** — name, LinkedIn link (external), created date, delete action
5. **Empty state** — “Add your first bench candidate”
6. **Errors** — duplicate slug → “This LinkedIn profile is already on your bench”

Use existing primitives: `DashboardPageLayout`, `DataPageLayout`, `Button`, `Input`, `toast` from `sonner` (see `HiringSignalsResumeImport.tsx`).

### GraphQL client example shape

```typescript
const CREATE_BENCH_CANDIDATE = gql`
  mutation CreateBenchCandidate($name: String!, $linkedinUrl: String!) {
    hireSignal {
      createBenchCandidate(name: $name, linkedinUrl: $linkedinUrl) {
        id
        name
        linkedinUrl
        createdAt
      }
    }
  }
`;
```

(Adjust path if you use root `candidates` instead of `hireSignal`.)

---

## Task breakdown (small steps)

### A — API: database & model (≈ half day)

1. Add Alembic migration `bench_candidates` table + indexes + unique constraint  
2. Add SQLAlchemy model `BenchCandidate`  
3. Import model in `models/__init__.py`  
4. Add `BenchCandidateRepository` — `insert`, `list_by_user`, `get_by_id`, `delete_by_id`, `update`  
5. Unit test repository (optional but useful)

### B — API: GraphQL (≈ 1 day)

6. Add Strawberry types + `from_model` mapper  
7. Add `CreateBenchCandidateInput` (if using input object)  
8. Implement `createBenchCandidate` mutation — validation + slug + duplicate handling  
9. Implement `benchCandidates` query with pagination (`validate_pagination`)  
10. Implement `benchCandidate(id)` query  
11. Implement `deleteBenchCandidate` mutation  
12. Wire into `schema.py` under `hireSignal` or new `candidates`  
13. Add API tests (auth required, owner-only, duplicate URL)  
14. Run Alembic upgrade locally  
15. Update GraphQL schema doc / DECISIONS if required

### C — App: route & service (≈ half day)

16. Add `ROUTES.CANDIDATES`  
17. Create `candidates/page.tsx`  
18. Create `candidatesService.ts` with create + list + delete operations  
19. Add client-side LinkedIn URL format check (UX only; server is source of truth)

### D — App: UI (≈ 1 day)

20. `CandidatesPageClient` — layout + data fetch on mount  
21. `AddCandidateForm` — controlled inputs, loading state, validation messages  
22. `CandidatesTable` — rows, open LinkedIn in new tab, delete with confirm  
23. Wire toasts for success/error  
24. Loading / empty / error states

### E — Nav & polish (≈ 2 hours)

25. Add sidebar nav entry  
26. Quick manual E2E: login → add candidate → see row → refresh → delete  
27. Optional: link from hiring-signals page (“Manage bench”)

### F — Future (not MVP; aligns with your earlier vision)

28. **Enrichment job** — on create, enqueue `job.server` Apify profile scrape (`RunProfileScrape`)  
29. Store `profile_json` on candidate row  
30. **Matched jobs** — map profile → `hireSignal.jobs` filters  
31. Resume upload column + link to `scraper.server`  
32. Connectra contact link (`connectra_contact_uuid`)  
33. Org-level bench (when multi-tenant `org_id` lands)

---

## Module placement decision

| Option | Pros | Cons |
|--------|------|------|
| **`hireSignal.createBenchCandidate`** | No new root schema field; hiring domain stays together | `hireSignal` already large |
| **Root `candidates` module** | Matches `/candidates` URL; clear API | Extra wiring in `schema.py` |
| **`jobs` module** | — | **Wrong domain** (scheduler only) |

**Practical MVP:** root **`candidates`** GraphQL module + table `bench_candidates` — clearest for app and future job-matching features.

---

## Alignment with `job.server` profile docs

You have Apify profile scraper docs open under `EC2/job.server/docs/`. For **“fetch all details”** after save:

- MVP only stores name + URL  
- **Phase 2:** mutation triggers profile scrape; updates `enrichment_status`, `profile_snapshot` JSON  
- Reuse gateway → `JobServerClient` patterns already used in `hire_signal` mutations  

That stays separate from the **`jobs`** scheduler module.

---

## Summary

To ship **`/candidates` with name + LinkedIn URL → Postgres**:

1. New table + model + repository in **`contact360.io/api`**  
2. GraphQL on **`hireSignal`** or new **`candidates`** module — **not** `jobs`  
3. New dashboard route + form + table in **`contact360.io/app`**  
4. Nav entry in **`navConfig.ts`**

I'm in **Ask mode**, so I can't implement this. Switch to **Agent mode** if you want it built; say whether you prefer GraphQL under **`hireSignal`** or a top-level **`candidates`** field, and whether the table should be named `candidates` or `bench_candidates`.

---

**User**

in @EC2/job.server  , after user saved all candiates , you fetch candiate details by apify actors like
1.  candiate  linkdin full details @EC2/job.server/docs/LinkedIn Profile Scraper + Email ✅ No Cookies.md   and upsert record in contact_index and saved full details in new contact_index_v1 in open sreach with same contact uuid  
2.  candiate  linkdin post details @EC2/job.server/docs/LinkedIn Profile Posts Scraper (No Cookies).md   and saved full details in new contact_index_post in open sreach with same contact uuid  
1.  candiate  linkdin comment details @EC2/job.server/docs/LinkedIn Profile Comments Scraper ✅ (No Cookies).md  and saved full details in new contact_index_post in open sreach with same contact uuid  
1.  candiate  linkdin reaction details @EC2/job.server/docs/LinkedIn Profile Reactions Scraper ✅ (No Cookies).md  and saved full details in new contact_index_post in open sreach with same contact uuid  
Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

I'll map how job.server uses Apify and OpenSearch today, then align that with your four actor flows and index naming.


# Bench candidate Apify enrichment in `job.server` — analysis & task breakdown

This extends the earlier **gateway Postgres bench list** (name + LinkedIn URL) with an **async enrichment pipeline** in `EC2/job.server`: four Apify actors, dual writes to OpenSearch, all tied to one **contact UUID**.

---

## What you want (end state)

```mermaid
flowchart TB
  subgraph save [Already planned / gateway]
    PG[(bench_candidates Postgres)]
  end

  subgraph trigger [job.server]
    API[POST enrich bench batch]
    Orch[BenchEnrichmentOrchestrator]
  end

  subgraph apify [Apify actors]
    P[Profile + Email LpVuK3Zozwuipa5bp]
    Po[Posts A3cAPGpwBEG8RJwse]
    C[Comments FiHYLewnJwS6GnRpo]
    R[Reactions VMwB47uSx3g2wCcBK]
  end

  subgraph os [OpenSearch]
    CI[contacts_index slim CRM]
    CV1[contacts_index_v1 full profile]
    CP[contact_index_post]
    CC[contact_index_comment]
    CR[contact_index_reaction]
  end

  PG --> API --> Orch
  Orch --> P --> CI
  P --> CV1
  Orch --> Po --> CP
  Orch --> C --> CC
  Orch --> R --> CR
```

**Index naming note:** You listed comments and reactions as `contact_index_post` twice. Use **separate indices**:

| Data | Suggested index |
|------|-----------------|
| Slim CRM row | `contacts_index` (existing, shared with Connectra) |
| Full profile JSON | `contacts_index_v1` (new) |
| Posts | `contact_index_post` (new) |
| Comments | `contact_index_comment` (new) |
| Reactions | `contact_index_reaction` (new) |

---

## What `job.server` already has

### 1. Profile scrape (partial — not your target design)

`RunProfileScrape` in `internal/services/apify_service.go`:

- Endpoint: `POST /api/v1/runs/profile` → Asynq `apify:start_profile_scrape`
- Actor: `APIFY_ACTOR_LINKEDIN_PROFILE_SCRAPER` (default `snipercoder/bulk-linkedin-email-finder`), **not** the doc actor `LpVuK3Zozwuipa5bp`
- Input: `linkedin_url_or_ids` — **not** `queries` + `profileScraperMode` from your doc
- **Reads** `contacts_index` to skip URLs already present
- **Writes** only to `linkedin_profiles_index` via `LinkedInProfileRepo` (raw Mongo-shaped docs, doc id = LinkedIn URL)
- **Does not** upsert `contacts_index` after Apify
- **Does not** write `contacts_index_v1`

### 2. Connectra / OpenSearch bridge (reusable)

`ConnectraBridge` + `OSBulkUpsertContacts` in `internal/clients/opensearch_contacts_companies.go`:

- `contacts_index` = shared B2B index (`IndexConnectraContacts`)
- UUID5 from LinkedIn slug via `GenerateUUID5` / `LinkedInSlug` (Connectra-compatible)
- `prepareContactDoc` sets `uuid`, `linkedin_slug`, timestamps

### 3. Apify infrastructure (reusable)

- `ApifyClient`: `StartRunForActor`, poll, `ListDatasetItems`
- `ApifyRunRepo` → `apify_runs_index`
- Asynq queue `QueueApify`, worker in `internal/worker/register.go`

### 4. Missing entirely

- Bench candidate source in job.server (no table/collection yet)
- Posts / comments / reactions actors
- New OpenSearch indices (`contacts_index_v1`, `contact_index_*`)
- Orchestrator that runs profile → then social signals per candidate
- Gateway → job.server hook after “save all candidates”

---

## Apify actors (from your docs)

| # | Actor ID | Input shape | Output use |
|---|----------|-------------|------------|
| 1 Profile | `LpVuK3Zozwuipa5bp` | `queries[]`, `profileScraperMode` | Slim → `contacts_index`; full → `contacts_index_v1` |
| 2 Posts | `A3cAPGpwBEG8RJwse` | `targetUrls[]`, `maxPosts`, flags | Many docs → `contact_index_post` |
| 3 Comments | `FiHYLewnJwS6GnRpo` | `profiles[]`, `maxItems` | Many docs → `contact_index_comment` |
| 4 Reactions | `VMwB47uSx3g2wCcBK` | `profiles[]`, `maxItems` | Many docs → `contact_index_reaction` |

Add to `config.go` / `.env.example`:

```env
APIFY_ACTOR_LINKEDIN_PROFILE_DETAILS=LpVuK3Zozwuipa5bp
APIFY_ACTOR_LINKEDIN_PROFILE_POSTS=A3cAPGpwBEG8RJwse
APIFY_ACTOR_LINKEDIN_PROFILE_COMMENTS=FiHYLewnJwS6GnRpo
APIFY_ACTOR_LINKEDIN_PROFILE_REACTIONS=VMwB47uSx3g2wCcBK
```

Keep the old profile actor env var only if you still need email-finder bulk runs.

---

## Contact UUID strategy (critical)

All indices must share the **same `contact_uuid`**:

1. Normalize URL: `utils.CleanLinkedInURL`
2. Slug: `clients.LinkedInSlug`
3. UUID: `clients.GenerateUUID5(slug)` — matches Connectra `EXTENSION_SCRAPER_UUID5` rules

**`contacts_index` document `_id`:** use `uuid` (bulk upsert already does via `contactUUIDFromDoc`).

**`contacts_index_v1`:** one doc per contact — `_id` = `uuid`, body includes `raw_apify_profile` + metadata.

**Posts / comments / reactions:** many rows per contact:

- `_id` = stable id from Apify (`activityUrn`, comment id, reaction id, or hash)
- Required field: `contact_uuid` (for filtering)
- Optional: `linkedin_url`, `ingested_at`, `apify_run_id`

---

## Profile step: dual write

### A. Slim upsert → `contacts_index`

Map Apify profile item → minimal contact doc (example fields):

```go
{
  "first_name": item["firstName"],
  "last_name":  item["lastName"],
  "linkedin_url": cleanURL,
  "email":      firstValidEmail(item["emails"]),
  "title":      headlineOrCurrentPosition,
  "city":       location.parsed.city,
  "country":    location.parsed.country,
  // company_id: resolve via company LinkedIn URL → companies_index upsert if needed
}
```

Call `clients.OSBulkUpsertContacts` → returns `contact_uuids[]`.

### B. Full payload → `contacts_index_v1`

```go
{
  "uuid": contactUUID,
  "linkedin_url": cleanURL,
  "linkedin_slug": slug,
  "source": "apify_profile",
  "apify_actor_id": "...",
  "apify_run_id": runID,
  "raw_payload": item,  // entire Apify JSON
  "fetched_at": RFC3339,
}
```

Use `dynamic: false` mapping with `raw_payload` as `object` + `enabled: false` or store as flattened keyword/text fields you query often (skills, headline, emails).

---

## Orchestration design

### Trigger

After user saves bench candidates (gateway):

1. Gateway calls job.server e.g. `POST /api/v1/bench-candidates/enrich` with `{ "candidates": [{ "id", "name", "linkedinUrl" }] }`
2. Or gateway stores rows and job.server polls — prefer **explicit enqueue** on save

### State machine (Mongo or OpenSearch `bench_enrichment_jobs`)

Per candidate:

| Field | Values |
|-------|--------|
| `bench_candidate_id` | gateway id |
| `contact_uuid` | set after profile step |
| `profile_status` | pending / running / done / failed |
| `posts_status` | … |
| `comments_status` | … |
| `reactions_status` | … |
| `last_error` | string |

### Task graph (Asynq)

```
apify:bench_enrich_batch          → fan-out per candidate
  apify:bench_profile_scrape      → profile actor → contacts_index + contacts_index_v1
  apify:bench_posts_scrape        → depends on profile (needs URL + uuid)
  apify:bench_comments_scrape     → parallel with posts
  apify:bench_reactions_scrape    → parallel with posts
```

**Ordering:** Profile **must** run first (establishes `contact_uuid` and validates URL). Posts/comments/reactions can run **in parallel** after profile succeeds.

**Idempotency:** Before Apify, check `contacts_index_v1` for `uuid` + fresh `fetched_at` (e.g. TTL 7d) to skip re-scrape.

---

## Task breakdown (small steps)

### Phase 0 — Design & contracts

1. Fix index names in a short ADR (`contacts_index_v1`, `contact_index_post`, `_comment`, `_reaction`).
2. Document UUID5 rules (link to Connectra `EXTENSION_SCRAPER_UUID5.md`).
3. Define gateway ↔ job.server payload (`bench_candidate_id`, `name`, `linkedin_url`, `org_id`/`user_id` if needed).
4. Update `docs/DECISIONS.md` § job.server with new indices and actors.
5. Cost model: profile mode `$10/1k` with email vs `$4/1k` without — pick default env mode.

### Phase 1 — OpenSearch indices

6. Add constants in `opensearch.go`:
   - `IndexContactsV1 = "contacts_index_v1"`
   - `IndexContactPosts = "contact_index_post"`
   - `IndexContactComments = "contact_index_comment"`
   - `IndexContactReactions = "contact_index_reaction"`
7. Add `EnsureOpenSearchIndexes` mappings (`dynamic: false`, keyword `contact_uuid`, date `fetched_at`).
8. Implement `OSUpsertContactV1`, `OSBulkIndexContactPosts`, etc. (bulk `_bulk` with deterministic `_id`).
9. Add `OSGetContactV1ByUUID` for UI/debug.

### Phase 2 — Config & Apify inputs

10. Extend `config.Config` with four actor env vars.
11. Add input builders per actor (match doc JSON exactly).
12. Add mappers: `MapApifyProfileToContactDoc`, `MapApifyProfileToV1Doc`.
13. Add mappers for post/comment/reaction items → OS docs + `contact_uuid`.

### Phase 3 — Refactor / replace profile scrape

14. New `RunBenchProfileScrape(ctx, contactUUID, linkedinURL)` (or derive UUID inside).
15. Switch actor to `LpVuK3Zozwuipa5bp` with `queries` + `profileScraperMode` from env.
16. After dataset ingest:
    - `OSBulkUpsertContacts` (slim)
    - `OSUpsertContactV1` (full)
17. Optionally upsert employer to `companies_index` from `currentPosition[].companyLinkedinUrl`.
18. Deprecate or keep `linkedin_profiles_index` for backward compat (recommend: write both during migration).

### Phase 4 — Posts / comments / reactions scrapers

19. `RunBenchPostsScrape(ctx, contactUUID, linkedinURL)`.
20. `RunBenchCommentsScrape` — actor `FiHYLewnJwS6GnRpo`.
21. `RunBenchReactionsScrape` — actor `VMwB47uSx3g2wCcBK`.
22. Shared helper: `pollApifyRunAndIngest` (extract from `RunProfileScrape`).
23. Record each run in `apify_runs_index` with `enrichment_kind` metadata.

### Phase 5 — Orchestrator & API

24. Mongo model `BenchCandidateEnrichment` (or reuse gateway Postgres via API only).
25. Asynq payloads: `BenchEnrichBatchPayload`, `BenchEnrichOnePayload`.
26. Handler `handleBenchEnrich` in `worker/register.go`.
27. `POST /api/v1/bench-candidates/enrich` — enqueue batch.
28. `GET /api/v1/bench-candidates/:id/enrichment-status` — poll statuses.
29. Optional: `POST /api/v1/bench-candidates/:id/retry` per failed stage.

### Phase 6 — Gateway integration

30. After `createBenchCandidate` (gateway), call job.server enrich endpoint with `JOB_SERVER_API_KEY`.
31. Store `contact_uuid` on `bench_candidates` row when enrichment completes (webhook or poll).
32. GraphQL field `benchCandidate.enrichmentStatus` proxied from job.server.

### Phase 7 — App UI

33. On `/candidates` list: show enrichment badges (profile / posts / comments / reactions).
34. Candidate detail drawer: tabs for profile (v1), posts, comments, reactions (read from job.server or gateway GraphQL).
35. “Enrich all” / “Retry failed” buttons.

### Phase 8 — Ops & quality

36. Rate limits: max concurrent Apify runs per org (Redis semaphore).
37. Retries: Asynq `MaxRetry(3)` with backoff; don’t retry 4xx Apify input errors.
38. Logging: `X-Request-ID` from gateway; log `contact_uuid`, `apify_run_id`.
39. SLO: profile p95 &lt; 3 min; full social bundle p95 &lt; 10 min.
40. Runbooks: Apify token exhausted, OpenSearch bulk failure, LinkedIn URL invalid.

### Phase 9 — Docs & parity

41. `docs/backend/endpoints/job.server/ROUTE-CLIENT-MATRIX.md` — new routes.
42. Postman collection for bench enrich.
43. `SATELLITE-PARITY.md` / gateway `JobServerClient` methods.

---

## Important gaps vs current `RunProfileScrape`

| Your requirement | Current code |
|------------------|--------------|
| Actor `LpVuK3Zozwuipa5bp` | Uses `snipercoder/bulk-linkedin-email-finder` |
| Input `queries` + `profileScraperMode` | Uses `linkedin_url_or_ids` |
| Upsert `contacts_index` | Only reads; no write after Apify |
| `contacts_index_v1` full JSON | Not implemented |
| Posts / comments / reactions | Not implemented |
| Same `contact_uuid` everywhere | Profile repo uses URL as doc id in `linkedin_profiles_index` |

**Recommendation:** Add a **new bench enrichment path** rather than overloading `RunProfileScrape`, so hiring-signal profile runs stay stable while bench uses the four-actor pipeline.

---

## Suggested MVP slices

| Slice | Deliverable |
|-------|-------------|
| **MVP-1** | Indices + profile actor only → `contacts_index` + `contacts_index_v1` |
| **MVP-2** | `POST /bench-candidates/enrich` + status API |
| **MVP-3** | Posts index + actor |
| **MVP-4** | Comments + reactions (parallel) |
| **MVP-5** | Gateway + `/candidates` UI status |

---

## Data model sketch (`contacts_index_v1`)

```json
{
  "uuid": "same-as-contacts_index",
  "linkedin_url": "https://www.linkedin.com/in/...",
  "linkedin_slug": "rgupteswardora",
  "display_name": "R Gupteswar Dora",
  "headline": "Data engineer 1 at Deloitte",
  "emails": ["gdora@deloitte.com"],
  "skills": ["Apache Spark", "Airflow"],
  "raw_payload": { },
  "apify_run_id": "...",
  "fetched_at": "2026-06-14T..."
}
```

Post/comment/reaction docs always include `"contact_uuid": "<uuid>"` for `term` queries from the app.

---

## Summary

`job.server` already has **Apify orchestration**, **OpenSearch bulk upsert to `contacts_index`**, and **UUID5 parity with Connectra**. It does **not** yet implement your four-actor bench pipeline or the new indices.

The work splits into: **(1) OpenSearch index design → (2) per-actor runners + mappers → (3) bench orchestrator → (4) HTTP API → (5) gateway trigger after save → (6) UI**.

I'm in **Ask mode** and can't implement this. Switch to **Agent mode** if you want MVP-1 (profile dual-write + enrich endpoint) started first.

---

**User**

in  @contact360.io/app  ,   create a route for /candiates/uuid where user can show full deatails about candiate and then show jobs according to candiate details  via @contact360.io/api  in job modular from @EC2/job.server @EC2/scraper.server  , Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

I'll trace how candidate detail and job-matching data flows through the app, API gateway, job.server, and scraper.server.


# `/candidates/[uuid]` — detail page + matched jobs (deep analysis)

This page sits on top of the stack you’ve been designing:

1. **`/candidates`** — bench list (name + LinkedIn URL → gateway Postgres)  
2. **`job.server`** — Apify enrichment → `contacts_index`, `contacts_index_v1`, social indices  
3. **`/candidates/[uuid]`** — full candidate view + jobs matched from their profile  

Below: what exists today, recommended architecture, and a step-by-step task list.

---

## What the page must do

```mermaid
flowchart LR
  subgraph app [contact360.io/app]
    List["/candidates"]
    Detail["/candidates/uuid"]
  end

  subgraph api [contact360.io/api GraphQL]
    BQ[benchCandidate query]
    MJ[benchCandidateMatchedJobs]
    PD[benchCandidateProfile bundle]
  end

  subgraph job [EC2/job.server]
    OSv1[contacts_index_v1]
    OSp[contact_index_post]
    OSC[contact_index_comment]
    OSR[contact_index_reaction]
    OSslim[contacts_index]
    Jobs[GET /api/v1/jobs]
  end

  subgraph scraper [EC2/scraper.server]
    Resume["/resume/v1 score"]
  end

  List --> Detail
  Detail --> BQ
  Detail --> PD
  Detail --> MJ
  PD --> job
  MJ --> Jobs
  MJ -.optional.-> scraper
```

**User experience on `/candidates/[uuid]`:**

| Section | Content |
|---------|---------|
| Header | Name, LinkedIn, enrichment status, “Refresh matches” |
| Profile | Full Apify profile (headline, experience, skills, emails) |
| Activity | Posts / comments / reactions tabs |
| Matched jobs | Table like hiring-signals, filtered/scored for this candidate |

Use **`/candidates`** (correct spelling), not `/candiates`.

---

## What `uuid` means in the URL

Pick one canonical ID and stick to it:

| Option | URL param | Pros | Cons |
|--------|-----------|------|------|
| **A (recommended)** | `bench_candidates.id` (gateway) | Auth/ownership on gateway row; works before enrichment | Extra hop to resolve `contact_uuid` |
| **B** | `contact_uuid` (OpenSearch/Connectra) | Stable CRM identity | Harder to authorize before enrichment completes |

**Recommended:** `/candidates/[benchCandidateId]` with fields:

- `id` — bench row (URL)
- `contact_uuid` — set after profile enrichment (`job.server`)
- `linkedin_url`, `name`, `resume_id` (optional, scraper)

Detail page loads bench row first, then uses `contact_uuid` for OpenSearch bundles and job matching.

---

## What already exists (reuse)

### App patterns

- Dynamic route: `contacts/[uuid]/page.tsx` — header, info rows, loading/error
- Job table: `HiringSignalDrawerJobsGrid`, `HiringSignalsDataTable`, `useHiringSignals`
- Resume detail: `resume/[id]/page.tsx` — tabs, score via scraper proxy

### Gateway (`contact360.io/api`)

| Piece | Status |
|-------|--------|
| `hireSignal.jobs` | Live — `JobServerClient.list_jobs` → `GET /api/v1/jobs` |
| `suggest_hire_filters_from_resume_payload` | Live — maps profile → `titles`, `locations`, `extendedJobFilters` |
| `JobServerClient` | `list_jobs`, `get_job`, company/contacts for **jobs**, not bench contacts |
| `resume` GraphQL + `/resume/v1` proxy | Live — scraper.server resume get/score |
| `bench_candidates` table / GraphQL | **Not built yet** (prior conversation) |
| `GET contact by uuid` on job.server | **Not built** (only job→company→contacts) |

### `job.server`

| Piece | Status |
|-------|--------|
| `contacts_index` bulk upsert | Live (`OSBulkUpsertContacts`) |
| `OSGetContactByUUID` | Live (client helper, no HTTP route yet) |
| Profile Apify → dual write | **Planned**, not on `LpVuK3Zozwuipa5bp` path yet |
| `contacts_index_v1`, social indices | **Planned** |
| `GET /api/v1/jobs` + extended filters | Live |

### `scraper.server`

| Piece | Status |
|-------|--------|
| `GET /resume/v1/resumes/{id}/score?job_id=` | Live — keyword match % |
| Resume structured JSON | Live — for resume-based matching |

---

## API design (gateway — `candidates` or `hireSignal` module)

Do **not** use the scheduler **`jobs`** module. Add a **`candidates`** (or `bench`) GraphQL namespace.

### Queries

```graphql
type BenchCandidateDetail {
  id: ID!
  name: String!
  linkedinUrl: String!
  contactUuid: String
  enrichmentStatus: JSON!      # profile/posts/comments/reactions
  profile: JSON                # contacts_index_v1 or slim + v1 merge
  posts: JSON                  # list from contact_index_post
  comments: JSON
  reactions: JSON
  suggestedJobFilters: JSON!   # derived filters (for transparency)
}

type BenchCandidateMatchedJobsResult {
  items: JSON!                 # same shape as hireSignal.jobs data[]
  total: Int!
  filtersApplied: JSON!
  scores: JSON                 # optional job_id → match_percentage
}

extend type Query {
  candidates: CandidateQuery!
}

type CandidateQuery {
  benchCandidate(id: ID!): BenchCandidateDetail
  benchCandidateMatchedJobs(
    id: ID!
    limit: Int = 25
    offset: Int = 0
    rankWithResumeScore: Boolean = false
  ): BenchCandidateMatchedJobsResult
}
```

### Resolver flow

**`benchCandidate(id)`**

1. `require_auth` → load `bench_candidates` row (owner = `user.uuid`)
2. If no `contact_uuid` → return slim row + `enrichmentStatus` only
3. Else proxy **`job.server`** (new routes below) for profile bundle
4. Optionally merge Connectra contact via existing `contacts.contact(uuid)` if linked

**`benchCandidateMatchedJobs(id)`**

1. Load bench row + `contact_uuid`
2. Fetch profile from `job.server` (`contacts_index_v1.raw_payload`)
3. **`suggest_hire_filters_from_apify_profile(profile)`** — extend `resume_suggest.py` for Apify field names (`firstName`, `currentPosition`, `topSkills`, `location.parsed`, etc.)
4. Call existing `JobServerClient.list_jobs(...)` with merged filters + user hire-signal prefs (hidden companies, hide applied)
5. **(v2)** For top N jobs: scraper `resume/v1` score if `resume_id` present; or store job descriptions in scraper and score against profile text

---

## New `job.server` HTTP routes (aggregation layer)

The app should not hit OpenSearch directly. Add read APIs:

| Route | Purpose |
|-------|---------|
| `GET /api/v1/bench/contacts/:uuid` | Slim doc from `contacts_index` |
| `GET /api/v1/bench/contacts/:uuid/profile` | Full `contacts_index_v1` |
| `GET /api/v1/bench/contacts/:uuid/posts` | Paginated `contact_index_post` |
| `GET /api/v1/bench/contacts/:uuid/comments` | Paginated `contact_index_comment` |
| `GET /api/v1/bench/contacts/:uuid/reactions` | Paginated `contact_index_reaction` |
| `GET /api/v1/bench/contacts/:uuid/enrichment-status` | Mongo/OS status doc |

Or one bundle:

`GET /api/v1/bench/contacts/:uuid/detail?include=profile,posts,comments,reactions`

Gateway `JobServerClient` mirrors these; update `ROUTE-CLIENT-MATRIX.md`.

---

## Job matching logic (candidate → jobs)

### Tier 1 — Filter mapping (MVP, no scraper)

Extend profile → filters (same idea as `suggestHireSignalFiltersFromResumeUpload`):

| Profile source (Apify / v1) | `hireSignal` / job.server param |
|----------------------------|----------------------------------|
| `headline`, `currentPosition[].position` | `titles[]` |
| `location.parsed.city/country` | `locations[]` |
| `currentPosition[].skills`, `topSkills` | `extendedJobFilters.skillsAll` |
| Education degrees | `educationLevelMins` |
| Infer from title | `seniority`, `experience_bucket` (heuristics) |

Then:

```python
async with JobServerClient() as client:
    jobs = await client.list_jobs(
        limit=limit,
        offset=offset,
        titles=suggested["primaryTitleTokens"],
        locations=suggested["locationTokens"],
        extended_job_filters=suggested["extendedJobFiltersSuggestion"],
        # + hire_signal_prefs hidden companies, etc.
    )
```

Return `filtersApplied` in GraphQL so the UI can show “Matching: Data Engineer · Hyderabad · Spark…”.

### Tier 2 — Scraper scoring (v2)

For each job in the filtered set (top 50–100):

1. Ensure job description stored (job.server Mongo `linkedin_jobs` or scraper `resume/v1/jobs/upload`)
2. Call gateway → scraper `GET /resume/v1/resumes/{resume_id}/score?job_id=`
3. Sort by `match_percentage`; show score column in jobs grid

If no `resume_id`, skip scoring or use keyword overlap only.

### Tier 3 — AI explain (later)

`ai.server` short explanation per top match — out of scope for first slice.

---

## App: `/candidates/[uuid]` UI structure

### Files (mirror existing patterns)

| File | Role |
|------|------|
| `app/(dashboard)/candidates/[uuid]/page.tsx` | Thin wrapper + Suspense |
| `components/feature/candidates/CandidateDetailPageClient.tsx` | Main page |
| `components/feature/candidates/CandidateProfilePanel.tsx` | Profile header + fields |
| `components/feature/candidates/CandidateActivityTabs.tsx` | Posts / comments / reactions |
| `components/feature/candidates/CandidateMatchedJobsPanel.tsx` | Jobs table |
| `services/graphql/candidatesService.ts` | GraphQL operations |
| `hooks/useBenchCandidateDetail.ts` | Data + refresh |
| `hooks/useBenchCandidateJobs.ts` | Matched jobs pagination |

### Layout (tabs)

```
[← Back to bench]  Name · LinkedIn · Status badges

Tabs: Overview | Posts | Comments | Reactions | Matched jobs

Overview: photo, headline, about, experience timeline, skills, emails
Matched jobs: reuse HiringSignalsDataTable columns (title, company, location, posted, match %)
```

### States

| State | UX |
|-------|-----|
| Enrichment pending | Skeleton + “Fetching LinkedIn data…” |
| Profile failed | Alert + Retry enrichment |
| No `contact_uuid` yet | Show name/URL only; disable jobs tab |
| Jobs loading | Table skeleton |
| Zero jobs | “No matches — widen filters” + show `filtersApplied` |

### Routing

```ts
// routes.ts
CANDIDATES: "/candidates",
candidateDetailRoute: (id: string) => `/candidates/${encodeURIComponent(id)}`,
```

List page links: `href={candidateDetailRoute(row.id)}`.

---

## Task breakdown (ordered)

### Phase A — Prerequisites (from prior work)

1. Gateway `bench_candidates` table + `createBenchCandidate` / `benchCandidates` list  
2. `job.server` profile enrichment → `contacts_index` + `contacts_index_v1`  
3. Social enrichment → `contact_index_post`, `_comment`, `_reaction`  
4. `POST /api/v1/bench-candidates/enrich` after save  
5. Store `contact_uuid` on bench row when profile step completes  

### Phase B — `job.server` read API

6. OpenSearch repos: get by `contact_uuid` per index  
7. `GET /api/v1/bench/contacts/:uuid/detail` (or split routes)  
8. Pagination for posts/comments/reactions (`contact_uuid` term query)  
9. `enrichment-status` endpoint  
10. Postman + `ROUTE-CLIENT-MATRIX.md`  
11. `JobServerClient` methods in gateway  

### Phase C — Gateway GraphQL

12. `CandidateQuery.benchCandidate(id)` — auth + proxy job.server  
13. `suggest_hire_filters_from_apify_profile()` in `hire_signal/` or `candidates/`  
14. `benchCandidateMatchedJobs(id, limit, offset)` — filters → `list_jobs`  
15. Merge `hire_signal_prefs` (hidden companies, hide applied)  
16. Register in `schema.py`  
17. API tests (owner-only, missing contact_uuid, filter mapping snapshot)  
18. Update `GRAPHQL-SCHEMA.md` / `DECISIONS.md` if needed  

### Phase D — App list + detail routes

19. `ROUTES.CANDIDATES` + `candidateDetailRoute`  
20. `candidates/page.tsx` (list — if not done)  
21. `candidates/[uuid]/page.tsx`  
22. `candidatesService.ts` — `fetchBenchCandidate`, `fetchBenchCandidateMatchedJobs`  
23. `useBenchCandidateDetail` hook  
24. `CandidateDetailPageClient` — layout shell  

### Phase E — Profile & activity UI

25. `CandidateProfilePanel` — map Apify/v1 JSON to display fields  
26. `CandidateActivityTabs` — posts/comments/reactions lists  
27. Enrichment status chips (profile / posts / comments / reactions)  
28. Empty/error/retry states  

### Phase F — Matched jobs UI

29. `useBenchCandidateJobs` — pagination, sort by posted date  
30. `CandidateMatchedJobsPanel` — reuse `HiringSignalsDataTable` or drawer grid  
31. Show `filtersApplied` summary above table  
32. Job row actions: open description modal (`JobDescriptionModal`), mark applied (existing hire-signal prefs)  
33. Optional: link to company drawer (`CompanyDrawerPanel`)  

### Phase G — Scraper integration (v2)

34. Link bench candidate ↔ `resume_id` when user uploads resume  
35. Gateway helper: batch score top N jobs via `/resume/v1` proxy  
36. `matchScore` column + sort in matched jobs panel  
37. Cache scores in gateway or `bench_candidate_job_matches` table  

### Phase H — Polish & ops

38. Nav: Bench under Database next to Hiring Signals  
39. Activity log on “view candidate” / “refresh matches”  
40. SLO: detail page p95 &lt; 2s (cached profile); jobs query p95 &lt; 800ms  
41. Doc: phase 11 pointer + `hiring-analytics` cross-link  

---

## Data source map per UI section

| UI section | Primary source | Fallback |
|------------|----------------|----------|
| Name, LinkedIn | Gateway `bench_candidates` | — |
| Profile overview | `job.server` → `contacts_index_v1` | `contacts_index` slim |
| Emails / headline | Apify `raw_payload` in v1 | Connectra `contacts.contact` |
| Posts | `job.server` → `contact_index_post` | — |
| Comments | `contact_index_comment` | — |
| Reactions | `contact_index_reaction` | — |
| Matched jobs | Gateway → `job.server` `list_jobs` | — |
| Match % (v2) | `scraper.server` `/resume/v1/.../score` | — |

---

## Important design notes

1. **Single gateway entry** — App only talks to GraphQL; gateway fans out to `job.server` and `scraper.server`.  
2. **Reuse hiring-signals UI** — Matched jobs should look like `/hiring-signals`, not a one-off table.  
3. **Filter transparency** — Show which candidate fields drove the job query (trust + debugging).  
4. **Auth boundary** — Bench row is user-scoped; `contact_uuid` reads go through gateway with ownership check.  
5. **Typo in your message** — Comments/reactions should **not** share `contact_index_post`; use separate indices as planned earlier.

---

## Suggested MVP slice for this page

Ship in this order:

| Step | Delivers |
|------|----------|
| **MVP-1** | `/candidates/[id]` with gateway bench row + enrichment status only |
| **MVP-2** | Profile panel from `job.server` v1 (after enrichment exists) |
| **MVP-3** | Matched jobs tab (filter-only, no scraper score) |
| **MVP-4** | Activity tabs (posts/comments/reactions) |
| **MVP-5** | Resume/scraper scoring column |

---

## Summary

`/candidates/[uuid]` is a **composition page**: gateway owns the bench record and authorization; **`job.server`** owns enriched LinkedIn data and job listings; **`scraper.server`** optionally ranks jobs against a resume.

Most hiring-signals plumbing already exists (`hireSignal.jobs`, filter merge, job table components). The net-new work is **bench CRUD**, **job.server read APIs for v1 + social indices**, **Apify-aware filter mapping**, and a **detail route** that wires them together.

I'm in **Ask mode** and can't implement this. Switch to **Agent mode** if you want MVP-1–3 built; say whether the URL id should be **bench candidate id** or **contact uuid**.

---

**User**

so now think about user can add their bench candiates , then you fetch all details about those candiates and user can show all job according to candiates fetch details for every bench candiates , Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

# Bench candidates → enrichment → matched jobs (end-to-end)

This is the **full product loop** across three layers: **app** (`contact360.io/app`), **gateway** (`contact360.io/api`), and **satellites** (`job.server` + optional `scraper.server`). Nothing in this loop is fully wired yet; the pieces below map to what exists vs what you still need to build.

---

## The user journey (one sentence)

A staffing user **adds people to their bench**, the system **pulls LinkedIn profile + social activity via Apify**, then **shows open jobs from `job.server` that fit each person’s skills, title, and location** — per candidate, not one global job search.

---

## End-to-end architecture

```mermaid
flowchart TB
  subgraph phase1 [1. Add bench]
    UI1["/candidates — form: name + LinkedIn URL"]
    GW1["Gateway: bench_candidates Postgres"]
  end

  subgraph phase2 [2. Fetch details]
    ENQ["Gateway → job.server enrich"]
    P[Apify Profile LpVuK3Zozwuipa5bp]
    Po[Apify Posts A3cAPGpwBEG8RJwse]
    C[Apify Comments FiHYLewnJwS6GnRpo]
    R[Apify Reactions VMwB47uSx3g2wCcBK]
    OS1[contacts_index slim]
    OSv1[contacts_index_v1 full]
    OSp[contact_index_post]
    OSC[contact_index_comment]
    OSR[contact_index_reaction]
  end

  subgraph phase3 [3. Jobs per candidate]
    MAP[Profile → hireSignal filters]
    JOBS[job.server GET /api/v1/jobs]
    UI2["/candidates/uuid — profile + jobs tabs"]
  end

  UI1 --> GW1 --> ENQ
  ENQ --> P --> OS1
  P --> OSv1
  ENQ --> Po --> OSp
  ENQ --> C --> OSC
  ENQ --> R --> OSR
  OSv1 --> MAP --> JOBS --> UI2
  GW1 --> UI2
```

**Canonical identity:** one **`contact_uuid`** (UUID5 from LinkedIn slug, Connectra-compatible) shared across all OpenSearch indices. The bench row in Postgres holds `id`, `name`, `linkedin_url`, `contact_uuid`, and enrichment status.

---

## Layer responsibilities

| Layer | Owns | Does not own |
|-------|------|----------------|
| **App** | `/candidates`, `/candidates/[id]`, forms, tables, tabs | Apify, OpenSearch, direct `job.server` calls |
| **Gateway** | `bench_candidates` CRUD, auth, GraphQL, job filter mapping, prefs merge | Apify polling, bulk OpenSearch writes |
| **job.server** | Apify runs, OpenSearch indices, `GET /jobs`, new `GET /bench/contacts/:uuid/*` | User/bench ownership (gateway) |
| **scraper.server** | (v2) resume parse + job keyword score | Bench list, LinkedIn scrape |

Use GraphQL namespace **`candidates`** (or nested under `hireSignal`) — **not** the scheduler **`jobs`** module.

---

## Phase 1 — Add bench candidates

### User action
On **`/candidates`**, user enters **name** + **LinkedIn profile URL** (and can add many rows).

### Gateway (Postgres)
Table `bench_candidates` (user-scoped):

| Column | Purpose |
|--------|---------|
| `id` | Primary key (use in URLs) |
| `user_id` | FK → `users.uuid` |
| `name` | Display name |
| `linkedin_url` | Normalized URL |
| `linkedin_slug` | Dedup per user |
| `contact_uuid` | Set after profile enrichment |
| `profile_status` | pending / running / done / failed |
| `posts_status`, `comments_status`, `reactions_status` | Same |
| `created_at`, `updated_at` | Audit |

### GraphQL (gateway)
- `createBenchCandidate(name, linkedinUrl)`
- `benchCandidates(limit, offset)`
- `deleteBenchCandidate(id)`

### App tasks
1. Add `ROUTES.CANDIDATES = "/candidates"` and nav entry under Database.
2. `candidates/page.tsx` + `CandidatesPageClient`.
3. Add form + table (name, LinkedIn link, status chips).
4. `candidatesService.ts` — create/list/delete mutations.
5. Validate LinkedIn `/in/` URLs client-side; server is source of truth.

---

## Phase 2 — Fetch all candidate details (job.server + Apify)

Triggered after save (single candidate or “Enrich all” batch).

### Orchestration
```
Gateway createBenchCandidate
  → POST job.server /api/v1/bench-candidates/enrich
  → Asynq: apify:bench_enrich_one per candidate
```

**Order:** Profile **first** (establishes `contact_uuid`), then **posts / comments / reactions in parallel**.

### Apify actors (from your docs)

| Step | Actor ID | Input | OpenSearch index |
|------|----------|-------|------------------|
| Profile + email | `LpVuK3Zozwuipa5bp` | `queries[]`, `profileScraperMode` | Slim → `contacts_index`; full → `contacts_index_v1` |
| Posts | `A3cAPGpwBEG8RJwse` | `targetUrls[]`, `maxPosts`, … | `contact_index_post` |
| Comments | `FiHYLewnJwS6GnRpo` | `profiles[]`, `maxItems` | `contact_index_comment` |
| Reactions | `VMwB47uSx3g2wCcBK` | `profiles[]`, `maxItems` | `contact_index_reaction` |

**Note:** Comments and reactions need **separate indices** (not `contact_index_post` for all three).

### Profile dual-write (critical)
1. Map Apify item → slim doc (`first_name`, `last_name`, `linkedin_url`, `title`, `email`, `city`, `country`, …).
2. `OSBulkUpsertContacts` → `contacts_index` → returns **`contact_uuid`**.
3. Write full JSON to `contacts_index_v1` with `_id = contact_uuid`.
4. Callback or poll: gateway updates `bench_candidates.contact_uuid` + `profile_status=done`.

### What exists vs gap in job.server today
| Exists | Gap |
|--------|-----|
| `RunProfileScrape`, `POST /runs/profile` | Wrong actor/input; writes only `linkedin_profiles_index`, not `contacts_index_v1` |
| `OSBulkUpsertContacts`, UUID5 | No bench orchestrator, no social actors, no new indices |
| `ConnectraBridge` | Pattern to reuse for slim upsert |

### job.server tasks
6. Env vars for four actor IDs.
7. Create indices + mappings: `contacts_index_v1`, `contact_index_post`, `_comment`, `_reaction`.
8. `RunBenchProfileScrape` → dual write + return `contact_uuid`.
9. `RunBenchPostsScrape`, `RunBenchCommentsScrape`, `RunBenchReactionsScrape`.
10. Shared `pollApifyRunAndIngest` helper.
11. Asynq tasks + `POST /api/v1/bench-candidates/enrich` (batch).
12. `GET /api/v1/bench-candidates/:id/enrichment-status`.
13. Read APIs: `GET /api/v1/bench/contacts/:uuid/detail` (profile + paginated social).
14. Mongo/OS enrichment status per bench candidate id (if job.server tracks gateway ids).

### Gateway tasks
15. `JobServerClient.enrich_bench_candidates([...])`.
16. `JobServerClient.get_bench_contact_detail(contact_uuid)`.
17. On create: auto-enqueue enrich (or explicit “Enrich” button).
18. Poll/webhook: update `bench_candidates` statuses + `contact_uuid`.

---

## Phase 3 — Show jobs per candidate (from fetched details)

### Matching logic (MVP: filter-based)

For each bench candidate with `contact_uuid` and profile in `contacts_index_v1`:

1. Load `raw_payload` (Apify profile JSON).
2. **Map to job filters** (extend `resume_suggest.py` for Apify shape):

| Profile field | Job filter |
|---------------|------------|
| `headline`, `currentPosition[].position` | `titles[]` |
| `location.parsed.city/country` | `locations[]` |
| Skills from positions / `topSkills` | `extendedJobFilters.skillsAll` |
| Education | `educationLevelMins` |
| Title heuristics | `seniority`, `experience_bucket` |

3. Call existing `JobServerClient.list_jobs(...)` with those filters.
4. Apply user prefs: hidden companies, hide applied (`hire_signal_prefs`).
5. Return jobs + `filtersApplied` for UI transparency.

### Detail page — `/candidates/[id]`

Use **bench row `id`** in the URL (not `contact_uuid`) for auth; resolve `contact_uuid` inside.

| Tab | Data source |
|-----|-------------|
| **Overview** | `contacts_index_v1` — headline, about, experience, skills, emails |
| **Posts** | `contact_index_post` |
| **Comments** | `contact_index_comment` |
| **Reactions** | `contact_index_reaction` |
| **Matched jobs** | Gateway → `list_jobs` with derived filters; reuse `HiringSignalsDataTable` |

### GraphQL (gateway)
- `benchCandidate(id)` — bench row + profile bundle from job.server
- `benchCandidateMatchedJobs(id, limit, offset)` — filtered job list

### App tasks
19. `candidates/[id]/page.tsx` + `CandidateDetailPageClient`.
20. `candidateDetailRoute(id)` in `routes.ts`.
21. `useBenchCandidateDetail` + `useBenchCandidateJobs`.
22. Profile panel + activity tabs + matched jobs table.
23. Loading states: enriching vs ready vs failed.
24. List page links → detail; status badges on list.

### v2 — Scraper scoring (optional)
25. Link `resume_id` on bench row if user uploads resume.
26. Top N jobs → `scraper.server` `GET /resume/v1/resumes/{id}/score?job_id=`.
27. Sort by `match_percentage`; show score column.

---

## Master task list (42 steps, dependency order)

### Track A — Foundation (gateway + list UI)
| # | Task |
|---|------|
| A1 | Alembic `bench_candidates` + model + repository |
| A2 | GraphQL create/list/delete + auth |
| A3 | App `/candidates` list + form |
| A4 | Nav + `candidatesService.ts` |

### Track B — Enrichment (job.server)
| # | Task |
|---|------|
| B1 | OpenSearch new indices + ensure mappings |
| B2 | Profile actor + dual write + `contact_uuid` |
| B3 | Posts / comments / reactions actors + bulk index |
| B4 | Asynq orchestrator (profile → parallel social) |
| B5 | HTTP enrich + status + read detail APIs |
| B6 | Gateway `JobServerClient` + enrich on create |

### Track C — Job matching (gateway)
| # | Task |
|---|------|
| C1 | `suggest_hire_filters_from_apify_profile()` |
| C2 | `benchCandidateMatchedJobs` resolver |
| C3 | Merge hire-signal user prefs |
| C4 | Tests for filter mapping + list_jobs integration |

### Track D — Detail UI
| # | Task |
|---|------|
| D1 | `/candidates/[id]` route + hooks |
| D2 | Overview / activity tabs |
| D3 | Matched jobs tab (reuse hiring-signals components) |
| D4 | “Enrich” / “Refresh matches” actions |

### Track E — Hardening
| # | Task |
|---|------|
| E1 | Apify rate limits + idempotency (skip fresh v1) |
| E2 | `DECISIONS.md` + route matrix docs |
| E3 | Credits/billing hooks (phase 1) |
| E4 | (v2) scraper resume scoring |

**Parallelism:** A1–A4 can start immediately. B1–B6 can run in parallel with A after A1 schema is fixed. C depends on B2 (profile in v1). D depends on A + B read APIs + C.

---

## MVP slices (what to ship first)

| Slice | User-visible outcome |
|-------|----------------------|
| **MVP-1** | Add bench candidates (name + URL); list only; no enrichment |
| **MVP-2** | Profile enrichment → overview on detail page |
| **MVP-3** | Matched jobs tab (filter-only, no Apify social) |
| **MVP-4** | Posts / comments / reactions tabs |
| **MVP-5** | Batch “Enrich all” + status on list |
| **MVP-6** | Resume/scraper match scores |

---

## What you already have (reuse, don’t rebuild)

- **Job corpus:** `job.server` `GET /api/v1/jobs` + gateway `hireSignal.jobs`
- **Filter merge:** `job_server_job_filters.merge_extended_job_filters`
- **Resume → filters:** `resume_suggest.py` (adapt for Apify profile)
- **OpenSearch contacts:** `OSBulkUpsertContacts`, UUID5, `contacts_index`
- **Apify infra:** `ApifyOrchestrator`, Asynq, `POST /runs/profile` (replace internals)
- **UI:** `HiringSignalsDataTable`, `contacts/[uuid]` detail pattern, `JobDescriptionModal`
- **Scraper:** `/resume/v1` proxy + score API (v2 ranking)

---

## Key decisions to lock before coding

1. **URL id:** bench `id` in `/candidates/[id]` (recommended).
2. **Enrich trigger:** automatic on create vs manual “Enrich” button (manual is cheaper for Apify).
3. **Profile actor mode:** with email ($10/1k) vs without ($4/1k) — env-driven.
4. **Job matching v1:** filters only; scoring in v2.
5. **Ownership:** bench is **per user** today (`user_id`); org-level bench later if you add `org_id`.

---

## Summary

The full flow is three connected pipelines:

1. **

