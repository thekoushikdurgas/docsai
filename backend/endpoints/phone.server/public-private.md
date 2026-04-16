# phone.server — public vs private routes

## Public (no `X-API-Key`)

| Method | Path |
|--------|------|
| GET | `/health` |
| GET | `/` |

## Private (`X-API-Key`)

| Prefix | Purpose |
|--------|---------|
| `/jobs` | List, status, pause, resume, terminate |
| `/phone` | Finder, verifier, S3 jobs |
| `/web` | `POST /web/web-search` |
| `/phone-patterns` | Pattern add / predict |

Optional: **`X-Request-ID`** echoed on responses.
