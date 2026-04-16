# extension.server — pipeline (Era 4)

## save-profiles

1. **`POST /v1/save-profiles`** receives `{ "profiles": [ ... raw JSON ... ] }`.
2. **`saveflex.ParseProfilesJSON`** normalizes rows into compact profiles.
3. **Dedupe** by normalized email / id ([`dedupeProfiles`](../../../../EC2/extension.server/internal/api/router.go)).
4. **Chunk** size **500** per Connectra request.
5. **In-process worker pool** submits each chunk: builds `contacts` + `companies` arrays, **`POST /internal/extension/upsert-bulk`** on Connectra.
6. Any chunk error → **502** with aggregated error strings.

## scrape

1. **`POST /v1/scrape`** receives `{ "html", "include_metadata", "save" }`.
2. **`scrapesn.ParseSearchHTML`** extracts profile maps + page metadata.
3. If **`save`** and profiles exist: map to compact profiles → same dedupe + single bulk payload as above (no chunking split beyond one bulk call for that request’s uniq set).

## Connectra side

[`UpsertBulk`](../../../../EC2/sync.server/modules/extension/controller.go) upserts **companies** first (name + domain → stable internal `linkedin_url`), then **contacts** via **`ContactService.BulkContacts`** → **`UpsertContact`** (email and/or **`linkedin_url`** identity).

Last updated: 2026-04-15.
