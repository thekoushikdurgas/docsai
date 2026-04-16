# extension.server — public vs private routes (Era 8)

| Route | Public | Auth |
|-------|--------|------|
| `GET /health` | Yes | None |
| `POST /v1/save-profiles` | No | `X-API-Key` or `api_key` when `EXTENSION_API_KEY` set |
| `POST /v1/scrape` | No | Same |

Last updated: 2026-04-15.
