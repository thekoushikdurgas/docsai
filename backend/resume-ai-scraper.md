# Résumé Matcher on scraper.server (`/resume/v1`)

The LinkedIn scraper FastAPI app (`EC2/scraper.server`) mounts the Resume Matcher-style API under **`/resume/v1`**:

- **`/resume/v1/resumes/*`** — upload PDF/DOCX, list, fetch, tailor (preview/confirm), PDF export, master promotion, keyword score.
- **`/resume/v1/jobs/*`** — store job description text for tailoring.
- **`/resume/v1/enrichment/*`** — AI analyze / enhance flows (ported from Resume Matcher).
- **`/resume/v1/health`** — OpenSearch resume index stats + LLM health ping.

Data is stored in **OpenSearch** (same cluster as the scraper), in indices:

- `resume_docs` (override with `OPENSEARCH_RESUME_DOCS_INDEX`)
- `resume_jobs` (`OPENSEARCH_RESUME_JOBS_INDEX`)
- `resume_improvements` (`OPENSEARCH_RESUME_IMPROVEMENTS_INDEX`)

Configure LLM access via `OPENAI_API_KEY` or `RESUME_LLM_*` env vars (see `resume/resume_settings.py`). PDF export uses **server-rendered HTML** + Playwright (no Next.js print route required).

**contact360.io/app** calls **`/resume/v1`** on **contact360.io/api** (gateway reverse-proxy with JWT). The gateway forwards to **`SCRAPER_SERVER_API_URL`** and injects **`SCRAPER_SERVER_API_KEY`** when set. **`GET /resume/v1/health`** is public at the gateway (no bearer token).

For local debugging directly against scraper.server, set **`NEXT_PUBLIC_RESUME_AI_URL`** in the app (JWT is only enforced when traffic goes through the API gateway).

### Migrating legacy Mongo resume data

If you previously stored resume rows in MongoDB, run once:

```bash
pip install pymongo
python scripts/migrate_resume_mongo_to_opensearch.py
```

Set `MONGO_URI`, `MONGO_DB_NAME`, and collection names via env (see script header). OpenSearch connection uses standard `OPENSEARCH_*` vars.
