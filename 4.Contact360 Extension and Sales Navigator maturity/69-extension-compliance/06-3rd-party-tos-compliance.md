---
id: 4.10.1.3
title: HubSpot/Salesforce/others ToS (what integrations are allowed)
phase: 4.Contact360 Extension and Sales Navigator maturity
owner: TBD
last_reviewed: 2026-04-19
status: stub
flow_refs: ["flow5"]
schema_refs: []
---

# HubSpot/Salesforce/others ToS (what integrations are allowed)

> Stub generated from [`index.json`](../index.json) (`4.10.1.3`) on 2026-04-19.
> Promote to `populated` per [`PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md) only after adding owner, last-reviewed, and a real outline.

## Summary

TBD — describe the concern owned by this section in the context of **Contact360 Extension and Sales Navigator maturity**.

**Apollo.io:** The extension **Apollo** tab reads the visible DOM on `*.apollo.io` (or sends HTML to **`/v1/apollo-scrape`** for server-side parsing). Product and legal must confirm this use is permitted under **Apollo.io Terms of Service** and your customer agreements before broad rollout. Ship behind storage flag **`c360_apollo_enabled`** (default on); set to `false` for an instant kill-switch — see release/rollback docs under `70-extension-testing/`.

## Anchors (do not fork)

- Architecture decisions: [`DECISIONS.md`](../../DECISIONS.md)
- Phase navigation: [`PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md)
- Docs entry: [`README.md`](../../README.md)
- Phase hub: `4.Contact360 Extension and Sales Navigator maturity/README.md` (create hub when ready)
- Related flows:
- [flow5](../../0.Foundation and pre-product stabilization and codebase setup/flows/FLOW-5-extension-enrich.md): `FLOW-5-extension-enrich.md`
- Related schemas:
- *(none)*

## Contracts / schemas

- TBD: list HTTP routes, GraphQL fields, Kafka topics, or Postgres tables touched by this section. Link to `docs/backend/endpoints/<service>/` instead of duplicating route tables.

## Open questions

- TBD

## Cross-links

- [`PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md) — maintenance backlog
- Sibling sections: [`index.json`](../index.json)
