---
id: 0.4.0.3
title: List contacts and filter aggregates (`filterData`)
phase: 0.Foundation and pre-product stabilization and codebase setup
owner: platform
last_reviewed: 2026-04-19
status: populated
flow_refs: ["flow1"]
schema_refs: ["Contact.json"]
---

# List contacts end‑to‑end (foundation v0)

## Summary

The dashboard lists contacts via GraphQL queries on the gateway; filter chips / facet counts use **`contacts.filterData`**, which delegates to Connectra’s **`get_filter_data`** for the **`contact`** service. The GraphQL type returns **`total`** from the Connectra response’s **`total`** field when present — this is the **global** match count for that filter key (not merely the current page length). Implementation: [`app/graphql/modules/contacts/queries.py`](../../../contact360.io/api/app/graphql/modules/contacts/queries.py) (`filterData`). Parity tests: [`tests/graphql/test_contacts_filters.py`](../../../contact360.io/api/tests/graphql/test_contacts_filters.py).

**VQL / filters:** [`../../3.Contact360 contact and company data system/52-app-contacts-vql-filters.md`](../../3.Contact360%20contact%20and%20company%20data%20system/52-app-contacts-vql-filters.md), [`../../tech/dashboard-graphql-vql.md`](../../tech/dashboard-graphql-vql.md), [`../../docs/contacts-filter-vql-ui.md`](../../docs/contacts-filter-vql-ui.md).

## Flow

1. Authenticated user loads contacts list in **`contact360.io/app`**.
2. **`POST /graphql`** — list query(ies) + optional **`filterData`** for facet buckets; JWT + RLS same as create path.
3. Gateway → Connectra HTTP with **`X-API-Key`** and **`X-Request-Id`** (see FLOW-1 doc and `BaseHTTPClient`).
4. UI displays **`filterData.total`** as global aggregate per [`DECISIONS.md`](../../DECISIONS.md) dashboard rules.

## Contracts / schemas

- [`../../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md`](../../backend/endpoints/contact360.io/GRAPHQL-SCHEMA.md) — `ContactFilterDataConnection`, `filterData`.
- [`Contact.json`](../../docs/json_schemas/Contact.json)

## Cross-links

- **Phase 0 flow:** [`../flows/FLOW-1-contact-creation.md`](../flows/FLOW-1-contact-creation.md) (same gateway spine).
- [`../../OBSERVABILITY-BASELINE.md`](../../OBSERVABILITY-BASELINE.md)
