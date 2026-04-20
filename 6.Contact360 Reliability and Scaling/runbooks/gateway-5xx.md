# Runbook: gateway 5xx spike

**Symptom:** Elevated HTTP 5xx from `api.contact360.io` (ALB/CloudWatch or error logs).

## Check

1. **Deploy / config** — recent gateway release, env var typos, DB migration failure.
2. **Dependencies** — Postgres connectivity, Redis (if used for rate limit), JWT signing keys.
3. **Downstream** — run GraphQL `health.satelliteHealth` (authenticated) to see failing satellites.

## Mitigate

- Roll back last deploy if correlated.
- Scale ECS task count if CPU-bound; check rate-limit false positives.

## Escalate

- DB team if RLS or connection pool exhausted; satellite owners if single dependency red.
