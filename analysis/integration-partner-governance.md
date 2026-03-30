# Integration contract governance + partner identity (Era 8 — Stages 8.1–8.2)

## Contract governance

**Principles**

- Every outbound integration (Lambda, Connectra, s3storage, third-party HTTP) is documented with: base URL, auth scheme, timeout, and idempotency expectations — see `contact360.io/api/app/clients/`.
- Breaking changes require a **version bump** in the consumer and a changelog entry; GraphQL schema changes follow deprecation rules in `docs/public-api-surface.md` (when published).
- Error shapes should map to gateway `GraphQL` errors where proxied; avoid leaking upstream stack traces to clients.

## Partner identity

**Today**

- **First-party clients** (dashboard, extension): user identity via **JWT** (`Authorization: Bearer`) — `docs/7. Contact360 deployment/rbac-authz.md`.
- **Service-to-service**: each downstream service uses its own **API key** (e.g. `X-API-Key`, Connectra key) — configured in `app/core/config.py` / env templates.

**Partner / B2B (target)**

| Concern | Approach |
| ------- | -------- |
| Partner id | Issued `client_id` + rotating **client_secret** or mTLS (infrastructure choice) |
| Scopes | Explicit allowlists per integration (read contacts, enqueue jobs, …) |
| Tenant safety | All partner tokens bound to `tenant_id`; resolvers enforce scope + tenant row access |

Until dedicated partner OAuth/m2m is implemented, treat **integration keys as secrets**, rotate on compromise, and never embed them in client-side code.

## Tenant-safe access (integrations)

- Do not accept a raw `user_id` / `tenant_id` from the partner body without cryptographic binding to the authenticated principal.
- Prefer **short-lived delegated tokens** or signed webhooks (see Era 8 webhook doc) for callbacks.
- Log partner id + `X-Trace-Id` on every cross-boundary call for audit — `docs/6. Contact360 Reliability and Scaling/queue-observability.md`.

## Era 9 partner token model

### Partner token schema

Define a tenant-bound partner token model (implementation choice: table, secure store, or auth provider), with canonical fields:

| Field | Purpose |
| ----- | ------- |
| `partner_id` | Stable identity for partner integration |
| `client_id` | Public credential identifier |
| `client_secret_hash` | Rotatable secret material (never plaintext persisted) |
| `tenant_id` | Hard binding between partner credentials and tenant boundary |
| `scopes` | Explicit allowlist (`read_contacts`, `enqueue_jobs`, `read_logs`, etc.) |
| `status` | `active`, `rotating`, `revoked` |
| `expires_at` | Time-bounded credential lifetime |
| `created_by` / `rotated_by` | Governance and audit ownership |

### Scope enforcement (gateway context)

- Resolve partner identity and scopes at request ingress.
- Attach `partner_id`, `tenant_id`, and scope claims to request context (for example in `app/graphql/context.py` and middleware).
- Enforce deny-by-default scope checks before resolver/service execution.

### Tenant-safe resolver guard pattern

- Resolver and downstream calls must verify both:
  1. token scope allows operation, and
  2. resource tenant matches authenticated `tenant_id`.
- Never trust partner-provided tenant identifiers without signed principal binding.
- Log denied operations with `partner_id`, scope mismatch reason, and `X-Trace-Id`.

### Secret rotation lifecycle

- Define phased rotation (`active` -> `rotating` -> `revoked`) with overlap window.
- Require immediate revoke flow for compromised credentials.
- Record rotation/revoke events in immutable audit trail with actor and timestamp.
