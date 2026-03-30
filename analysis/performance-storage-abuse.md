# Era 6.5–6.8: Performance, storage, cost, and abuse guardrails

This stage adds gateway-level controls for predictable latency and safer write traffic.

## Performance and latency tuning

- RED request telemetry remains available via `GET /health/slo`.
- New GraphQL body-size guard:
  - Middleware: `GraphQLBodySizeMiddleware`
  - Config: `GRAPHQL_MAX_BODY_BYTES`
  - Behavior: rejects oversized `POST /graphql` payloads with `413`.

## Abuse prevention and write throttling

- New per-actor mutation throttle:
  - Middleware: `GraphQLMutationAbuseGuardMiddleware`
  - Config: `MUTATION_ABUSE_GUARD_RPM`
  - Scope: operations listed in `ABUSE_GUARDED_MUTATIONS`
  - Identity source order: `X-User-ID` → `Authorization` fingerprint → IP
  - Behavior: returns `429` when per-minute write threshold is exceeded.

## Per-plan `MUTATION_ABUSE_GUARD_RPM` tuning (guidance)

Align with **roadmap Stage 6.7–6.8** and sales packaging. **Values below are examples** — set per environment after measuring legitimate peak RPM.

| Plan / tier | Example `MUTATION_ABUSE_GUARD_RPM` | Notes |
| --- | --- | --- |
| Free / trial | 30–60 | Tight; watch FP reports |
| Standard | 120–240 | Default starting band for SMB |
| Professional | 300–600 | Bulk-heavy tenants; monitor cost KPI |
| Enterprise | 600–1200 | Custom SOW; may use allowlists |

**Ops:** When sustained `429` appears on top accounts, **raise tier** before disabling guards. Track in cost + abuse dashboards (`6.7 — Cost reliability and budget guardrails.md`, `6.8 — Security and abuse resilience at scale.md`).

## Storage lifecycle and cost guardrails (runbook baseline)

- Keep S3 object retention/lifecycle policies managed in storage infrastructure
  (non-code), including automatic expiration for temporary upload artifacts.
- Keep guarded mutation set focused on high-cost side effects (billing/bulk/sync).
- Track sustained `429` rates and adjust limits by plan tier before widening defaults.

### S3 lifecycle rules snippet (reference YAML)

Use IaC appropriate to your cloud provider; below is an **Illustrative** AWS/CDK-style policy for **temporary upload prefixes**:

```yaml
# Illustrative only — adapt bucket/prefix/tags to s3storage metadata
Rules:
  - Id: expire-tmp-uploads
    Status: Enabled
    Filter:
      Prefix: tmp/uploads/
    Expiration:
      Days: 7
    AbortIncompleteMultipartUpload:
      DaysAfterInitiation: 1
  - Id: transition-exports-to-ia
    Status: Enabled
    Filter:
      Prefix: exports/
    Transitions:
      - StorageClass: STANDARD_IA
        Days: 90
```

Pair with reconciliation + orphan cleanup documented in **Service task slices** for [`6.6 — Storage lifecycle and artifact integrity`](6.6%20%E2%80%94%20Storage%20lifecycle%20and%20artifact%20integrity.md) (`6.*.*` patches).

## References

- [`6.5 — Performance and latency wave.md`](6.5 — Performance and latency wave.md)–[`6.8 — Security and abuse resilience at scale.md`](6.8 — Security and abuse resilience at scale.md)
- Era `6.x` **Service task slices** — S3 storage (`6.6` patch ladder and related `6.N.P` files)
