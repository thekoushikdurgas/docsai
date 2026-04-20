# extension.server — pipeline (Era 4)

## save-profiles

1. **`POST /v1/save-profiles`** receives `{ "profiles": [ ... raw JSON ... ] }`.
2. **`saveflex.ParseProfilesJSON`** normalizes rows into compact profiles.
3. **Dedupe** by normalized email / id ([`dedupeProfiles`](../../../../EC2/extension.server/internal/api/router.go)).
4. **Chunk** size **500** per worker item; **in-process worker pool** processes chunks.
5. Each chunk: **`syncbatch.BuildCompanyMaps`** → **`POST /companies/batch-upsert`** (chunks of 100); then **`syncbatch.BuildContactMaps`** → **`POST /contacts/batch-upsert`** (chunks of 100).
6. Responses are parsed with **`ParseUpsertBatchResponseWithFallback`**: if Connectra returns only `{ "success": true }`, UUIDs are taken from the maps sent in the request body (same order).
7. Optional **hydration** (`hydrate=1` default): **`POST /contacts/`** and **`POST /companies/`** VQL with `keyword_match.must.uuid` lists.
8. **Response** includes `contact_uuids`, `company_uuids`, and optional `contacts` / `companies` arrays (capped).

## scrape

1. **`POST /v1/scrape`** receives `{ "html", "include_metadata", "save" }`.
2. **`scrapesn.ParseSearchHTML`** extracts profile maps + page metadata.
3. If **`save`** and profiles exist: map to compact profiles → **`upsertConnectraBatch`** (same companies-first, contacts-second batch-upsert as above).

## Connectra side

Batch upserts are handled by **`modules/companies/controller`** and **`modules/contacts/controller`** **`BatchUpsert`** handlers: PostgreSQL + OpenSearch, **HTTP 500** on **`BulkUpsert`** error, **HTTP 200** with **`company_uuids`** / **`contact_uuids`** echoing input order on success.

Last updated: 2026-04-20.
