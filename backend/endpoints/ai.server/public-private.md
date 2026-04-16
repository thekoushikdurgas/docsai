# ai.server — public vs private routes (Era 8)

| Route | Public |
|-------|--------|
| `GET /health` | Yes |
| `GET /health/ready` | Yes (no API key) |
| All other routes | No — require `X-API-Key` when `AI_API_KEY` is set |

Last updated: 2026-04-15.
