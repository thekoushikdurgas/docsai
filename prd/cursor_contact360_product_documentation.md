# Contact360 product documentation analysis
_Exported on 6/7/2026 at 12:53:49 GMT+5:30 from Cursor (3.7.12)_

---

**User**

@docs/prd/Contact360_Product_Documentation_v3.md  read this file and then thick about explain the file properly , Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

I'll read the PRD and break it down into a structured analysis.


# Contact 360 PRD — Deep Analysis

This document is the **internal product requirements and roadmap** for Contact 360 (v2.1, implementation-aligned, June 2026). It defines what the platform is, who it serves, how features roll out across versions, and how engineering should treat the shipping codebase as the source of truth where the PRD and code differ.

Below is a structured breakdown: learn the product → understand the architecture → analyze the roadmap → decompose work into actionable steps.

---

## Step 1: Understand the Product at a Glance

### What Contact 360 Is

Contact 360 is a **B2B SaaS staffing intelligence platform**. It:

1. **Aggregates** live US job postings from major boards (LinkedIn, Indeed, Glassdoor, etc.)
2. **Normalizes** them into one schema
3. **Surfaces hiring signals** in a filterable dashboard
4. **Provides contact intelligence** — decision-makers at hiring companies (with masked emails until reveal)
5. **Sends email alerts** when new jobs match saved filter sets

### The Core Problem

Staffing agencies today:

- Jump between multiple job boards manually
- Export and cross-reference data
- Spend hours finding *who* to contact at hiring companies

Contact 360 collapses that into **one intelligent workflow**: discover hiring companies → filter signals → reach decision-makers.

### Target Users (v1.x)

| Segment | Goal |
|---------|------|
| IT Staff Augmentation | Find companies hiring IT talent to pitch consultants |
| IT Bench Sales | Match open roles to benched consultants |
| General Staffing | Cross-industry hiring signals for BD |

**v2 (future):** Colleges & training providers — hiring trends for curriculum and placement.

**Geography:** US is primary; multi-country ISO filters exist in UI, but ingest/GTM focus is US.

---

## Step 2: Map the Filter System (Release-Versioned)

Filters are the product’s main differentiator. They are **explicitly version-gated** — not all filters ship at once.

### Company Filters

| Filter | Version | Dependency |
|--------|---------|------------|
| Company Name | v1 | Core text search |
| Country | v1 | ISO include/exclude |
| Industry | v1 | Multi-select |
| Employee Size | v1 | Range |
| Funding | v1.1 | Enrichment data |
| Revenue | v1.2 | Enrichment data |

### Job Filters

| Filter | Version | Notes |
|--------|---------|-------|
| Title, Location, Date Posted, Experience, Job Type, LinkedIn Apply | v1 | Core set |
| Department | v1 | Renamed from “Function”; uses `function_category` in code |
| Job Function | v1 | Sub-filter under Department |
| Education, Required Skills, Compliance, Compensation | v1.1 | NLP/parsing required |
| — | — | **Removed:** View, Remote/Workplace (out of v1.x scope) |

**Design implication:** Filter UI, API, and indexing must be built incrementally. v1.1 filters need NLP parsing and enrichment pipelines.

---

## Step 3: Understand Versioning Philosophy

The roadmap is **not open-ended**. Each version has a **locked core scope**:

| Principle | Meaning |
|-----------|---------|
| Fixed core scope | v1 / v1.1 / v1.2 scopes are defined before dev starts; no mid-version scope creep |
| Market-driven additions | v1.2+ gets **2 extra features** from customer feedback per version |
| Stability gate | v1 must be stable before v1.1 ships; v1.1 before v1.2 |
| Feedback loop | Collect requests continuously; pick top 2 per version |

This is a **predictable, staged delivery model** — good for engineering planning and sales commitments.

---

## Step 4: Implementation Alignment (Code vs PRD)

Section **3.0.1** says the **shipping codebase** (`contact360.io` + `EC2/`) overrides older PRD drafts:

| Area | Authoritative behavior |
|------|------------------------|
| RBAC | `FreeUser`, `ProUser`, `Admin`, `SuperAdmin`, `Owner` — billing tier vs operator roles are separate |
| Saved searches | Side panel (`SavedSearchesMenu`), not a main tab |
| Country filter | Multi-country ISO via `COUNTRY_FILTER_OPTIONS`, `hiringSignalFilterDraft.countries` |
| Department (v1) | Job Function only (`function_category`) in `HiringSignalsFilterSidebar` |
| Work email | Masked until reveal in drawer/modal components |

**Takeaway:** When building or QA’ing, treat this table as the contract; the PRD narrative may lag the code in a few places.

---

## Step 5: Version 1 — Foundation (Detailed Breakdown)

v1 = **first working product** for internal stakeholders.

### 5.1 Platform Setup
- Auth (email/password)
- Team/org onboarding
- RBAC (5 roles)
- Basic billing scaffolding

### 5.2 Job Aggregation
- **LinkedIn Jobs** (only platform in v1)
- Normalization → Contact 360 schema
- Deduplication (same job, multiple sources → one row)
- Fetch cadence: **every 15–30 minutes**

### 5.3 Dashboard
- Columns: Title, Company, Location, Type, Posted, Actions
- Tabs: **All Signals | Today’s Jobs**
- Saved searches: side panel (save filters + email config)
- 50 jobs/page, refresh + last-updated, export XLSX (max 500 rows)

### 5.4 v1 Filters (12 total conceptually; 8 job + 4 company in success criteria)
Company: Name, Country, Industry, Employee Size  
Job: Title, Location, Date Posted, Experience, Job Type, LinkedIn Apply, Department/Function

### 5.5 Email Notifications (v1 core)
- Trigger: new job matches active filters
- Frequency: real-time or custom (2h, 6h, 12h)
- Per saved filter set on/off
- Email content: title, company, location, date, dashboard link

### 5.6 Contact Intelligence (v1 core)
| Field | v1 behavior |
|-------|-------------|
| First Name, Job Title, Department, LinkedIn | Always visible |
| Work Email | Masked until reveal |
| Phone | v1.3 (TBD); credits TBD |

### 5.7 v1 Success Metrics

| Metric | Target |
|--------|--------|
| Platforms | LinkedIn |
| Company filters | 4 |
| Job filters | 8 |
| Dashboard load | < 3s |
| Job freshness | < 30 min |
| Contact fields | 5 (email reveal-on-demand) |

---

## Step 6: Version 1.1 — Expansion & Beta

**Goal:** Advanced filters + stability; **closed beta** with 3–5 staffing clients.

### Additions
- **Indeed** + 1 TBD platform
- **5 new filters:** Education, Skills, Compliance, Compensation, Funding
- Better dedup across sources
- Performance: load < 2.5s, freshness < 20 min
- Integration monitoring + internal status page

### Success criteria
- 2+ platforms
- All filters except Revenue (12 job + company)
- 0 P0 bugs

---

## Step 7: Version 1.2 — GA Readiness

**Goal:** Complete filter set + enterprise hardening.

### Additions
- **Revenue** filter (enrichment)
- **2 market-driven features** (TBD from v1/v1.1 feedback)

### GA checklist (high bar)

| Category | Target |
|----------|--------|
| Uptime | 99.9% SLA |
| Load | 500 concurrent users |
| Security | SOC 2 Type I readiness, GDPR, full audit log |
| Accessibility | WCAG 2.1 AA |
| Performance | Dashboard < 2s, filters < 500ms, freshness < 15 min |
| Integrations | 6+ job platforms |
| Contact intelligence | Credits system live |
| QA | > 80% core flow coverage |

---

## Step 8: Data Schema — The Normalization Contract

Section 4 defines the **unified job signal model**. Everything from ingest → API → UI flows through these fields:

```
signal_id, title, company_name, company_id
location_state, location_city
job_type, experience_level, department, job_function
date_posted, date_fetched, source_platform, link, description_text
required_skills[], salary_min/max, education_required, visa_sponsorship  (v1.1)
linkedin_easy_apply
industry, company_size, revenue, funding_stage  (enrichment)
is_saved  (per-user)
```

**Architecture insight:**  
- **Platform fields** come from scrapers/APIs  
- **Parsed fields** (v1.1) need NLP on `description_text`  
- **Enrichment fields** need a separate company data pipeline  
- **User fields** (`is_saved`) are per-tenant/user state  

---

## Step 9: Logical Work Decomposition (How Teams Should Break This Down)

If you were planning or implementing from this PRD, a sensible task breakdown:

### Phase A — v1 Core (MVP)
1. Auth + org + RBAC
2. LinkedIn ingest + normalize + dedupe + 15–30 min scheduler
3. Job signals API + pagination (50/page)
4. Dashboard UI + All/Today tabs + refresh + export
5. v1 filters (company + job) wired to search index
6. Saved searches side panel + apply/restore
7. Email notification engine (real-time + scheduled)
8. Contact intelligence module + email mask/reveal
9. Basic billing scaffolding

### Phase B — v1.1
1. Indeed + second platform adapter
2. Cross-source dedup improvements
3. NLP pipeline: skills, education, compliance, salary parsing
4. Company enrichment: funding stage
5. New filter UI + API
6. Monitoring, alerting, internal status page
7. Closed beta onboarding (3–5 clients)

### Phase C — v1.2 (GA)
1. Revenue enrichment + filter
2. 2 customer-driven features (scoped after feedback)
3. Load testing, SLA, audit log
4. SOC 2 / GDPR / WCAG work
5. Contact credits system
6. 6+ platform integrations
7. QA to 80%+ on core flows

### Cross-cutting (all versions)
- Filter versioning in API (feature flags or schema version)
- Performance budgets per version
- Stability gate before next version ships

---

## Step 10: Key Tensions & Gaps to Watch

1. **Filter count inconsistency:** Section 2 lists Department + Job Function separately; v1 success criteria says “8 job filters” including both; implementation uses `function_category` only for Department in v1 — align PRD, QA, and UI copy.

2. **Platform list vs v1 scope:** Section 1.5 lists 7+ boards; v1 success = LinkedIn only. Later versions scale integrations deliberately.

3. **Removed filters:** Remote/Workplace explicitly cut — don’t reintroduce without a version bump.

4. **Credits:** Mentioned for v1.2 contact intelligence and v1.3 phone — not fully specified in v1.

5. **Market-driven slots:** v1.2 has 2 TBD requirements — product must close these before v1.2 dev starts.

6. **Document version naming:** Header says “Version 1.x Series”; body says “v2.1 (Implementation-aligned)” — doc revision, not product version.

---

## Mental Model (One Diagram)

```mermaid
flowchart TB
    subgraph ingest [Data Ingestion]
        LI[LinkedIn v1]
        IN[Indeed v1.1]
        MORE[6+ platforms v1.2]
    end

    subgraph pipeline [Processing]
        NORM[Normalize to Schema]
        DEDUP[Deduplication]
        NLP[NLP Parse v1.1]
        ENRICH[Company Enrichment v1.1/v1.2]
    end

    subgraph product [Product Surface]
        DASH[Hiring Signals Dashboard]
        FILT[Versioned Filters]
        SAVE[Saved Searches + Email Alerts]
        CONTACT[Contact Intelligence]
    end

    subgraph users [Users]
        STAFF[Staffing Agencies]
        BETA[Closed Beta v1.1]
        GA[General Availability v1.2]
    end

    LI --> NORM
    IN --> NORM
    MORE --> NORM
    NORM --> DEDUP
    DEDUP --> NLP
    NLP --> ENRICH
    ENRICH --> DASH
    DASH --> FILT
    FILT --> SAVE
    DASH --> CONTACT
    STAFF --> DASH
    BETA --> DASH
    GA --> DASH
```

---

## Summary

| Dimension | Contact 360 in one sentence |
|-----------|---------------------------|
| **Product** | Unified US hiring-signal dashboard + contact intelligence for staffing BD |
| **Moat** | Aggregation + normalization + rich filters + decision-maker contacts |
| **Delivery** | Strict v1 → v1.1 → v1.2 with stability gates and 2 feedback-driven features per later version |
| **v1 must-haves** | LinkedIn, 12 filters (subset), dashboard, saved searches, email alerts, contact reveal |
| **v1.2 must-haves** | Full filters, 6+ platforms, enterprise compliance, credits, GA quality bar |

If you want to go deeper next, we can map any section (filters, notifications, RBAC, or contact reveal) to specific files under `contact360.io`, or turn the v1 checklist into an engineering sprint plan — still in Ask mode, so guidance only unless you switch to Agent mode for implementation.

---

**User**

now break the tasks in versions , Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

I'll cross-check the PRD against the codebase so the version-by-version task breakdown reflects what's already built versus what's still planned.


# Contact 360 — Version-by-Version Task Breakdown

This breaks the PRD into **v1 → v1.1 → v1.2** with epics, sub-tasks, dependencies, and acceptance checks. It also notes where the current codebase is ahead of or behind the PRD (useful for planning).

---

## Version Dependency Chain

```mermaid
flowchart LR
    V1[v1 Foundation] -->|stability gate| V11[v1.1 Beta]
    V11 -->|stability gate| V12[v1.2 GA]
    
    V1 --> A[Auth + RBAC]
    V1 --> B[LinkedIn ingest]
    V1 --> C[Dashboard + v1 filters]
    V1 --> D[Email notifications]
    V1 --> E[Contact intelligence]
    
    V11 --> F[Indeed + 2nd platform]
    V11 --> G[5 advanced filters]
    V11 --> H[Perf + monitoring]
    
    V12 --> I[Revenue filter]
    V12 --> J[Enterprise hardening]
    V12 --> K[2 market-driven features]
```

**Rule from PRD:** The next version does not ship until the previous one is **stable** (0 P0 bugs, performance targets met).

---

# VERSION 1 — Foundation (Internal Launch)

**Objective:** First working product — login, LinkedIn signals, core filters, email alerts, contact reveal.

**Success bar:** LinkedIn only · 4 company + 8 job filters · notifications live · dashboard &lt; 3s · freshness &lt; 30 min · 5 contact fields.

---

## Epic 1: Platform Setup & Access

### 1.1 Authentication
| Step | Task | Done when |
|------|------|-----------|
| 1.1.1 | Email/password signup | User can register with validated email |
| 1.1.2 | Login + session/JWT | Authenticated sessions persist correctly |
| 1.1.3 | Password reset flow | User can recover account via email |
| 1.1.4 | Logout + session expiry | Sessions invalidate on logout/timeout |

### 1.2 Organization & Team Onboarding
| Step | Task | Done when |
|------|------|-----------|
| 1.2.1 | Create organization on first signup | New user gets a workspace |
| 1.2.2 | Owner + member invite model | Owner invites members; invites accept/expire |
| 1.2.3 | Team member list + role assignment | Owner sees members and can assign roles |
| 1.2.4 | Onboarding wizard (minimal) | New org completes basic setup |

### 1.3 RBAC (5 roles)
| Step | Task | Done when |
|------|------|-----------|
| 1.3.1 | Define roles: `FreeUser`, `ProUser`, `Admin`, `SuperAdmin`, `Owner` | Constants in `contact360.io/api/app/core/constants.py` |
| 1.3.2 | Separate billing tier vs operator roles | Free/Pro ≠ Admin/SuperAdmin permissions |
| 1.3.3 | Gateway middleware enforces role on GraphQL | Unauthorized mutations/queries blocked |
| 1.3.4 | Frontend `RoleContext` gates UI features | Export, runs tab, etc. respect role |

### 1.4 Billing Scaffolding (v1 minimal)
| Step | Task | Done when |
|------|------|-----------|
| 1.4.1 | Free vs Pro plan model in DB | User has plan field |
| 1.4.2 | Stripe/payment placeholder or stub | Subscription object exists; upgrade path defined |
| 1.4.3 | Feature limits by tier (basic) | FreeUser vs ProUser behavior differs where PRD says so |

---

## Epic 2: Job Aggregation (LinkedIn)

### 2.1 LinkedIn Integration
| Step | Task | Done when |
|------|------|-----------|
| 2.1.1 | Scraper/fetcher for LinkedIn Jobs | Jobs pulled on schedule |
| 2.1.2 | Store raw payload + normalized fields | OpenSearch/Mongo documents created |
| 2.1.3 | Run tracking (`apify_run_id` / run UUID) | Each ingest batch traceable |
| 2.1.4 | Scheduler: 15–30 min cadence | Jobs refreshed within SLA |

### 2.2 Normalization Engine
| Step | Task | Done when |
|------|------|-----------|
| 2.2.1 | Map platform fields → PRD schema (Section 4) | `title`, `company_name`, `location_*`, `job_type`, etc. |
| 2.2.2 | Parse `posted_at`, `employment_type`, `seniority_level` | Consistent enums/buckets |
| 2.2.3 | `function_category_v2` for Department filter | Maps to PRD `department` / job function |
| 2.2.4 | `linkedin_easy_apply` flag | `apply_method` = `ComplexOnsiteApply` |
| 2.2.5 | Company linkage (`company_id` / UUID) | Jobs join to company profile |

### 2.3 Deduplication
| Step | Task | Done when |
|------|------|-----------|
| 2.3.1 | Primary key: `linkedin_job_id` upsert | Same job updates, not duplicates |
| 2.3.2 | Cross-field dedup rules (v1: single source) | One row per LinkedIn job |
| 2.3.3 | `date_fetched` updated on re-ingest | Freshness visible |

### 2.4 API Layer
| Step | Task | Done when |
|------|------|-----------|
| 2.4.1 | `job.server` list endpoint with filters | `GET /api/v1/jobs` |
| 2.4.2 | Filter-options facets endpoint | `GET /api/v1/jobs/filter-options` |
| 2.4.3 | Gateway `hireSignal.jobs` GraphQL | App queries through API gateway |

---

## Epic 3: Dashboard (Hiring Signals UI)

### 3.1 Main List
| Step | Task | Done when |
|------|------|-----------|
| 3.1.1 | Data table: Title, Company, Location, Type, Posted, Actions | Columns match PRD |
| 3.1.2 | Pagination: 50 jobs/page | `pageSize` = 50 default |
| 3.1.3 | Total signal count | Toolbar shows `total` |
| 3.1.4 | Refresh + last-updated timestamp | Manual refresh works |
| 3.1.5 | Row actions (drawer, connect, etc.) | User can open job/company detail |

### 3.2 Tab Navigation
| Step | Task | Done when |
|------|------|-----------|
| 3.2.1 | **All Signals** tab | Full filtered list |
| 3.2.2 | **Today's Jobs** tab (`new_7d` preset) | Calendar-today window applied |
| 3.2.3 | Tab + sidebar date filters compose correctly | Documented in `hiring-signals-ui.md` |

### 3.3 Saved Searches (Side Panel — not main tab)
| Step | Task | Done when |
|------|------|-----------|
| 3.3.1 | `SavedSearchesMenu` in side panel | Save current filter set |
| 3.3.2 | Apply saved search restores filters + time preset | One-click restore |
| 3.3.3 | Delete/rename saved searches | CRUD complete |
| 3.3.4 | Persist `listFilters` + `signalTimePreset` | Payload versioned |

### 3.4 Export
| Step | Task | Done when |
|------|------|-----------|
| 3.4.1 | Export selected rows to XLSX | Modal + async job queue |
| 3.4.2 | Cap at 500 rows | Enforced server-side |
| 3.4.3 | Download via presigned URL | Jobs drawer shows progress |

---

## Epic 4: Filters — v1 Live Set

### 4.1 Company Filters (4)
| Filter | Sub-tasks | Acceptance |
|--------|-----------|------------|
| **Company Name** | Facet combobox + include/exclude tokens; wire to `companies` / `excludedCompanies` | Substring match narrows results |
| **Country** | ISO include/exclude (`COUNTRY_FILTER_OPTIONS`, `countries` draft) | Multi-country works; US default |
| **Industry** | Multi-select facet combobox | OR within, AND across dimensions |
| **Employee Size** | Range/bucket selector | Buckets match enrichment data |

### 4.2 Job Filters (8)
| Filter | Sub-tasks | Acceptance |
|--------|-----------|------------|
| **Title** | Text facet combobox + custom tokens | `titles` / `excludedTitles` |
| **Location** | US state/location tokens | State-wise selection |
| **Date Posted** | Presets: Today, 7d, 30d, Any, custom | Local TZ boundaries → RFC3339 |
| **Experience Level** | Buckets: entry, mid, senior, director, etc. | `experienceBuckets` |
| **Job Type** | Multi-select: Full-time, Contract, etc. | `employmentTypes` |
| **LinkedIn Apply** | Toggle → `ComplexOnsiteApply` | Only LinkedIn Apply jobs |
| **Department** | `function_category` only in v1 (PRD alignment) | `HiringSignalsFilterSidebar` field |
| **Job Function** | Sub-filter under department (if separate in v1 criteria) | Maps to `functionCategory` |

### 4.3 Filter Infrastructure
| Step | Task | Done when |
|------|------|-----------|
| 4.3.1 | Draft state (`HireSignalFilterProvider`) | Sidebar draft separate from applied |
| 4.3.2 | Debounced auto-apply (~350ms) | No manual Apply button |
| 4.3.3 | Active filter chips + clear per section | UX matches PRD |
| 4.3.4 | Monotonic filter verification QA | Adding constraint reduces or maintains `total` |

### 4.4 Explicitly Out of Scope (v1)
- Remote / Workplace filter (PRD removed)
- View filter (removed)
- Revenue, Funding, Education, Skills, Compliance, Compensation (v1.1+)

---

## Epic 5: Email Notifications (v1 Core)

| Step | Task | Done when |
|------|------|-----------|
| 5.1 | Saved search ↔ notification config link | `job_email_notification.py` resolves by filter JSON |
| 5.2 | Trigger: new job matches saved filters | Worker detects new matches |
| 5.3 | Frequency: instant (`new_job_mode: instant`) | Real-time email |
| 5.4 | Frequency: delayed (2h, 6h, 12h, etc.) | `new_job_delay_hours` honored |
| 5.5 | Per saved search enable/disable | `SavedSearchEmailNotifyModal` |
| 5.6 | Email template: title, company, location, date, dashboard link | `DAILY_JOBS_TEMPLATE_ID` |
| 5.7 | User notification settings page | Profile/settings integration |

---

## Epic 6: Contact Intelligence (v1 Core)

| Step | Task | Done when |
|------|------|-----------|
| 6.1 | Surface contacts for hiring company | Drawer contacts grid |
| 6.2 | Always visible: First Name, Job Title, Department, LinkedIn | No gate |
| 6.3 | Work email masked until reveal | `HiringSignalDrawerContactsGrid`, `JobConnectraModal` |
| 6.4 | Reveal flow: FreeUser local / ProUser API | `email.findEmails` for Pro |
| 6.5 | Connectra integration for people data | Company website → finder |
| 6.6 | Phone number | **Deferred to v1.3** |

---

## Epic 7: v1 QA & Launch Gate

| Check | Target |
|-------|--------|
| Dashboard load | &lt; 3 seconds |
| Job freshness | &lt; 30 minutes |
| Platforms live | LinkedIn only |
| Filters | 4 company + 8 job |
| Notifications | End-to-end test pass |
| Contact reveal | Mask + reveal works |
| P0 bugs | 0 before v1.1 starts |

---

### v1 Implementation Notes (codebase today)
- Dashboard, saved searches side panel, LinkedIn ingest, email notification plumbing, and contact reveal are largely in place.
- Some v1.1 filters exist in UI but are **admin-gated** (`canUseAdvancedJobFilters`) or show **Coming Soon** for regular users.
- Company filters Industry/Employee Size/Revenue/Funding show Coming Soon for non-admin in `HiringSignalsCompanyFilters.tsx` — v1 may still need **full ProUser rollout** of the 4 company filters.

---

# VERSION 1.1 — Expansion & Closed Beta

**Objective:** Advanced filters, Indeed + 1 platform, better dedup, performance, monitoring. Target: **3–5 beta clients**.

**Success bar:** 2+ platforms · 12 filters (excl. Revenue) · load &lt; 2.5s · freshness &lt; 20 min · 0 P0.

**Prerequisite:** v1 stable.

---

## Epic 8: Additional Job Integrations

### 8.1 Indeed
| Step | Task | Done when |
|------|------|-----------|
| 8.1.1 | Indeed scraper/API adapter | Jobs ingested to `indeed` index |
| 8.1.2 | Indeed → normalized schema mapping | Same PRD fields where possible |
| 8.1.3 | Indeed company enrichment on ingest | Employer → company UUID |
| 8.1.4 | `source_platform: indeed` on unified list | Dashboard shows source |

### 8.2 Second Platform (TBD)
| Step | Task | Done when |
|------|------|-----------|
| 8.2.1 | Product picks platform (Glassdoor, ZipRecruiter, etc.) | Decision recorded |
| 8.2.2 | Adapter + normalization | Same pipeline as Indeed |
| 8.2.3 | Beta validation with real data | Sample jobs visible in UI |

### 8.3 Cross-Source Deduplication
| Step | Task | Done when |
|------|------|-----------|
| 8.3.1 | Define dedup key (title + company + location fuzzy match) | Spec documented |
| 8.3.2 | Merge duplicate signals → single row | User sees one signal |
| 8.3.3 | Preserve `source_platform` provenance | Audit which sources matched |
| 8.3.4 | Regression tests on LinkedIn-only + multi-source | No duplicate inflation |

---

## Epic 9: New Filters — v1.1 (5 job + 1 company)

### 9.1 Education
| Step | Sub-tasks |
|------|-----------|
| Parse | NLP/rules extract min education from `description_text` |
| Store | `education_required` / `education_level_min` on job doc |
| UI | Multi-select: High School, Bachelor's, Master's, PhD |
| API | `educationLevelMins` in `extendedJobFilters` |
| Rollout | Remove admin-only gate; enable for all Pro users |

### 9.2 Required Skills
| Step | Sub-tasks |
|------|-----------|
| Parse | NLP tag extraction from description |
| Store | `required_skills: string[]` |
| UI | Tag-based multi-select (`skillsAll`) |
| API | Skills filter in job.server query |
| QA | Spot-check parsed skills vs JD text |

### 9.3 Compliance & Preferences
| Step | Sub-tasks |
|------|-----------|
| Parse | Visa/H1B, security clearance, EEO flags from text |
| Store | `visa_sponsorship`, `clearance_mode`, etc. |
| UI | Multi-select + H1B checkbox |
| API | `clearanceMode`, `h1bOnly` filters |

### 9.4 Compensation
| Step | Sub-tasks |
|------|-----------|
| Parse | `salary_min`, `salary_max` from platform or description |
| UI | Range selector (hourly/annual) |
| API | `salaryMinUsd` / extended compensation fields |
| Edge cases | "Not disclosed" jobs handled gracefully |

### 9.5 Funding (Company)
| Step | Sub-tasks |
|------|-----------|
| Enrich | Company funding stage from enrichment provider |
| Store | `funding_stage` on company profile |
| UI | Multi-select: Seed, Series A/B/C, Public, Bootstrapped |
| API | Company cohort filter via funding buckets |

### 9.6 Filter Rollout (all v1.1 filters)
| Step | Task |
|------|------|
| Remove `HiringSignalFilterComingSoon` for Pro users | Filters usable by beta customers |
| Keep admin-only only where intentional | Document exceptions |
| Update PRD success criteria checklist | 12 filters live |

---

## Epic 10: NLP / Parsing Pipeline (v1.1 backbone)

| Step | Task | Done when |
|------|------|-----------|
| 10.1 | Batch parser on ingest (or async enrichment job) | New jobs get parsed fields |
| 10.2 | Backfill job for existing LinkedIn corpus | Historical jobs searchable by new filters |
| 10.3 | Parser accuracy sampling + manual review | Acceptable false positive rate |
| 10.4 | Index fields in OpenSearch for filter performance | Queries &lt; 500ms at scale |

---

## Epic 11: Stability & Performance (v1.1)

| Step | Task | Target |
|------|------|--------|
| 11.1 | Dashboard load optimization | &lt; 2.5s |
| 11.2 | Ingest cadence tuning | &lt; 20 min freshness |
| 11.3 | Integration failure monitoring | Alert on scraper/API failures |
| 11.4 | Internal status page | Ops sees platform health |
| 11.5 | Load test baseline | Document concurrent user limits |
| 11.6 | 0 P0 bugs gate | Before v1.2 planning |

---

## Epic 12: Closed Beta Program

| Step | Task | Done when |
|------|------|-----------|
| 12.1 | Select 3–5 staffing companies | Signed beta agreements |
| 12.2 | Onboarding docs + training | Users can self-serve filters + alerts |
| 12.3 | Feedback collection template | Structured input for v1.2 market-driven slots |
| 12.4 | Weekly bug/feedback triage | Issues categorized P0–P3 |
| 12.5 | Beta success review | Go/no-go for v1.2 dev kickoff |

---

### v1.1 Implementation Notes (codebase today)
- **Indeed ingest** exists in `EC2/job.server` (`apify_service.go`, `indeed` repos).
- **Advanced filter UI + API wiring** largely built; gating is the main gap for beta.
- **Company enrichment filters** (Industry, Employee Size) may need data pipeline completion, not just UI ungating.

---

# VERSION 1.2 — General Availability (GA)

**Objective:** Revenue filter, enterprise hardening, 2 customer-driven features, 6+ platforms, credits system.

**Success bar:** 99.9% uptime · 500 concurrent users · SOC 2 Type I readiness · WCAG 2.1 AA · all 6+6 filters · credits live · &gt;80% QA coverage.

**Prerequisite:** v1.1 stable + beta feedback collected.

---

## Epic 13: Revenue Filter (Last Company Filter)

| Step | Task | Done when |
|------|------|-----------|
| 13.1 | Company revenue enrichment integration | Annual revenue bands on company |
| 13.2 | Store `revenue` field (PRD schema) | Searchable in index |
| 13.3 | UI: revenue bucket multi-select | Remove Coming Soon |
| 13.4 | Company cohort filter via revenue | Jobs narrow by company revenue |
| 13.5 | Data coverage report | % of jobs with revenue metadata |

---

## Epic 14: Platform Integrations (6+ total)

| Step | Task | Done when |
|------|------|-----------|
| 14.1 | Glassdoor adapter | Normalized ingest |
| 14.2 | ZipRecruiter adapter | Normalized ingest |
| 14.3 | Monster adapter | Normalized ingest |
| 14.4 | CareerBuilder adapter | Normalized ingest |
| 14.5 | SimplyHired adapter | Normalized ingest |
| 14.6 | Unified multi-source list view | Single dashboard across 6+ |
| 14.7 | Source filter/badge in UI | User sees job origin |
| 14.8 | Dedup at scale across 6+ sources | No duplicate explosion |

---

## Epic 15: Contact Credits System

| Step | Task | Done when |
|------|------|-----------|
| 15.1 | Define credit model (reveals per plan) | Product spec |
| 15.2 | Credit balance on user/org | DB + API |
| 15.3 | Deduct on email reveal (Pro) | Atomic decrement |
| 15.4 | UI: credits remaining + upgrade CTA | Profile/billing |
| 15.5 | Audit log for reveals | Compliance |
| 15.6 | Prepare for v1.3 phone reveals | Extensible credit types |

---

## Epic 16: Enterprise Security & Compliance

| Step | Task | Target |
|------|------|--------|
| 16.1 | Full audit log (all user actions) | Every mutation logged |
| 16.2 | GDPR data handling | Export/delete user data |
| 16.3 | SOC 2 Type I readiness | Controls documented + implemented |
| 16.4 | Secrets rotation + access reviews | Ops runbook |
| 16.5 | Penetration test remediation | Critical findings closed |

---

## Epic 17: Performance & Reliability (GA bar)

| Step | Task | Target |
|------|------|--------|
| 17.1 | 99.9% uptime SLA | Monitoring + paging |
| 17.2 | Load test: 500 concurrent users | No degradation |
| 17.3 | Dashboard load | &lt; 2 seconds |
| 17.4 | Filter response | &lt; 500ms |
| 17.5 | Job freshness | &lt; 15 minutes |
| 17.6 | Disaster recovery drill | RTO/RPO documented |

---

## Epic 18: Accessibility & Quality

| Step | Task | Target |
|------|------|--------|
| 18.1 | WCAG 2.1 AA audit | Hiring signals + core flows |
| 18.2 | Keyboard nav + screen reader fixes | Filter sidebar, table, modals |
| 18.3 | QA automation &gt; 80% core flows | E2E + API tests |
| 18.4 | 0 P0 at GA launch | Release checklist signed |

---

## Epic 19: Market-Driven Features (2 slots — TBD)

**Process (from PRD §3.0):**
1. Collect feedback during v1 + v1.1 beta
2. Product evaluates and prioritizes
3. **Confirm exactly 2** before v1.2 dev starts
4. Lock scope — no additions mid-cycle

| Phase | Task |
|-------|------|
| Discovery | Synthesize top 10 customer requests |
| Prioritization | Score by impact × effort × strategic fit |
| Selection | Pick 2; document in PRD table |
| Delivery | Full epic per feature (spec → eng → QA → docs) |

**Likely candidates** (not in PRD — placeholders for planning):
- Phone number in contact intelligence (PRD says v1.3, but customers may pull it forward)
- CRM export integration
- Team-wide saved searches
- Advanced analytics dashboard
- API access for enterprise

---

## Epic 20: GA Launch Readiness Checklist

| Category | Criteria | Owner |
|----------|----------|-------|
| Uptime | 99.9% SLA | Eng/Ops |
| Performance | Dashboard &lt; 2s, filters &lt; 500ms | Eng |
| Data | Freshness &lt; 15 min, 6+ platforms | Data |
| Filters | All 6 company + 12 job | Product |
| Features | Contact intelligence + credits | Product |
| Security | Audit log, GDPR, SOC 2 Type I | Security |
| Quality | 0 P0, &gt;80% test coverage | QA |
| GTM | Pricing, support, onboarding | GTM |

---

# Cross-Version Workstreams (Continuous)

These run across all versions but deepen at each gate:

| Workstream | v1 | v1.1 | v1.2 |
|------------|----|----|------|
| **Data schema** | Core fields | + parsed fields | + revenue, full enrichment |
| **Search/index** | Basic facets | NLP fields indexed | Multi-source unified index |
| **Observability** | Basic logs | Alerts + status page | SLA dashboards |
| **Documentation** | `hiring-signals-ui.md` | Filter contract updates | GA runbooks |
| **Customer feedback** | Internal only | Beta program | GA + v2 planning |

---

# Suggested Sprint Mapping (High Level)

If each “version” ≈ 2–3 months:

| Sprint block | Focus |
|--------------|-------|
| **Sprints 1–4** | v1 Epics 1–3 (auth, ingest, dashboard) |
| **Sprints 5–6** | v1 Epics 4–6 (filters, email, contacts) |
| **Sprint 7** | v1 Epic 7 (QA gate) |
| **Sprints 8–9** | v1.1 Epics 8–10 (Indeed, parsers, filters) |
| **Sprint 10** | v1.1 Epics 11–12 (perf, beta) |
| **Sprints 11–14** | v1.2 Epics 13–18 (GA hardening) |
| **Sprint 15** | v1.2 Epic 19 (2 market features) + launch |

---

# Quick Reference: What Ships When

| Capability | v1 | v1.1 | v1.2 |
|------------|:--:|:----:|:----:|
| LinkedIn | ✅ | ✅ | ✅ |
| Indeed + 1 more | — | ✅ | ✅ |
| 6+ platforms | — | — | ✅ |
| Company filters (4) | ✅ | ✅ | ✅ |
| Funding filter | — | ✅ | ✅ |
| Revenue filter | — | — | ✅ |
| Job filters (8 basic) | ✅ | ✅ | ✅ |
| Job filters (4 advanced) | — | ✅ | ✅ |
| Email notifications | ✅ | ✅ | ✅ |
| Contact reveal (email) | ✅ | ✅ | ✅ |
| Contact credits | — | — | ✅ |
| Phone number | — | — | v1.3 |
| SOC 2 / GDPR / WCAG | — | — | ✅ |
| Market-driven extras | — | — | 2 features |

---

If you want to go deeper on one version, I can turn **v1 only** into a week-by-week engineering checklist mapped to specific files (`HiringSignalsFilterSidebar.tsx`, `job.server`, `job_email_notification.py`, etc.), or produce a **gap analysis** (PRD vs what’s already built). I’m in Ask mode, so that would stay as guidance unless you switch to Agent mode for implementation.

---

**User**

so now telll me the gaps b/w project codebases vs prd with version  , Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

I'll compare the PRD to the codebase across v1, v1.1, and v1.2 by checking auth, ingest, filters, notifications, contacts, and enterprise features.


# PRD vs Codebase Gap Analysis (by Version)

This compares `docs/prd/Contact360_Product_Documentation_v3.md` to what is in `contact360.io` (app + API) and `EC2/` (job.server, email.server, scraper.server).

**Overall pattern:** The codebase is **ahead on plumbing** (ingest, filter APIs, billing, notifications) but **behind on PRD-aligned rollout** — many v1/v1.1 features are built but **admin-gated**, and multi-platform / GA items are largely missing.

---

## How to Read This

| Status | Meaning |
|--------|---------|
| ✅ Aligned | Matches PRD intent for that version |
| 🟡 Partial | Exists but incomplete, gated, or behavior differs |
| ❌ Missing | Not implemented or not wired end-to-end |
| ⚡ Ahead | Built before PRD version or beyond PRD scope |

---

# VERSION 1 — Foundation

**PRD bar:** LinkedIn only · 4 company + 8 job filters for users · dashboard · saved searches · email alerts · contact reveal · export 500 rows · freshness &lt; 30 min.

## v1 Status Summary

| Area | PRD | Codebase | Gap severity |
|------|-----|----------|--------------|
| Auth & sessions | ✅ | ✅ | Low |
| Team invites | Owner + member | `inviteTeamMember` on profile | 🟡 No dedicated onboarding wizard |
| RBAC (5 roles) | FreeUser, ProUser, Admin, SuperAdmin, **Owner** | `OWNER` in constants but **not in `VALID_ROLES`**; frontend has no Owner tier | 🟡 |
| Billing | Basic scaffolding | Full billing module (plans, subscribe, credits) | ⚡ Ahead of v1 scope |
| LinkedIn ingest | ✅ | `job.server` ingest + `ApplyDerivedFieldsToJob` | ✅ |
| Auto fetch 15–30 min | Scheduled cadence | Manual / tracked scrape runs (`Runs` tab, reschedule) | 🟡 |
| Dashboard tabs | All Signals \| Today's Jobs | ✅ (`HiringSignalsListToolbar`) | ✅ |
| Saved searches | Side panel | `SavedSearchesMenu` | ✅ |
| Pagination 50 | ✅ | `useHiringSignals` default `limit: 50` | ✅ |
| Email notifications | Instant + custom delay | `SavedSearchEmailNotifyModal` + `email.server` `IngestNewJobs` | ✅ |
| Contact intelligence | 5 fields, masked email | `HiringSignalDrawerContactsGrid` | ✅ |
| Export XLSX | All users, max **500** | **Admin/SuperAdmin only**; cap **400** non-staff | ❌ |
| Company filters (4) | Live for v1 users | Name + Country ✅; **Industry + Employee Size admin-only** (`ComingSoon`) | ❌ |
| Job filters (8) | Live for v1 users | Most wired; **Department = `function_category` only** | 🟡 |
| Location | US **state dropdown** | Text facet combobox (`locations`) | 🟡 |
| Remote / Workplace | **Removed** in PRD | Still in `HiringSignalsFilterSidebar` | ❌ PRD drift |
| Cross-source dedup | Same job once (v1: LinkedIn only) | Per-source upsert only | ✅ for v1 |
| Performance SLA | &lt; 3s dashboard | Not measured in repo | 🟡 |

---

## v1 Gaps — Broken Into Steps

### Gap 1.1 — Company filters not live for target users (Critical)

**PRD:** Industry + Employee Size ship in v1 for staffing users.  
**Code:** Only Admin/SuperAdmin see real controls; others get `HiringSignalFilterComingSoon`.

| Step | Action |
|------|--------|
| 1 | Confirm company enrichment coverage (% jobs with industry + headcount) |
| 2 | Change gating from `isAdmin \|\| isSuperAdmin` → `ProUser` (or plan-based) per PRD |
| 3 | QA monotonic filter behavior for Industry + Employee Size |
| 4 | Update docs/PRD alignment table if admin-only was intentional |

---

### Gap 1.2 — Export not matching PRD (Critical)

**PRD:** Export to XLSX up to **500 rows** for product users.  
**Code:** `canExportHireSignalXlsx = isAdmin || isSuperAdmin`; `MAX_EXPORT_LINKEDIN_JOB_IDS_NON_STAFF = 400`.

| Step | Action |
|------|--------|
| 1 | Open export to `ProUser` (and optionally `FreeUser` with lower cap) |
| 2 | Raise non-staff cap from 400 → **500** (`export_jobs.py` + frontend modal) |
| 3 | Align credit deduction policy with billing docs if export costs credits |
| 4 | E2E test: Pro user exports 500 selected rows |

---

### Gap 1.3 — RBAC Owner role incomplete (Medium)

**PRD:** Owner is a first-class role.  
**Code:** `OWNER = "Owner"` exists; `VALID_ROLES` omits it; `RoleContext` has no Owner mapping.

| Step | Action |
|------|--------|
| 1 | Add `Owner` to `VALID_ROLES` and auth assignment paths |
| 2 | Define Owner permissions (team mgmt, billing, vs Admin) |
| 3 | Map Owner in frontend `RoleContext` / GraphQL types |
| 4 | Add tests for Owner-only mutations (invites, billing) |

---

### Gap 1.4 — Department vs Job Function (Medium)

**PRD:** 8 job filters including **Department** and **Job Function** separately.  
**Code (PRD v2.1):** v1 uses **`function_category` only** as “Job Department”.

| Step | Action |
|------|--------|
| 1 | Decide: PRD success criteria (8 filters) vs implementation note (single field) |
| 2 | If keeping single field, update PRD §3.1.7 count to avoid QA confusion |
| 3 | If splitting, add sub-function facet under department in UI + API |

---

### Gap 1.5 — Location filter shape (Low–Medium)

**PRD:** US state-wise dropdown.  
**Code:** Free-text / facet location tokens + separate country filter.

| Step | Action |
|------|--------|
| 1 | Add US states static list or facet field `location_state` |
| 2 | Map PRD `location_state` schema field to filter UI |
| 3 | Keep free-text as advanced option if needed |

---

### Gap 1.6 — Remote / Workplace filter should not exist in v1.x (Medium)

**PRD §2.3:** Removed from scope.  
**Code:** “Remote / workplace” section still active for all users.

| Step | Action |
|------|--------|
| 1 | Hide or remove workplace filter from customer UI |
| 2 | Strip `workplaceTypes` from default saved-search payloads if deprecated |
| 3 | Document in `hiring-signals-ui.md` as internal-only if retained for staff |

---

### Gap 1.7 — Automated ingest cadence (Medium)

**PRD:** Real-time fetch every **15–30 minutes**.  
**Code:** Scrape runs are **queued manually** or rescheduled per run; no clear global 15–30 min scheduler in app layer.

| Step | Action |
|------|--------|
| 1 | Define production scrape schedule (cron / satellite worker) |
| 2 | Expose “last updated” SLA monitoring |
| 3 | Alert if freshness &gt; 30 min (v1 target) |

---

### Gap 1.8 — Extra features not in v1 PRD (Informational)

**Code ahead / scope creep:**
- **Runs** tab (admin-only scrape queue)
- **Data quality** filters (super-admin)
- **Market insights / Demands** pages sharing hire-signal filters
- **Global search** toolbar row

These are not v1 gaps to “build” — they are **documentation / GTM** gaps if customers see them unexpectedly.

---

# VERSION 1.1 — Beta Expansion

**PRD bar:** Indeed + 1 TBD platform · 12 filters (excl. Revenue) · cross-source dedup · perf &lt; 2.5s · freshness &lt; 20 min · monitoring · 3–5 beta clients.

## v1.1 Status Summary

| Area | PRD | Codebase | Gap |
|------|-----|----------|-----|
| Indeed integration | v1.1 | `job.server` Indeed repos + Apify ingest | 🟡 Ingest only |
| Unified job dashboard | Multi-source signals | `hire_signal` GraphQL = **LinkedIn only** (`linkedin_job_id` everywhere) | ❌ |
| 2nd platform | TBD | Not implemented | ❌ |
| Cross-source dedup | Same job across sources once | Per-platform upsert; **no merge layer** | ❌ |
| Education filter | v1.1 live | API ✅; UI **admin-gated** | 🟡 |
| Required Skills | NLP-parsed tags | Regex/keyword `skillKeywords` in `job_derived.go` | 🟡 |
| Compliance | Visa, clearance, EEO | H1B + clearance + US citizen; **no EEO flags** | 🟡 |
| Compensation | Salary range | `salary_min_usd` derived; UI **admin-gated** | 🟡 |
| Funding (company) | v1.1 | Backend + UI exist; **admin-gated** | 🟡 |
| Internal status page | v1.1 | Not found in repo | ❌ |
| Integration alerting | v1.1 | Logs only | 🟡 |
| Closed beta program | 3–5 clients | Process not in codebase | ❌ (ops) |
| Perf / freshness SLA | &lt; 2.5s / &lt; 20 min | Not verified | 🟡 |

---

## v1.1 Gaps — Broken Into Steps

### Gap 2.1 — Indeed not in the product surface (Critical)

**Ingest exists; product does not consume it.**

| Step | Action |
|------|--------|
| 1 | Add unified `signal_id` / multi-source list in `job.server` OR federated GraphQL query |
| 2 | Replace `linkedinJobId`-only types with source-agnostic job key |
| 3 | Show `source_platform` column/badge in `HiringSignalsDataTable` |
| 4 | Update export, saved searches, notifications to use unified IDs |
| 5 | Migrate `hire_signal` mutations (applied jobs, export) off LinkedIn-only naming |

---

### Gap 2.2 — Cross-source deduplication (Critical)

**PRD:** Same job from LinkedIn + Indeed shown once.

| Step | Action |
|------|--------|
| 1 | Define dedup fingerprint (normalized title + company + location + posted date window) |
| 2 | Build merge index or canonical `signal_id` with `sources[]` |
| 3 | Backfill dedup across existing LinkedIn + Indeed corpora |
| 4 | Add tests for near-duplicate pairs |

---

### Gap 2.3 — v1.1 filters not rolled out to beta users (Critical)

**Backend ready in `jobs_handlers.go` + `job_list_opensearch_query.go`; UI blocks non-admin.**

| Step | Action |
|------|--------|
| 1 | Ungate Education, Skills, Compliance, Compensation for `ProUser` |
| 2 | Ungate Funding (company) for v1.1 — currently grouped with v1.2 Revenue in same admin gate |
| 3 | Remove `HiringSignalFilterComingSoon` for shipped filters |
| 4 | Run PRD verification checklist (`hiring-signals-ui.md` § Verification) per filter |

---

### Gap 2.4 — Skills parsing weaker than PRD (Medium)

**PRD:** “NLP parsed from job descriptions.”  
**Code:** Fixed keyword list in `job_derived.go` (~20 tech terms).

| Step | Action |
|------|--------|
| 1 | Expand skill taxonomy or plug NLP extractor |
| 2 | Backfill `skill_tags` on historical jobs |
| 3 | Validate precision/recall on beta sample set |

---

### Gap 2.5 — Second job platform (High)

| Step | Action |
|------|--------|
| 1 | Product selects platform (Glassdoor, ZipRecruiter, etc.) |
| 2 | Clone Indeed adapter pattern in `job.server` |
| 3 | Wire into unified list + dedup |
| 4 | Beta validation with real data |

---

### Gap 2.6 — Ops / reliability (Medium)

| Step | Action |
|------|--------|
| 1 | Build internal status page (scraper, job.server, email.server health) |
| 2 | Pager/alert on ingest failure rates |
| 3 | Load test dashboard + filter API; document p95 |
| 4 | Stand up beta client onboarding + feedback capture (for v1.2 slots) |

---

# VERSION 1.2 — General Availability

**PRD bar:** Revenue filter · 6+ platforms · 99.9% uptime · 500 concurrent users · SOC 2 / GDPR · full audit log · WCAG 2.1 AA · contact credits · &gt;80% QA · 2 market features.

## v1.2 Status Summary

| Area | PRD | Codebase | Gap |
|------|-----|----------|-----|
| Revenue filter | v1.2 | Backend + UI built; **admin-gated** | 🟡 Early build, not GA rollout |
| 6+ platforms | v1.2 | **LinkedIn + Indeed** only | ❌ |
| Contact credits | v1.2 GA | **Credits live now** on `email.findEmails` (daily plan + addon) | ⚡ Ahead, but not PRD-isolated to v1.2 |
| Phone number | v1.3 | Not in contacts grid | ✅ Expected deferral |
| 99.9% SLA | v1.2 | No SLA infra in repo | ❌ |
| 500 concurrent users load test | v1.2 | Not evidenced | ❌ |
| SOC 2 Type I | v1.2 | PRD only | ❌ |
| GDPR | v1.2 | PRD only | ❌ |
| Full audit log (all actions) | v1.2 | `graphql_audit_events` on **some** admin/billing mutations only | 🟡 |
| WCAG 2.1 AA | v1.2 | No compliance program | ❌ |
| Filter &lt; 500ms / dashboard &lt; 2s | v1.2 | Not verified | 🟡 |
| Freshness &lt; 15 min | v1.2 | Depends on scrape schedule gap | 🟡 |
| QA &gt; 80% core flows | v1.2 | Tests exist (`hiringSignalFilterDraft.test.ts`, API tests) — **coverage unknown** | 🟡 |
| 2 market-driven features | v1.2 | TBD in PRD | ❌ |

---

## v1.2 Gaps — Broken Into Steps

### Gap 3.1 — Revenue filter GA rollout (High)

**Built early; needs enrichment + customer access.**

| Step | Action |
|------|--------|
| 1 | Measure company revenue field coverage in index |
| 2 | Ungate Revenue filter for GA users (not admin-only) |
| 3 | Validate cohort query performance at scale |
| 4 | Document enrichment source + refresh cadence |

---

### Gap 3.2 — Platform scale to 6+ (Critical)

| Step | Action |
|------|--------|
| 1 | Prioritize Glassdoor, ZipRecruiter, Monster, CareerBuilder, SimplyHired |
| 2 | One adapter template (ingest → normalize → index) |
| 3 | Unified list + dedup (depends on Gap 2.1–2.2) |
| 4 | Source-specific monitoring per integration |

---

### Gap 3.3 — Enterprise security & compliance (Critical)

| Step | Action |
|------|--------|
| 1 | Extend audit logging to **all** user mutations (filters, exports, reveals, saved searches) |
| 2 | GDPR: data export + delete-user flows |
| 3 | SOC 2 Type I control mapping + evidence collection |
| 4 | Security review + pen test remediation |
| 5 | WCAG audit on hiring-signals flow (sidebar accordion, table, modals) |

---

### Gap 3.4 — Credits model vs PRD timeline (Medium)

**PRD:** Credits for contact intelligence at **v1.2 GA**.  
**Code:** Credits already deduct on email finder; **FreeUser reveals stored email locally without API/credits**.

| Step | Action |
|------|--------|
| 1 | Align product rules: should FreeUser reveal consume credits? |
| 2 | Unify reveal path through API for auditable credit deduction |
| 3 | UI: credits remaining on reveal actions in hiring drawer |
| 4 | Prepare credit types for v1.3 phone reveals |

---

### Gap 3.5 — Performance & reliability program (High)

| Step | Action |
|------|--------|
| 1 | Define SLOs: uptime 99.9%, dashboard p95 &lt; 2s, filters p95 &lt; 500ms |
| 2 | Load test 500 concurrent users on hire-signal list + filters |
| 3 | Automate freshness checks (&lt; 15 min) with alerts |
| 4 | Chaos/failover runbook for job.server + OpenSearch |

---

### Gap 3.6 — Market-driven features (Process gap)

| Step | Action |
|------|--------|
| 1 | Collect top requests from v1/v1.1 beta |
| 2 | Product locks **exactly 2** before v1.2 dev |
| 3 | Estimate + schedule as Epics 19.1 and 19.2 |
| 4 | Do not start v1.2 feature dev until v1.1 stability gate passes |

---

# Cross-Version Architecture Gaps

These block multiple versions:

```mermaid
flowchart TB
    subgraph built [Built in Code]
        LI[LinkedIn Index]
        IN[Indeed Index]
        FILT[Full Filter API]
        UI[Hiring Signals UI]
    end

    subgraph missing [Missing Product Layer]
        UNI[Unified Signal List]
        DEDUP[Cross-Source Dedup]
        GATE[ProUser Filter Rollout]
        GA[Enterprise GA Shell]
    end

    LI --> UNI
    IN --> UNI
    UNI --> DEDUP
    FILT --> GATE
    UI --> GATE
    GATE --> GA
```

| # | Architectural gap | Blocks |
|---|-------------------|--------|
| A | LinkedIn-centric IDs (`linkedinJobId`) | v1.1 unified dashboard, export, notifications |
| B | Separate indexes per platform | v1.1 dedup, v1.2 6+ platforms |
| C | Admin-gated filters despite full API | v1 company filters, v1.1 advanced filters |
| D | No production freshness SLA | v1, v1.1, v1.2 data targets |
| E | Partial audit / no compliance program | v1.2 GA checklist |

---

# Suggested Closure Order (Practical)

If the goal is **PRD truth** with minimum rework:

### Phase 1 — Close v1 for real users
1. Ungate Industry + Employee Size for ProUser  
2. Open export to ProUser (500 cap)  
3. Fix Owner role in `VALID_ROLES` + frontend  
4. Remove/hide Remote filter per PRD  
5. Document or implement 15–30 min scrape schedule  

### Phase 2 — Make v1.1 real (not just admin preview)
1. Unified multi-source job list API  
2. Cross-source dedup  
3. Ungate v1.1 filters + Funding  
4. Surface Indeed in dashboard  
5. Second platform + status page  

### Phase 3 — v1.2 GA
1. Revenue GA + enrichment coverage  
2. 4 more platforms  
3. Audit/compliance/accessibility program  
4. Load + SLO verification  
5. Two market-driven features from beta feedback  

---

# Quick Scorecard

| Version | PRD readiness (estimate) | Biggest blocker |
|---------|--------------------------|-----------------|
| **v1** | ~**70%** | Company filters + export gated to admin; Owner incomplete |
| **v1.1** | ~**45%** | Indeed not in UI; filters admin-gated; no cross-source dedup |
| **v1.2** | ~**15%** | 4+ platforms missing; no enterprise compliance/SLA program |

---

The codebase looks like an **internal/staff build** that implemented v1.2-shaped APIs early, while the **customer-facing version gates** in the PRD were never switched on. The highest-leverage work is not new features — it is **rollout + unified multi-source product layer**.

If you want next, I can produce a **file-level gap map** (exact files to touch per gap) or a **v1-only closure checklist** with acceptance tests — still in Ask mode, so guidance only unless you switch to Agent mode.

---

**User**

so now telll me the gaps b/w project codebases vs prd with version 1 , so now we want to start version contact360 1.0 , so all things shows for super admin and admin but free user and pro user shows only version 1.0 , Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

I'll map PRD v1.0 scope against current role gating so we can define exactly what Free/Pro users should see versus Admin/SuperAdmin.


# Contact 360 v1.0 Launch — PRD vs Codebase Gaps

Your target model:

| Role | What they see |
|------|----------------|
| **SuperAdmin + Admin** | Full product (current build + future filters, Runs, export at scale, ops tools) |
| **FreeUser + ProUser** | **Only PRD v1.0** — core hiring signals, 12 filters, notifications, contacts, export |

Right now the codebase mostly gates by **Admin/SuperAdmin**, not by **product version**. Several **v1.0 filters are wrongly hidden** from Free/Pro, while several **non-v1 features are still visible** to them.

---

## Step 1 — Define the v1.0 Contract (Free/Pro manifest)

From PRD §3.1, this is the **only** surface Free/Pro should get at launch.

### Platform
| Feature | v1.0 |
|---------|------|
| Auth (email/password) | ✅ |
| Team invites | ✅ (basic) |
| Billing | Scaffolding only (not full enterprise billing UX) |
| Roles | FreeUser + ProUser customer roles |

### Data
| Feature | v1.0 |
|---------|------|
| Job source | **LinkedIn only** |
| Fetch freshness | &lt; 30 min (ops target) |
| Deduplication | Per LinkedIn job ID |

### Dashboard (`/hiring-signals`)
| Feature | v1.0 |
|---------|------|
| Table columns | Title, Company, Location, Type, Posted, Actions |
| Tabs | **All Signals** \| **Today's Jobs** |
| Saved searches | Side panel (`SavedSearchesMenu`) |
| Pagination | 50/page |
| Refresh + total count | ✅ |
| Export XLSX | **Up to 500 rows** |
| **Hidden** | Runs tab, scrape modal, run filter chip, data-quality block |

### Company filters (4)
1. Company Name  
2. Country (ISO include/exclude)  
3. Industry  
4. Employee Size  

### Job filters (8 per PRD success criteria)
1. Title  
2. Location (US state-wise — PRD intent)  
3. Date Posted  
4. Experience Level  
5. Job Type  
6. LinkedIn Apply (toggle)  
7. Job Department (`function_category`)  
8. Job Function (PRD lists separately; code uses single **Job Department** field in v2.1 alignment)

### Email notifications
- Per saved search  
- Instant or delayed (PRD: 2h, 6h, 12h)  
- Email: title, company, location, date, dashboard link  

### Contact intelligence
- First Name, Job Title, Department, LinkedIn — visible  
- Work email — masked until reveal  
- Phone — **not v1.0**  

### Explicitly NOT v1.0 (hide from Free/Pro)
- Remote / Workplace (PRD §2.3 removed)  
- Category (Topic)  
- Education, Skills, Compliance, Compensation (v1.1)  
- Revenue, Funding (v1.1/v1.2)  
- Data quality filters (internal)  
- Demands & Trends, Market Insights nav  
- Runs / scrape tooling  

---

## Step 2 — Current Gating vs Desired Model

```mermaid
flowchart LR
    subgraph today [Today in Code]
        A[Admin/SuperAdmin] --> ALL[Almost all filters + export]
        F[Free/Pro] --> CS[Coming Soon on v1 filters]
        F --> EXTRA[Sees v1.1 UI sections + extra nav]
    end

    subgraph target [v1.0 Target]
        A2[Admin/SuperAdmin] --> ALL2[Full preview build]
        F2[Free/Pro] --> V1[v1.0 manifest only]
    end
```

### Central gating locations today

| File | Current logic | Problem |
|------|---------------|---------|
| `HiringSignalsCompanyFilters.tsx` | `canUseAdvancedCompanyCohortFilters = isAdmin \|\| isSuperAdmin` | **Industry + Employee Size** blocked for Free/Pro — they are **v1.0** |
| `HiringSignalsFilterSidebar.tsx` | `canUseAdvancedJobFilters = isAdmin \|\| isSuperAdmin` | v1.1 filters admin-only ✅, but **v1 extras** (Remote, Category shell) still visible |
| `HiringSignalsPageClient.tsx` | Export + Runs admin-only | Export should be **v1.0 for Free/Pro** (500 cap) |
| `navConfig.ts` | Demands/Market Insights in **Database** for everyone | Not v1.0 — should hide for Free/Pro |
| `hiring-signals-ui.md` | `applyFilters` sends **full** `JobListFilters` for every role | API not version-enforced |

---

## Step 3 — v1.0 Gap Matrix (PRD vs Code)

### Legend
- ✅ Aligned  
- 🟡 Partial  
- ❌ Gap  
- 🔒 Should stay admin-only  

| # | Area | PRD v1.0 (Free/Pro) | Code today (Free/Pro) | Gap |
|---|------|---------------------|------------------------|-----|
| **A** | **Industry filter** | Live | `ComingSoon` | ❌ **Critical** |
| **B** | **Employee Size filter** | Live | `ComingSoon` | ❌ **Critical** |
| **C** | Company Name | Live | ✅ | ✅ |
| **D** | Company Country | Live | ✅ | ✅ |
| **E** | Title, Date Posted, Job Type | Live | ✅ | ✅ |
| **F** | Experience Level | Live | ✅ (seniority + bucket — richer than PRD) | 🟡 Simplify UI? |
| **G** | LinkedIn Apply | Toggle | 3 checkboxes + dropdown | 🟡 Simplify to PRD toggle |
| **H** | Job Department | `function_category` | ✅ | ✅ |
| **I** | Location | US state dropdown | Text facet + job country in section | 🟡 |
| **J** | Remote / Workplace | **Removed** | **Visible to all** | ❌ |
| **K** | Category (Topic) | Not v1 | Section visible (`ComingSoon`) | 🟡 Hide section entirely |
| **L** | Education/Skills/Compliance/Compensation | v1.1 | `ComingSoon` sections visible | 🟡 Hide for Free/Pro |
| **M** | Revenue / Funding | v1.1/v1.2 | `ComingSoon` in company filters | 🟡 Hide for Free/Pro |
| **N** | Export XLSX 500 | All users | Admin-only; cap 400 | ❌ **Critical** |
| **O** | Saved searches + email notify | Live | ✅ UI exists | 🟡 Verify E2E |
| **P** | Email delay options | 2h, 6h, 12h | 1, 3, 6, 12, 24h | 🟡 |
| **Q** | Contact reveal | Mask + reveal | ✅ Free local / Pro API | ✅ |
| **R** | Dashboard tabs | All \| Today | ✅ | ✅ |
| **S** | Pagination 50 | ✅ | ✅ | ✅ |
| **T** | Runs / scrape | Not v1 | Hidden for Free/Pro | ✅ |
| **U** | Data quality filters | Not v1 | SuperAdmin only | ✅ |
| **V** | Demands & Market Insights nav | Not v1 | **Visible to all** | ❌ |
| **W** | API filter enforcement | v1 only | No server-side version strip | ❌ **Security** |
| **X** | LinkedIn-only data | ✅ | ✅ (hire_signal is LinkedIn-centric) | ✅ |
| **Y** | Auto ingest 15–30 min | Ops SLA | Manual/triggered runs | 🟡 Ops gap |
| **Z** | Owner role | v1 RBAC | `OWNER` not in `VALID_ROLES` | 🟡 |

---

## Step 4 — Implementation Plan (Small Steps)

Organize work into **6 epics**. Each epic has ordered sub-tasks.

---

### Epic 1 — Version feature registry (foundation)

**Goal:** One source of truth for “what is v1.0 vs preview”.

| Step | Task |
|------|------|
| 1.1 | Add `PRODUCT_VERSION = "1.0"` config (env or `lib/productVersion.ts`) |
| 1.2 | Define `V1_0_FEATURES` enum: filter section IDs, toolbar actions, nav routes |
| 1.3 | Add helper `isStaffUser(role)` → Admin \|\| SuperAdmin |
| 1.4 | Add helper `canUseFeature(feature, role)` → staff = all; Free/Pro = v1 manifest |
| 1.5 | Document manifest in `docs/prd` or `app/docs/hiring-signals-v1.md` |

**Acceptance:** Any component can ask “is this v1.0 for this user?” in one call.

---

### Epic 2 — Filter sidebar: show v1.0 to Free/Pro, full to staff

**Primary files:**  
`HiringSignalsCompanyFilters.tsx`, `HiringSignalsFilterSidebar.tsx`, `hsFilterSectionIds.ts`

#### 2A — Fix critical v1.0 regressions (Free/Pro)

| Step | Task |
|------|------|
| 2A.1 | Change Industry gate: `canUseAdvancedCompanyCohortFilters` → `isStaffUser \|\| isV10CompanyFilter('industry')` |
| 2A.2 | Same for Employee Size |
| 2A.3 | Remove `HiringSignalFilterComingSoon` for Industry + Employee Size for Free/Pro |
| 2A.4 | QA: Pro user selects Industry → `total` decreases monotonically |

#### 2B — Hide non-v1.0 sections from Free/Pro (don’t show “Coming soon”)

| Step | Task |
|------|------|
| 2B.1 | Wrap **Remote / workplace** section: `{isStaff && <HsFilterSection ...>}` |
| 2B.2 | Hide **Category (Topic)** section for Free/Pro |
| 2B.3 | Hide **Education, Skills, Compliance, Compensation** sections for Free/Pro |
| 2B.4 | Hide **Revenue, Funding** company sections for Free/Pro |
| 2B.5 | Keep all sections for Admin/SuperAdmin unchanged |

#### 2C — Simplify v1.0 job filters (optional polish)

| Step | Task |
|------|------|
| 2C.1 | LinkedIn Apply: single toggle → `ComplexOnsiteApply` for Free/Pro; keep full control for staff |
| 2C.2 | Experience: hide “Seniority regex” sub-control for Free/Pro; keep experience buckets only |
| 2C.3 | Location: add US states `Select` for Free/Pro; keep facet combobox for staff |

#### 2D — Strip applied filters on save/apply

| Step | Task |
|------|------|
| 2D.1 | In `HireSignalFilterContext` / `applyFilters`, run `stripNonV10Filters(draft, role)` for Free/Pro |
| 2D.2 | When loading saved search with v1.1 fields, ignore unknown keys for Free/Pro + toast |

**Acceptance (Free/Pro sidebar):** Exactly 4 company + 8 job filter sections visible; no “Coming soon” on v1 filters.

---

### Epic 3 — Dashboard & toolbar v1.0

**Primary file:** `HiringSignalsPageClient.tsx`, `HiringSignalsListToolbar.tsx`

| Step | Task |
|------|------|
| 3.1 | Export: `canExportHireSignalXlsx = isStaff \|\| isV10Feature('export')` → true for Free/Pro |
| 3.2 | Set `HS_EXPORT_MAX_IDS_NON_STAFF = 500` (sync API `export_jobs.py`) |
| 3.3 | Pro/Free export toast: “max 500 rows per export” |
| 3.4 | Confirm Runs tab stays `showRunsTab = isAdmin` only |
| 3.5 | Confirm `RunScrapeModal` stays SuperAdmin only |
| 3.6 | Hide run-filter chip drill-down for Free/Pro if they can’t reach Runs |
| 3.7 | Verify columns match PRD (hide staff-only columns for Free/Pro if any) |

**Acceptance:** Pro user exports 500 matching jobs; Admin still gets staff cap.

---

### Epic 4 — Navigation & page access v1.0

**Primary file:** `navConfig.ts`

| Step | Task |
|------|------|
| 4.1 | Add `requiresStaff?: boolean` or `minProductVersion?: '1.0' \| 'preview'` on nav items |
| 4.2 | Hide **Demands & Trends** and **Market Insights** for Free/Pro |
| 4.3 | Keep **Hiring signals** + Dashboard + Activities + Contacts/Companies per GTM decision |
| 4.4 | Route guard: redirect Free/Pro from `/demands-*` and `/market-insights` if URL typed |
| 4.5 | Staff sees full Database section unchanged |

**Acceptance:** Free/Pro sidebar shows only v1.0-relevant destinations.

---

### Epic 5 — API / backend enforcement (don’t trust UI alone)

**Primary files:**  
`hire_signal/queries.py`, `hiringSignalService.ts` `buildExtendedJobFilters`, `HireSignalFilterContext.tsx`

| Step | Task |
|------|------|
| 5.1 | Gateway: `strip_hire_signal_filters_for_role(filters, role)` before job.server call |
| 5.2 | Strip for Free/Pro: `workplaceTypes`, `industries`, `skillsAll`, `educationLevelMins`, `clearanceMode`, `h1bOnly`, `salaryMinUsd`, `companyRevenue`, `companyFunding`, data-quality fields |
| 5.3 | **Allow** for Free/Pro: company name/country/industry/employee size + v1 job fields |
| 5.4 | Export mutation: allow Free/Pro with cap 500 |
| 5.5 | Add API tests: Free/Pro cannot filter by `skill` even if client sends it |
| 5.6 | Mirror strip in saved-search restore path |

**Acceptance:** Tampering with GraphQL variables cannot access v1.1 filters as Free/Pro.

---

### Epic 6 — Email notifications & contacts v1.0

| Step | Task |
|------|------|
| 6.1 | Verify `SavedSearchEmailNotifyModal` reachable for Free/Pro from saved searches panel |
| 6.2 | Align delay options with PRD: add **2h**; consider hiding 1h/3h/24h for Free/Pro |
| 6.3 | E2E test: save filter → enable instant notify → new job triggers email |
| 6.4 | Contact drawer: confirm 5 fields; no phone column |
| 6.5 | Document Free vs Pro reveal behavior (local vs API) as v1.0 acceptable |

---

### Epic 7 — Ops & launch gate (non-UI but v1.0 success criteria)

| Step | Task |
|------|------|
| 7.1 | Production LinkedIn scrape schedule (15–30 min) |
| 7.2 | Dashboard p95 load &lt; 3s smoke test |
| 7.3 | Freshness monitor (&lt; 30 min) |
| 7.4 | v1.0 QA checklist sign-off for Free/Pro + staff regression |

---

## Step 5 — What Admin/SuperAdmin Keep (Preview / Internal)

Staff should continue to see **everything already built** — this is your internal v1.1+ preview:

| Feature | Staff visibility |
|---------|------------------|
| Industry, Employee Size, Revenue, Funding | ✅ (already) |
| Education, Skills, Compliance, Compensation | ✅ |
| Category (Topic), Remote/Workplace | ✅ |
| Data quality filters | SuperAdmin only ✅ |
| Runs tab + scrape queue | Admin+ ✅ |
| Export 10M cap | Admin+ ✅ |
| Demands, Market Insights | ✅ (nav) |
| Run filter / drill-down | ✅ |

No need to remove staff features — only **add** correct v1.0 boundaries for Free/Pro.

---

## Step 6 — Priority Order for v1.0 Launch

```mermaid
flowchart TD
    P0[Epic 1 Version registry] --> P1[Epic 2A Industry + Employee Size for Free/Pro]
    P1 --> P2[Epic 3 Export 500 for Free/Pro]
    P2 --> P3[Epic 2B Hide non-v1 sections]
    P3 --> P4[Epic 5 API strip]
    P4 --> P5[Epic 4 Nav hide Demands/Market]
    P5 --> P6[Epic 6 Email E2E + Epic 7 Ops]
```

### P0 — Blockers (cannot call it v1.0 without these)
1. Industry + Employee Size live for Free/Pro  
2. Export open to Free/Pro with **500** cap  
3. Hide Remote/Workplace + v1.1 filter sections from Free/Pro  
4. API-side filter stripping  

### P1 — Important before external users
5. Nav: hide Demands & Market Insights  
6. Email notification E2E verification  
7. Scrape freshness SLA  

### P2 — Polish
8. US state location control  
9. LinkedIn Apply single toggle  
10. Email delay options match PRD (2h, 6h, 12h)  

---

## Step 7 — v1.0 Acceptance Checklist (Free/Pro user test)

Run as **ProUser** and **FreeUser**:

| # | Test | Pass criteria |
|---|------|---------------|
| 1 | Open Hiring signals | No Runs tab |
| 2 | Filter sidebar | 4 company + 8 job sections only |
| 3 | Industry filter | Works; no “Coming soon” |
| 4 | Employee size | Works |
| 5 | Remote / workplace | Section **not visible** |
| 6 | Education / Skills / etc. | Sections **not visible** |
| 7 | Revenue / Funding | **Not visible** |
| 8 | All Signals / Today's jobs | Both work |
| 9 | Save search + email notify | Save + instant/delayed works |
| 10 | Export | Up to 500 rows |
| 11 | Contact drawer | Email masked; reveal works |
| 12 | Sidebar nav | No Demands / Market Insights |
| 13 | API tamper test | v1.1 filter params ignored server-side |

Run as **Admin** — all current features still work.

---

## Bottom line

The biggest v1.0 problem is **inverted gating**:

- **v1.0 filters** (Industry, Employee Size) are hidden from customers  
- **Non-v1.0 filters** (Remote, v1.1 sections) are still shown (as “Coming soon” or live)  
- **Export** is staff-only though PRD makes it v1.0  

Your launch work is mainly **rebalancing visibility**: introduce a `v1.0 feature manifest`, **enable** the 4 company filters for Free/Pro, **hide** everything after v1.0, **open export**, and **enforce on the API**.

If you want next, I can produce a **file-by-file change list** (exact conditions to add per component) or a **single `canUseHireSignalFeature()` module design** — still Ask mode, so guidance only unless you switch to Agent mode for implementation.

---

**User**

Read all the above and previous prompts and their answers, then create a plan to do all the above and previous prompts and their answers, Learn, understand, and analyze deeply, breaking tasks into smaller steps

---

**Cursor**

Let me do a final read of the most critical files to confirm exact paths and current code before writing the plan.

Now I have all the detail I need. Let me create the comprehensive plan.

---

**User**

Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

---

**Cursor**

I'll implement the v1.0 launch plan task by task, starting with the product version helper.


Implementing the changes now.


# Contact 360 v1.0 Launch — Implemented

All 7 plan tasks are done. Summary of changes:

## 1. Version helper
- Added [`contact360.io/app/src/lib/productVersion.ts`](contact360.io/app/src/lib/productVersion.ts) with `isStaffRole()` and `V1_FEATURES`.

## 2. Navigation (staff-only Intelligence)
- [`navConfig.ts`](contact360.io/app/src/lib/navConfig.ts): `requiresStaff` flag; Demands & Trends and Market Insights moved to staff-only **Intelligence** section.
- [`Sidebar.tsx`](contact360.io/app/src/components/layout/Sidebar.tsx): filters sections by `requiresStaff`.
- [`NavCommandPalette.tsx`](contact360.io/app/src/components/shared/NavCommandPalette.tsx): hides Intelligence section for Free/Pro.

## 3. Company filters
- [`HiringSignalsCompanyFilters.tsx`](contact360.io/app/src/components/feature/hiring-signals/HiringSignalsCompanyFilters.tsx):
  - **Industry** and **Employee size** live for all users (no more Coming Soon).
  - **Revenue** and **Funding** hidden entirely for Free/Pro (staff only).

## 4. Job filter sidebar
- [`HiringSignalsFilterSidebar.tsx`](contact360.io/app/src/components/feature/hiring-signals/HiringSignalsFilterSidebar.tsx): staff-only sections:
  - Remote / Workplace, Category (Topic), Education, Skills, Compliance, Compensation.
  - v1.0 sections (Title, Location, Date Posted, Experience, Job Type, LinkedIn Apply, Department) remain for everyone.

## 5. Export for all users (500 cap)
- [`HiringSignalsPageClient.tsx`](contact360.io/app/src/components/feature/hiring-signals/HiringSignalsPageClient.tsx): `canExportHireSignalXlsx = true`.
- [`hiringSignalService.ts`](contact360.io/app/src/services/graphql/hiringSignalService.ts): `HS_EXPORT_MAX_IDS_NON_STAFF = 500`.
- [`export_jobs.py`](contact360.io/api/app/graphql/modules/hire_signal/export_jobs.py): `MAX_EXPORT_LINKEDIN_JOB_IDS_NON_STAFF = 500`.

## 6. API enforcement
- [`queries.py`](contact360.io/api/app/graphql/modules/hire_signal/queries.py):
  - `_strip_extended_filters_for_non_staff()` strips v1.1+ filter fields for Free/Pro.
  - Applied in `hireSignal.jobs` and `hireSignal.jobFilterOptions`.
  - Blocks staff-only facet fields for non-staff users.

## 7. Owner role
- [`constants.py`](contact360.io/api/app/core/constants.py): `OWNER` added to `VALID_ROLES`.

---

**Resulting behavior**

| Role | Sees |
|------|------|
| **FreeUser / ProUser** | v1.0 filters, export (500 rows), saved searches, contacts — no Runs, no Intelligence nav, no v1.1+ filters |
| **Admin / SuperAdmin** | Full preview build (all filters, Runs, Intelligence nav, unlimited export) |

Use the acceptance checklist in the plan to verify as FreeUser, ProUser, and Admin.

