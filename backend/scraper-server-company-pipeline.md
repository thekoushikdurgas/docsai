# scraper.server — company snapshot + Connectra upsert

**Code:** `EC2/scraper.server`  
**Last reviewed:** 2026-05-07

## Purpose

Each scraped job batch:

1. Optionally enriches company websites (Connectra lookup + OpenAI fallback).
2. **Normalizes** `company_linkedin_url` using the same cleaning rules as **job.server** / Connectra UUID derivation (`scraper/enricher.py`).
3. **Upserts** employers to **Connectra** (`batch-upsert`) and assigns **`company_uuid`** on each raw row (API response UUID when returned; otherwise deterministic UUID5 from cleaned URL). Payloads send **`logo`** and **`profile_pic`** (same URL) when `company_logo` is known so Connectra can populate **`profile_pic`** on `PgCompany`.
4. **Upserts** denormalized company fields into MongoDB collection **`MONGO_COMPANIES_COLLECTION`** (default `linkedin_company_snapshots`), keyed by **`company_uuid`**.
5. Builds **`JobResult`** (drops unknown/extra keys) and persists slim job rows to **`MONGO_RAW_JOBS_COLLECTION`** (`linkedin_jobs`) via `append_results`, which strips heavy company blob keys.

Canonical employer identity for the product remains **Connectra**; Mongo snapshots are a **cache/denormalized store** for ops and faster local joins.

## Per-batch invariants

| Step | Invariant |
| ---- | --------- |
| After URL normalize | Non-empty `company_linkedin_url` is cleaned (query stripped, `/company/{slug}` trimmed). |
| After Connectra apply | Every row with a non-empty LinkedIn company URL has a **`company_uuid`** (deterministic fallback if API returns no mapping). |
| Mongo company snapshot | One upsert per distinct `company_uuid` in the batch; `linkedin_url` in the snapshot uses **normalized** form. |
| Mongo job row | `linkedin_jobs` documents keep **`company_name`** + **`company_uuid`**; stripped keys listed in `mongo_store._COMPANY_STRIP_KEYS`. Scraper **`JobResult`** keys are renamed to **`LinkedInJob`** BSON names in `append_results` (see [hire-signal-data-pipeline.md](hire-signal-data-pipeline.md)). |

## Observability

On each flush, the worker logs one line:

`[{job_id}] flush_company_metrics ...`

Fields include batch size, Connectra payload counts, UUID assignment breakdown, HTTP status, and Mongo snapshot write count or **`mongo_err=...`** if snapshot writes fail (job rows still append if `append_results` runs afterward).

## Env

| Variable | Default | Role |
| -------- | ------- | ---- |
| `MONGO_COMPANIES_COLLECTION` | `linkedin_company_snapshots` | Company snapshot collection |
| `CONNECTRA_API_URL` / `CONNECTRA_API_KEY` | see `config.py` | Batch-upsert + lookup |

## See also

- [hire-signal-data-pipeline.md](hire-signal-data-pipeline.md) — full-stack Hire Signal flow, scraper→job.server field mapping, snapshot fallback on job.server.
- [VERIFICATION-HIRING-SIGNALS.md](VERIFICATION-HIRING-SIGNALS.md) — Mongo spot-checks after deploy
