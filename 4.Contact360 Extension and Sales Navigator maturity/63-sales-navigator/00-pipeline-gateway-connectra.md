# Sales Navigator — pipeline (capture → gateway → extension.server → Connectra)

**Owner:** extension · **Last reviewed:** 2026-04-19  
**Order:** matches [`docs/PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md) item 8 and [`docs/DECISIONS.md`](../../DECISIONS.md) § Sales Navigator / extension satellite.

## 1. Capture (browser)

- MV3 **content script** extracts profile/company **links** (default) or optional **HTML** scrape on SN pages (feature-flagged).
- **Service worker** holds JWT; calls **only** the gateway **`POST /graphql`** — not extension.server directly.

## 2. Gateway (`contact360.io/api`)

- Mutations: **`saveSalesNavigatorProfiles`**, **`scrapeSalesNavigatorHtml`** (names per current schema — see [`GRAPHQL-SCHEMA.md`](../../../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md)).
- Resolves org + user; forwards to **`SalesNavigatorServerClient`** with **`SALES_NAVIGATOR_SERVER_API_URL`** / **`SALES_NAVIGATOR_SERVER_API_KEY`**.

## 3. extension.server

- **`POST /v1/save-profiles`** — maps payloads → Connectra batch upserts (companies first, then contacts), chunked.
- **`POST /v1/scrape`** — optional HTML parse path; when `save: true`, same persistence rules.
- **`GET /health`** included in GraphQL **`health.satelliteHealth`** as **sales_navigator**.

## 4. Connectra (sync.server)

- **`POST /companies/batch-upsert`** then **`POST /contacts/batch-upsert`** — response **`company_uuids`** / **`contact_uuids`** in request order.
- Optional **`hydrate=0`** to skip large hydrate payloads.

## Preview merge (`chrome.storage`)

- Persist lightweight preview under key **`c360_last_capture_preview`** (see [`frontend/extension/eras/era-04-scrape-preview.md`](../../frontend/extension/eras/era-04-scrape-preview.md)).
- Merge server truth from GraphQL **`SaveProfilesResponse`**: **`contactUuids`**, **`companyUuids`**, **`savedContacts`**, **`savedCompanies`**.

## SSE sidebar

- Subscribe to gateway/extension **SSE** channel for enrichment job completion (see [`DECISIONS.md`](../../DECISIONS.md) § SSE vs WebSocket).

## Related

- Flowchart: [`docs/flowchart/extension-capture.md`](../../flowchart/extension-capture.md)
- Flow 5: [`docs/0.Foundation and pre-product stabilization and codebase setup/flows/FLOW-5-extension-enrich.md`](../../0.Foundation%20and%20pre-product%20stabilization%20and%20codebase%20setup/flows/FLOW-5-extension-enrich.md)
- Preview UX: [`docs/frontend/extension/eras/era-04-scrape-preview.md`](../../frontend/extension/eras/era-04-scrape-preview.md)
