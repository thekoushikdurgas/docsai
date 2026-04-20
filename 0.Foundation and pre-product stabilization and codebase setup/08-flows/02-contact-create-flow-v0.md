---
id: 0.4.0.2
title: Create contact end‑to‑end (UI → gateway → Connectra)
phase: 0.Foundation and pre-product stabilization and codebase setup
owner: platform
last_reviewed: 2026-04-19
status: populated
flow_refs: ["flow1"]
schema_refs: ["Contact.json"]
---

# Create contact end‑to‑end (foundation v0)

## Summary

**FLOW-1 (slice):** Dashboard (**[`contact360.io/app`](../../../contact360.io/app)**) calls GraphQL mutation **`contacts.createContact`** on the gateway (**[`contact360.io/api`](../../../contact360.io/api)** `POST /graphql`) with a **JWT**. The gateway enforces auth, applies **RLS** via `SET LOCAL app.current_org_id` on its DB session where applicable, maps input to Connectra JSON, and persists through **Connectra** (`EC2/sync.server`) using **`ConnectraClient.batch_upsert_contacts`** with **`X-API-Key`** identity. Responses return the created contact (including **UUID** aligned with Connectra’s deterministic UUID5 rules — see `EC2/sync.server/docs/EXTENSION_SCRAPER_UUID5.md`). **`X-Request-ID`** is assigned early in the gateway middleware stack and forwarded to Connectra as **`X-Request-Id`** via [`app/clients/base.py`](../../../contact360.io/api/app/clients/base.py).

**Canonical narrative:** [`../flows/FLOW-1-contact-creation.md`](../flows/FLOW-1-contact-creation.md) · **Spine:** [`../../3.Contact360 contact and company data system/50-connectra-vql-spine.md`](../../3.Contact360%20contact%20and%20company%20data%20system/50-connectra-vql-spine.md).

## Implementation pointers (code)

| Step | Location |
| ---- | -------- |
| Middleware / `X-Request-ID` | [`contact360.io/api/app/main.py`](../../../contact360.io/api/app/main.py) — see `RequestIdMiddleware`; order documented in comments § **Middleware order**. |
| Mutation | [`app/graphql/modules/contacts/mutations.py`](../../../contact360.io/api/app/graphql/modules/contacts/mutations.py) — `createContact` → `create_connectra_entity`. |
| Mapping | [`app/utils/connectra_mappers.py`](../../../contact360.io/api/app/utils/connectra_mappers.py) — `map_create_contact_input`. |
| Connectra upsert + fetch | [`app/graphql/common/crud_helpers.py`](../../../contact360.io/api/app/graphql/common/crud_helpers.py) — `batch_upsert_contacts` then VQL fetch by UUID. |
| Outgoing correlation | [`app/clients/base.py`](../../../contact360.io/api/app/clients/base.py) — sets `headers["X-Request-Id"] = get_request_id()`. |

## Contracts / schemas

- GraphQL: see [`../../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md`](../../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md) and [`ROUTES.md`](../../backend/endpoints/contact360.io/ROUTES.md).
- JSON schema (reference): [`Contact.json`](../../docs/json_schemas/Contact.json).

## Validation notes

- **Integration test** exercising the mutation (mocked Connectra): [`contact360.io/api/tests/integration/test_connectra_integration.py`](../../../contact360.io/api/tests/integration/test_connectra_integration.py) (`test_create_contact_mutation`).
- Run in CI: **`api-ci.yml`** on `contact360.io/api`.

## Cross-links

- [`DECISIONS.md`](../../DECISIONS.md) — gateway / Connectra / RLS.
- [`../../OBSERVABILITY-BASELINE.md`](../../OBSERVABILITY-BASELINE.md) — request correlation.
