# scraper.server — company snapshot + Connectra upsert

**Code:** `EC2/scraper.server`  
**Last reviewed:** 2026-05-23

## Purpose

Each scraped job batch:

1. Optionally enriches company websites (Connectra lookup + OpenAI fallback).
2. **Normalizes** `company_linkedin_url` using the same cleaning rules as **job.server** / Connectra UUID derivation (`scraper/enricher.py`).
3. **Upserts** employers to **Connectra** (`batch-upsert`) and assigns **`company_uuid`** on each raw row (API response UUID when returned; otherwise deterministic UUID5 from cleaned URL). Payloads send **`logo`** and **`profile_pic`** (same URL) when `company_logo` is known so Connectra can populate **`profile_pic`** on `PgCompany`.
4. **Upserts** denormalized company fields into OpenSearch index **`OPENSEARCH_COMPANIES_INDEX`** (default `linkedin_companies`), keyed by **`company_uuid`**.
5. Builds **`JobResult`** and persists slim job rows to **`OPENSEARCH_JOBS_INDEX`** (default `linkedin_jobs`) via `append_results`, which strips heavy company blob keys.

Canonical employer identity for the product remains **Connectra**; OpenSearch company docs are a **cache/denormalized store** for ops and faster local joins.

## Per-batch invariants

| Step | Invariant |
| ---- | --------- |
| After URL normalize | Non-empty `company_linkedin_url` is cleaned (query stripped, `/company/{slug}` trimmed). |
| After Connectra apply | Every row with a non-empty LinkedIn company URL has a **`company_uuid`** (deterministic fallback if API returns no mapping). |
| OpenSearch company doc | One upsert per distinct `company_uuid` in the batch; `linkedin_url` uses **normalized** form. |
| OpenSearch job doc | `linkedin_jobs` documents keep **`company_name`** + **`company_uuid`**; heavy company keys stripped before index (see `scrape_job_store`). Field aliases applied in `append_results` for job.server compatibility. |

## Observability

On each flush, the worker logs one line:

`[{job_id}] flush_company_metrics ...`

Fields include batch size, Connectra payload counts, UUID assignment breakdown, HTTP status, and company snapshot write count or **`company_snapshot_err=...`** if snapshot writes fail (job rows still append if `append_results` runs afterward).

## Env

| Variable | Default | Role |
| -------- | ------- | ---- |
| `OPENSEARCH_COMPANIES_INDEX` | `linkedin_companies` | Company snapshot index |
| `OPENSEARCH_JOBS_INDEX` | `linkedin_jobs` | Scraped job postings |
| `OPENSEARCH_SCRAPE_JOBS_INDEX` | `scrape_data_index` | Scrape session metadata |
| `CONNECTRA_API_URL` / `CONNECTRA_API_KEY` | see `config.py` | Batch-upsert + lookup |

## See also

- [hire-signal-data-pipeline.md](hire-signal-data-pipeline.md) — full-stack Hire Signal flow, scraper→job.server field mapping.
- [resume-ai-scraper.md](resume-ai-scraper.md) — Resume Matcher on OpenSearch.
