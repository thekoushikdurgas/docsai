# RBAC and authorization (Era 7 — Stages 7.1–7.2)

Contact360 uses **role names** on `UserProfile` plus resolver-level checks in the GraphQL API (`contact360.io/api`).

## Role model

Defined in `contact360.io/api/app/core/constants.py`:

| Role | Notes |
| ---- | ----- |
| `SuperAdmin` | Highest privilege; billing plan admin, payment instructions, destructive plan ops |
| `Admin` | Operational admin; payment proof approve/decline, many read admin queries |
| `ProUser` | Paid tier capabilities (feature gating in places) |
| `FreeUser` | Default role for new users |

`UNLIMITED_CREDITS_ROLES` = `SuperAdmin`, `Admin` (no credit deduction; subscription not required for testing paths).

## Gateway (GraphQL) enforcement

- **Authentication:** JWT in `Authorization: Bearer …`; user loaded in `app/graphql/context.py`.
- **Require login:** `require_auth(info.context.user)` in `app/core/security.py`.
- **Require admin (Admin or SuperAdmin):** `require_admin(profile)` or `require_profile_roles(profile, ADMIN, SUPER_ADMIN)` (use constants).
- **Examples:**
  - Billing admin mutations: `app/graphql/modules/billing/mutations.py` — `SuperAdmin` for plan CRUD; `Admin`/`SuperAdmin` for payment review.
  - Resource ownership: e.g. AI chats — `user_id` on resource must match caller.

## Content / feature gating

- `app/utils/access_control.py` — `ROLE_HIERARCHY`, `has_role_access`, `is_role_higher_or_equal` for DocsAI-style content visibility.

## Service-level auth (downstream)

| Service | Mechanism |
| ------- | --------- |
| Lambda AI / Email / etc. | `X-API-Key` + service-specific headers (see each client under `app/clients/`) |
| Connectra | `CONNECTRA_API_KEY` on outbound requests |
| Contact AI (browser/extension) | Session + GraphQL; see `docs/extension-auth.md` |

**Rule:** gateway validates **who** the user is; downstream services validate **API identity** (keys). Do not trust client-supplied user id without JWT-bound context.

## Hardening checklist

- 📌 Planned: New mutations use `require_auth` + explicit role or ownership check.
- 📌 Planned: Admin-only paths use `require_profile_roles` with imported constants (not string typos).
- 📌 Planned: Partner/public APIs (future) use separate keys and scopes — see Era 8.
- 📌 Planned: Admin settings controls in `contact360.io/admin` are fully wired and role-enforced (no placeholder-form deployment for governance-critical settings).
