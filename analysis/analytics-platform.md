# Analytics Platform

**Era:** 8  
**Stage:** 8.1 - Telemetry Instrumentation  
**Status:** Active baseline

## 8.x Context

This document defines analytics rules for the API era so partner/public endpoint traffic can be observed, audited, and replayed safely.

- Event taxonomy is locked by `event_name`, `event_category`, `service`, `endpoint`, `api_version`, `tenant_id`, `actor_type`, `result`, and `duration_ms`.
- `X-Trace-Id` must be generated at ingress (or preserved if present) and propagated across `appointment360`, downstream services, and webhook delivery logs.
- PII is excluded from analytics payloads; only IDs/hashes are allowed for user/contact references.
- Error events must include normalized code groups (`auth`, `rate_limit`, `validation`, `dependency`, `internal`).

## Primary References

- `docs/backend/apis/18_ANALYTICS_MODULE.md`
- `docs/backend/endpoints/appointment360_endpoint_era_matrix.json`
- `docs/frontend/hooks-services-contexts.md` (`analyticsService`, `useAnalytics`)

## Required 8.x Outputs

- Instrument public/private API calls with taxonomy-complete events.
- Add request/response latency, status class, and rate-limit outcome tags.
- Provide daily quality report: missing fields, invalid event names, trace breaks.
- Store replay-safe event IDs for webhook and callback lifecycle analytics.
