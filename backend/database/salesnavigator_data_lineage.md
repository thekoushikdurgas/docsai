# Sales Navigator — Data Lineage

**Service:** `backend(dev)/salesnavigator`  
**Local persistence:** None — all data is forwarded to Connectra  
**Downstream stores:** Connectra PostgreSQL + Elasticsearch (`contacts`, `companies` indexes)

---

## Data Flow Overview

```
[SN Browser Extension]
        │
        │ Raw HTML or Profile Array
        ▼
[POST /v1/scrape or POST /v1/save-profiles]
        │
        │ Parsed / Validated Profiles
        ▼
[SaveService — Deduplicate + Chunk + Map]
        │
        ├──[POST /companies/bulk] ──► Connectra (PostgreSQL + Elasticsearch companies)
        │
        └──[POST /contacts/bulk]  ──► Connectra (PostgreSQL + Elasticsearch contacts)
```

---

## Input data — Sales Navigator profile fields

| Field | Source | Presence |
| --- | --- | --- |
| `name` | SN lead card | Required for mapping |
| `title` | SN lead card | Optional |
| `company` | SN lead card | Optional |
| `location` | SN lead card | Optional |
| `profile_url` | SN lead card anchor | Required (dedup key) |
| `company_url` | SN company anchor | Optional |
| `connection_degree` | SN relationship badge | Optional |
| `email` | SN enriched data | Optional (often absent) |
| `mobile_phone` | SN enriched data | Optional |
| `email_status` | SN enriched data | Optional |
| `about` | SN profile blurb | Optional |
| `is_premium` | SN premium icon | Optional |
| `mutual_connections_count` | SN connection info | Optional |
| `recently_hired` | SN signal | Optional |

---

## UUID generation strategy (deterministic, idempotent)

### Contact UUID

```
uuid5(NAMESPACE_URL, linkedin_url + email)
```

- `linkedin_url` derived from SN URL via `convert_sales_nav_url_to_linkedin()`
- When SN URL cannot be converted → uses `PLACEHOLDER_VALUE` sentinel
- `email` may be empty string — still used in UUID seed

### Company UUID

```
uuid5(NAMESPACE_URL, company_name_normalized + company_url)
```

- `company_name_normalized` — lowercase, whitespace collapsed
- `company_url` — SN company URL (`linkedin.com/sales/company/...`)

> **Risk:** If SN URL conversion fails (PLACEHOLDER sentinel), UUID will differ from organic LinkedIn contact for the same person. Dedup against existing contacts is degraded. Era `4.x` should track this as enrichment debt.

---

## Contact fields written to Connectra

| Connectra field | Source field / derivation |
| --- | --- |
| `uuid` | Deterministic UUID5 (see above) |
| `first_name` | Parsed from `name` (first token) |
| `last_name` | Parsed from `name` (last token; multi-word → last) |
| `title` | Normalized `title` |
| `seniority` | Inferred: executive/director/manager/senior_ic/entry |
| `departments` | Extracted keywords from `title` + `about` |
| `city` | First comma-segment of `location` |
| `state` | Second comma-segment of `location` |
| `country` | Third comma-segment of `location` |
| `text_search` | `location` raw |
| `email` | Direct from profile (may be absent) |
| `email_status` | Direct from profile (may be absent) |
| `mobile_phone` | Direct from profile (may be absent) |
| `linkedin_url` | Converted from SN URL (may be PLACEHOLDER) |
| `linkedin_sales_url` | `profile_url` from SN |
| `company_id` | Company UUID (deterministic) |
| `source` | `"sales_navigator"` |
| `connection_degree` | From SN badge |
| `data_quality_score` | Computed completeness metric |
| `lead_id` | Extracted from SN URL URN |
| `search_id` | Extracted from SN URL context |

---

## Company fields written to Connectra

| Connectra field | Source field / derivation |
| --- | --- |
| `uuid` | Deterministic UUID5 |
| `name` | `company` field from profile; normalized |
| `text_search` | `company` raw |
| `linkedin_url` | `company_url` (SN format) |
| `linkedin_sales_url` | `company_url` (SN format) |
| `technologies` | Regex-extracted from `about` field (tech keywords) |
| `employees_count` | **Always null** — not available from SN lead cards |
| `industries` | **Always null** — not available from SN lead cards |
| `annual_revenue` | **Always null** — not available from SN lead cards |

---

## Data quality scoring

| Dimension | Weight | Fields checked |
| --- | --- | --- |
| Required fields (name, title, company, profile_url) | 70% | 4 fields |
| Optional fields enrichment | 30% | email, phone, location, about, company_url |
| **Score** | 0–100 | Composite |

- Score is stored as `data_quality_score` on the Connectra contact record.
- Score < 30: flagged as `low_quality` — may be excluded from AI context.

---

## Deduplication

1. Normalize `profile_url` (strip trailing slashes, lowercase).
2. Group profiles by normalized URL.
3. Within group: compute completeness score for each duplicate.
4. Retain the highest-scoring profile; merge optional arrays (skills, etc.) from others.
5. Resulting deduplicated list is chunked into batches of 500 and sent to Connectra.

---

## Chunking and parallelism

| Parameter | Value |
| --- | --- |
| Chunk size | 500 profiles |
| Max parallel chunks | 3 |
| Timeout base | 30s |
| Timeout per additional profile (>20) | +100ms/profile |
| Timeout cap | 300s |

---

## Era-by-era data lineage evolution

| Era | Data change |
| --- | --- |
| `0.x` | UUID generation contract defined; no active ingest |
| `1.x` | `actor_id`/`org_id` injected into contact records for audit |
| `2.x` | `email`, `email_status` field handling validated; enrichment queue stub |
| `3.x` | Full field mapping locked; provenance fields (`source`, `lead_id`, `search_id`) added |
| `4.x` | `data_quality_score` surfaced; `connection_degree` and `recently_hired` added; backend ingestion complete through `4.2` while extension shell delivery continues in `4.5+` |
| `5.x` | `seniority`, `departments`, `about` quality gated for AI context |
| `6.x` | Chunk idempotency tokens; replay-safe ingest; partial success tracking |
| `7.x` | Immutable audit event per save session; GDPR erasure cascade |
| `8.x` | Usage counters per key; `api_usage` table tracking ingest volume |
| `9.x` | Partner connector adapter fields; webhook delivery metadata |
| `10.x` | Campaign provenance: `lead_id`/`search_id` carried to campaign audience records |

---

## Table/index ownership summary

| Store | Owner | SN writes via |
| --- | --- | --- |
| `contacts` (Elasticsearch) | Connectra | `POST /contacts/bulk` |
| `contacts` (PostgreSQL) | Connectra | `POST /contacts/bulk` |
| `companies` (Elasticsearch) | Connectra | `POST /companies/bulk` |
| `companies` (PostgreSQL) | Connectra | `POST /companies/bulk` |
| None locally | Sales Navigator service | — |

---

## Cross-references

- Codebase analysis: `docs/codebases/salesnavigator-codebase-analysis.md`
- API era matrix: `docs/backend/endpoints/salesnavigator_endpoint_era_matrix.json`
- GraphQL module: `docs/backend/apis/23_SALES_NAVIGATOR_MODULE.md`
- UI bindings: `docs/frontend/docs/salesnavigator-ui-bindings.md`
- Era task packs: `docs/backend/apis/SALESNAVIGATOR_ERA_TASK_PACKS.md`
