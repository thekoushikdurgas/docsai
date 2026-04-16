# ai.server — health and reliability (Era 6)

- **`GET /health`** — always 200 if process up.
- **`GET /health/ready`** — 503 if `HF_API_KEY` missing; 503 if `DATABASE_URL` set and DB ping fails.
- **HF client:** retries across fallback models on 5xx/429-style errors.
- **Satellite:** HTTP calls fail fast; enrich endpoints return 502 on Connectra errors.

Last updated: 2026-04-15.
