# extension.server — gateway route matrix (Era 3)

| extension.server route | Gateway client | Method on client | Notes |
|------------------------|----------------|------------------|-------|
| `GET /health` | (ops / probes) | — | No API key |
| `POST /v1/save-profiles` | `SalesNavigatorServerClient` | `save_profiles` | `profiles` array |
| `POST /v1/scrape` | `SalesNavigatorServerClient` | `scrape_html` | `html`, `include_metadata`, `save` |

| sync.server route | Caller | Notes |
|-------------------|--------|-------|
| `POST /internal/extension/upsert-bulk` | extension `connectra.Client` | `{ contacts, companies }` DTO |

Last updated: 2026-04-15.
