# Observability baseline

**Owner:** platform · **Last reviewed:** 2026-04-19  
**Anchor:** [`DECISIONS.md`](DECISIONS.md) — gateway middleware stack.

## Request correlation

- **`X-Request-ID`** — generated or forwarded on the **gateway** (`contact360.io/api`); propagated to satellite HTTP clients where supported. Satellites echo on responses per service `DECISIONS.md` entries.
- Logs should include `request_id` / trace id in gateway and workers.

## Gateway

- **Middleware (order):** CORS → TrustedHost → ProxyHeaders → GraphQL rate limit → mutation abuse guard → idempotency → body size → trace/request IDs → timing → **RED metrics** → GZip — see `app/main.py` in the API package.
- **Health:** Public `GET /health`; authenticated GraphQL **`health.satelliteHealth`** runs best-effort probes to each configured EC2 satellite (`GET /health` or service-specific readiness).

## Satellites

- Each satellite documents **`GET /health`** (and optional `/health/ready`) in `docs/backend/endpoints/<service>/`.
- **Aggregated view:** Use GraphQL `satelliteHealth` from an authenticated session to see per-satellite `ok` / `error` / `skipped`.

## Metrics & SLO pointers

- Slice-level SLO table: [`6.Contact360 Reliability and Scaling/SLO-BY-SLICE.md`](6.Contact360%20Reliability%20and%20Scaling/SLO-BY-SLICE.md)
- Runbooks: [`6.Contact360 Reliability and Scaling/runbooks/`](6.Contact360%20Reliability%20and%20Scaling/runbooks/)
