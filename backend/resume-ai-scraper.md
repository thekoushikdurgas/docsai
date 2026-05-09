# Résumé Matcher on scraper.server (`/resume/v1`)

The LinkedIn scraper FastAPI app (`EC2/scraper.server`) mounts the Resume Matcher-style API under **`/resume/v1`**:

- **`/resume/v1/resumes/*`** — upload PDF/DOCX, list, fetch, tailor (preview/confirm), PDF export, master promotion, keyword score.
- **`/resume/v1/jobs/*`** — store job description text for tailoring.
- **`/resume/v1/enrichment/*`** — AI analyze / enhance flows (ported from Resume Matcher).
- **`/resume/v1/health`** — Mongo stats + LLM health ping.

Data is stored in the **same MongoDB** as the scraper (`MONGO_DB_NAME`), in collections:

- `resume_docs` (default; override with `RESUME_MONGO_DOCS_COLLECTION`)
- `resume_jobs` (`RESUME_MONGO_JOBS_COLLECTION`)
- `resume_improvements` (`RESUME_MONGO_IMPROVEMENTS_COLLECTION`)

Configure LLM access via `OPENAI_API_KEY` or `RESUME_LLM_*` env vars (see `resume/resume_settings.py`). PDF export uses **server-rendered HTML** + Playwright (no Next.js print route required).

**contact360.io/app** calls **`/resume/v1`** on **contact360.io/api** (gateway reverse-proxy with JWT). The gateway forwards to **`SCRAPER_SERVER_API_URL`** and injects **`SCRAPER_SERVER_API_KEY`** when set. **`GET /resume/v1/health`** is public at the gateway (no bearer token).

For local debugging directly against scraper.server, set **`NEXT_PUBLIC_RESUME_AI_URL`** in the app (JWT is only enforced when traffic goes through the API gateway).
