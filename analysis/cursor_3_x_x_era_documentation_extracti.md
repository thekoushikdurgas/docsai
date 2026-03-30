# 3.x.x era documentation extraction
_Exported on 3/25/2026 at 14:29:19 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read these files and return sections relevant to the 3.x.x era (contact/company data, Connectra, VQL, enrichment, dedup, search, Sales Navigator, export):
1. d:\code\ayan\contact\docs\roadmap.md - find VERSION 3.x section, stage names, status, KPIs, code pointers
2. d:\code\ayan\contact\docs\versions.md - find 3.x entries
3. d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md - return sections: era mapping, immediate execution queue, gaps/risks
4. d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md - return sections: era mapping, 3.x rows, gaps/risks

Return only the relevant sections.

---

**Cursor**


Reading the four files and extracting sections relevant to the 3.x.x era.




Here are the excerpts that matter for **3.x** (contact/company data, Connectra, VQL, enrichment, dedup, search, Sales Navigator tie-ins, export), pulled from the paths you named.

---

## 1. `d:\code\ayan\contact\docs\roadmap.md` — VERSION 3.x + related pointers

**VERSION 3.x — Contact and Company Data System** (stages 3.1–3.4: names, status, depends, risk, DoD, KPI, ships in). Note: unlike some earlier stages, these blocks do **not** list explicit **code pointers** lines.

```211:254:d:\code\ayan\contact\docs\roadmap.md
## VERSION 3.x — Contact and Company Data System

### Stage 3.1 - Advanced search filters (VQL)

**Status:** Planned  
**Depends on:** Connectra index quality and VQL parser support  
**Risk:** Filter complexity causing query performance regressions  
**Definition of done:** Advanced contacts/companies filters are available and stable  
**KPI:** Filter query success and latency percentiles  
**Ships in:** `3.0.0`

---

### Stage 3.2 - Enrichment and deduplication

**Status:** Planned  
**Depends on:** Stage 3.1  
**Risk:** Duplicate profiles and confidence mismatch in enrichment  
**Definition of done:** Enrichment quality improves with dedupe controls  
**KPI:** Duplicate reduction rate, enrichment completeness  
**Ships in:** `3.0.0`

---

### Stage 3.3 - Search quality and performance

**Status:** Planned  
**Depends on:** Stages 3.1, 3.2  
**Risk:** Index refresh and relevance tuning instability  
**Definition of done:** Relevance and latency SLO targets are met  
**KPI:** Search precision proxy score and P95 response time  
**Ships in:** `3.0.0`

---

### Stage 3.4 - Dashboard search UX expansion

**Status:** Planned  
**Depends on:** Stages 3.1, 3.3  
**Risk:** UI complexity reducing discoverability  
**Definition of done:** Advanced filtering flows are available in dashboard UX  
**KPI:** Filter usage rate and successful search-to-export conversions  
**Ships in:** `3.0.0`
```

**Feature-to-service traceability** (3.x row — Connectra, gateway, stores, export relevance):

```836:836:d:\code\ayan\contact\docs\roadmap.md
| 3.1–3.4 | Contact/company data | `connectra`, `appointment360` | `dashboard` | Elasticsearch, PostgreSQL | `3.0.0` |
```

**Deep execution — 3.x slice** (VQL, enrichment/dedup, search, UX, export tracking):

```879:896:d:\code\ayan\contact\docs\roadmap.md
### `3.x` → `4.x` (Contact/company data → Extension)

- **3.1 VQL/filters**
  - Freeze filter taxonomy and validate VQL-to-ES query translation.
  - Add performance regression tests for complex filter queries.
- **3.2 Enrichment/dedupe**
  - Tune merge-on-conflict rules and deterministic UUID assignment.
  - Add deduplication quality metrics to observability.
- **3.3 Search quality**
  - Tune index refresh cycle and relevance scoring.
  - Validate P95 latency targets against SLO.
- **3.4 Search UX**
  - Build advanced filter UI with saved-search capability.
  - Add company drill-down and search-to-export conversion tracking.
- **4.1–4.4 Extension**
  - Harden token refresh and session expiry handling in extension context.
  - Validate SN ingestion pipeline with dedup and conflict resolution.
  - Add telemetry error shipping to logs.api and ingestion status UX.
```

**Cross-service callouts** (3.x lines for `s3storage`, `logs.api`, `jobs`, `contact.ai`, `salesnavigator`):

```1008:1011:d:\code\ayan\contact\docs\roadmap.md
### `3.x` contact/company data
- Contract: ingestion artifact naming/versioning.
- Service: robust schema/stats/preview behavior for large CSVs.
- Data/Ops: upload-to-ingestion lineage evidence.
```

```1066:1066:d:\code\ayan\contact\docs\roadmap.md
- `3.x`: data-enrichment/search support diagnostics.
```

```1082:1082:d:\code\ayan\contact\docs\roadmap.md
- `3.x`: Contact360 import/export stream processors + VQL validation.
```

```1110:1110:d:\code\ayan\contact\docs\roadmap.md
- `3.x`: `parseContactFilters` + `generateCompanySummary` aligned with Connectra VQL taxonomy.
```

```1138:1138:d:\code\ayan\contact\docs\roadmap.md
- `3.x`: Full `mappers.py` locked; provenance fields (`source=sales_navigator`, `lead_id`, `search_id`, `connection_degree`) written to Connectra.
```

---

## 2. `d:\code\ayan\contact\docs\versions.md` — 3.x release index + entries

**Release index row:**

```30:30:d:\code\ayan\contact\docs\versions.md
| `3.0.0` | planned | TBD | Contact and company data system era |
```

**Release entries `3.0.0`–`3.4.0`:**

```149:192:d:\code\ayan\contact\docs\versions.md
### `3.0.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Contact and company data system era — Connectra intelligence expansion.
- **Scope:** VQL filters, enrichment quality, deduplication, and advanced search UX.
- **Roadmap mapping:** `3.1` to `3.4`
- **Owner:** Search/Data Engineering

### `3.1.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Advanced search filters and VQL.
- **Scope:** VQL parser maturity, advanced contacts/companies filter taxonomy.
- **Roadmap mapping:** `3.1`
- **Owner:** Connectra Engineering

### `3.2.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Enrichment and deduplication.
- **Scope:** Duplicate profile reduction and enrichment completeness improvements.
- **Roadmap mapping:** `3.2`
- **Owner:** Data Engineering

### `3.3.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Search quality and performance.
- **Scope:** Index refresh stability, relevance tuning, and latency SLO.
- **Roadmap mapping:** `3.3`
- **Owner:** Connectra Engineering

### `3.4.0`

- **Status:** planned
- **Target window:** TBD
- **Summary:** Dashboard search UX expansion.
- **Scope:** Advanced filtering UX and search-to-export conversion flows.
- **Roadmap mapping:** `3.4`
- **Owner:** Dashboard + Search
```

**`3.x` task-pack pattern** (VQL, Connectra, dedupe, search UX, export-adjacent):

```727:732:d:\code\ayan\contact\docs\versions.md
### `3.x` task-pack pattern (contact/company data)

- Contract: VQL filter taxonomy and search schema changes.
- Service: Connectra VQL, dual-write logic, enrichment pipeline, and dedupe algorithm updates.
- Surface: advanced filter UX, company drill-down, and saved-search feature updates.
- Data/Ops: index refresh reliability, search relevance checks, and deduplication quality metrics.
```

**Connectra execution spine — 3.x row:**

```869:869:d:\code\ayan\contact\docs\versions.md
| 3.x | VQL freeze, filter taxonomy, dual-write PG+ES, enrichment/dedup | Contact/company search core |
```

---

## 3. `d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md` — era mapping, immediate queue, gaps/risks

**Gaps and risks:**

```66:71:d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md
## Gaps and risks

- Single in-memory queue can lose pending work on abrupt process crash.
- API key and rate-limit policy need stricter rotation and tenant partitioning.
- `AllowAllOrigins` CORS posture is too broad for hardened environments.
- ES/PG drift detection and reconciliation automation are not first-class.
```

**Era mapping** (`3.x` row highlighted):

```73:87:d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md
## Era mapping (`0.x`-`10.x`)

| Era | Connectra concern | Small-task decomposition |
| --- | --- | --- |
| `0.x` | Service bootstrap | API key baseline, index bootstrap scripts, health checks |
| `1.x` | Credit-aware usage | Search/export volume guards and billing event alignment |
| `2.x` | Bulk email pipeline | CSV contract stability, column mapping, stream import/export |
| `3.x` | Core data system | VQL freeze, filter taxonomy, dual-write and dedup integrity |
| `4.x` | Extension/SN ingest | Provenance fields and idempotent sync from SN sources |
| `5.x` | AI workflows | AI-readable attributes and enrichment artifact lookup paths |
| `6.x` | Reliability/scaling | Query P95 SLO, job success SLI, retry/DLQ hardening |
| `7.x` | Deployment governance | RBAC on write/export, audit evidence, tenant isolation |
| `8.x` | Public/private APIs | Versioned REST contracts, partner keys, webhook-ready job events |
| `9.x` | Productization | Quota-aware throttling and connector-safe filter contracts |
| `10.x` | Campaign runtime | Audience query stability, suppression filter compliance, export controls |
```

**Immediate execution queue:**

```89:95:d:\code\ayan\contact\docs\codebases\connectra-codebase-analysis.md
## Immediate execution queue

1. Add persistent queue backing for job durability.
2. Add ES-PG reconciliation job and drift diagnostics.
3. Add per-tenant rate limiting and API key scope model.
4. Add contract-parity tests for VQL operators and filter metadata.
5. Add release gates for batch-upsert idempotency evidence.
```

---

## 4. `d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md` — era mapping, 3.x block, gaps/risks

**Era relevance** (positions SN vs 3.x):

```3:7:d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md
**Service path:** `backend(dev)/salesnavigator/`  
**Runtime:** FastAPI on AWS Lambda (via Mangum adapter)  
**Language:** Python 3.11  
**Era relevance:** `4.x` (primary) — with influence from `0.x` setup through `10.x` campaign audience  
**Era task-pack index:** `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
```

**3.x era row** (Contact/Company Data — mapper, Connectra/VQL alignment, dedup, ops):

```296:301:d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md
### 3.x — Contact/Company Data
**Contract:** Strict schema alignment with Connectra contact/company VQL contract.  
**Service:** Improve mapper coverage: seniority inference, departments extraction, company metadata.  
**Surface:** Sync result table with created/updated split; company row enrichment.  
**Data:** Dedup/idempotency evidence per `profile_url`/UUID; reconciliation report.  
**Ops:** Connectra parity checks: input profiles vs. created+updated total.
```

**Gaps and risks** (full table; several fixes land in 4.x–6.x but affect ingest/search/dedup quality):

```237:251:d:\code\ayan\contact\docs\codebases\salesnavigator-codebase-analysis.md
## 8. Known gaps and risks

| Gap | Risk | Era fix |
| --- | --- | --- |
| `POST /v1/scrape-html-with-fetch` documented but not implemented | Client misconfiguration | `4.x` immediate fix or remove from docs |
| `POST /v1/scrape` active but README says scraping removed | Maintenance confusion | `4.x` fix docs/README |
| Single global `API_KEY` — no tenant/user scoping | No per-user audit trail | `7.x`–`8.x` |
| No rate limiting | Abuse risk for large SN exports | `6.x` |
| Wide-open CORS (`*`) | Risk if endpoint becomes internet-accessible | `6.x` |
| No request-ID/correlation header | Blind spots in distributed tracing | `6.x` |
| SN URL → standard LinkedIn URL conversion always returns PLACEHOLDER | Contact dedup quality risk | `4.x` |
| `employees_count`, `industries` null for all SN contacts | Enrichment gap | `5.x`–`9.x` |
| `extraction.py` kept but not in active production path | Dead code accumulation | `4.x` cleanup |
| Connectra coupling: no local DB | Full availability depends on Connectra | `6.x` retry budget |
| No chunk-level idempotency token | Duplicate saves on Lambda retry | `6.x` |
```

---

**Note:** In `roadmap.md`, **VERSION 3.x** stages do not include per-stage **code pointers** bullets; the closest “code-level” anchors are the **traceability matrix** row for `3.1–3.4` (`connectra`, `appointment360`, Elasticsearch, PostgreSQL) and the **deep execution** bullets for VQL, dedupe, and search-to-export.

