# Hire Signal — full-stack data pipeline

End-to-end reference for **scraper.server → MongoDB → job.server → GraphQL gateway → Next.js app**, including **field alignment**, **company logos**, and **Mongo company snapshots** as a Connectra fallback.

**Related (canonical contracts):**

- [HIRING-SIGNALS-FULL-CONTRACT.md](endpoints/job.server/HIRING-SIGNALS-FULL-CONTRACT.md) — REST ↔ GraphQL ↔ app routes and auth.
- [scraper-server-company-pipeline.md](scraper-server-company-pipeline.md) — Connectra batch-upsert and snapshot writes.
- [job.server-schema.md](database/job.server-schema.md) — Mongo collections used by job.server.

---

## 1. Scraper `JobResult` → job.server `LinkedInJob` (Mongo)

Apify-style ingest writes BSON keys that match [`LinkedInJob`](../../EC2/job.server/internal/models/linkedin_job.go). Scraper rows historically used **different names** on the same `linkedin_jobs` collection.

**Normalization:** `EC2/scraper.server/storage/mongo_store.py` runs `_normalize_job_doc_for_job_server()` inside `append_results()` **after** stripping heavy `company_*` keys and **before** upsert. That renames scraper fields so listing filters, sort on `posted_at`, and JSON tags align with Apify-ingested documents.

| Scraper / `JobResult` (Python) | job.server `LinkedInJob` BSON / JSON |
| ------------------------------ | ------------------------------------- |
| `job_title` | `title` |
| `linkedin_job_url` | `link` |
| `job_location` | `location` |
| `job_description` | `description_text` |
| `job_function` | `function_category_v2` |
| `industry` | `industries` |
| `num_applicants` | `applicants_count` (string) |
| `salary_range` | `salary` |
| `poster_profile_url` | `poster_linkedin_url` |
| `posted_at_timestamp` (unix sec) | `posted_at` (UTC datetime) |

Also set on upsert: `apify_run_id` → `""` when missing; `ingested_at` / `created_at` on `$setOnInsert`.

---

## 2. Company logo: Connectra `profile_pic` + UI

- Connectra **PgCompany** exposes the logo URL as **`profile_pic`**.
- Scraper batch-upsert (`EC2/scraper.server/scraper/enricher.py`) sends both **`logo`** (API compatibility) and **`profile_pic`** (same URL) when `company_logo` is present.
- The app normalizes display via **`pickCompanyDisplay`** (`profile_pic` · `logo` · `company_logo`) and shows an image in **Company drawer** and **Company contacts modal** when a URL is present.

---

## 3. Mongo `linkedin_company_snapshots` fallback (job.server)

Scraper.server upserts denormalized companies into Mongo (see `MONGO_COMPANIES_COLLECTION` / default collection name **`linkedin_company_snapshots`** in scraper config).

**job.server** `GET /api/v1/companies/:company_uuid/record` and `GET /api/v1/jobs/:linkedinJobId/company`:

1. Prefer **Connectra** when `CONNECTRA_BASE_URL` + `CONNECTRA_API_KEY` are set and the API succeeds.
2. If Connectra is missing, errors, or returns 404, optionally load the **Mongo snapshot** by `company_uuid` and return a Connectra-shaped JSON object (`uuid`, `name`, `website`, `linkedin_url`, `profile_pic` from snapshot `logo`, `employees_count`, `industries` from `industry`, etc.).
3. Successful snapshot responses may include top-level `"source": "mongo_company_snapshot"` for debugging.

**Environment (job.server):**

| Variable | Default | Purpose |
| -------- | ------- | ------- |
| `MONGO_LINKEDIN_COMPANY_SNAPSHOTS_COLLECTION` | `linkedin_company_snapshots` | Collection name (must match scraper when sharing one DB). |
| `ENABLE_MONGO_COMPANY_SNAPSHOT_FALLBACK` | `true` | Disable with `false` to force Connectra-only behavior. |

Contacts endpoints still require Connectra; snapshots do not include contact lists.

---

## 4. App row type `LinkedInJobRow` (mental model)

The UI hook maps job.server / GraphQL job payloads into **`LinkedInJobRow`** (see `useHiringSignals.ts`). Typical sources:

| UI (`LinkedInJobRow`) | job.server JSON (examples) |
| --------------------- | -------------------------- |
| `linkedinJobId` | `linkedinJobId` |
| `companyName` | `companyName` |
| `companyUuid` | `companyUuid` |
| `title` | `title` |
| `location` | `location` |
| `functionCategory` | `functionCategoryV2` (via display helpers) |
| `postedAt` | `postedAt` |
| `jobUrl` | `link` |

For the **full** GraphQL field → HTTP path matrix, use [HIRING-SIGNALS-FULL-CONTRACT.md](endpoints/job.server/HIRING-SIGNALS-FULL-CONTRACT.md).
