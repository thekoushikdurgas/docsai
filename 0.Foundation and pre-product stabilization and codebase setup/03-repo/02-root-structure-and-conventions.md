---
id: 0.2.0.2
title: Define root folder layout
phase: 0.Foundation and pre-product stabilization and codebase setup
owner: platform
last_reviewed: 2026-04-19
status: populated
flow_refs: ["flow1"]
schema_refs: []
---

# Define root folder layout

## Summary

Real monorepo roots are **not** npm `apps/*` + `services/*`; see the table in the as-built map (gateway under `contact360.io/`, satellites under `EC2/`).

Authoritative map: [`02-architecture/04-as-built-map.md`](../02-architecture/04-as-built-map.md) (`0.2.0.2`).


## Anchors (do not fork)

- Architecture decisions: [`DECISIONS.md`](../../DECISIONS.md)
- Phase navigation: [`PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md)
- Docs entry: [`README.md`](../../README.md)
- Phase hub: [Phase README](../README.md)
- Related flows:
- [flow1](../flows/FLOW-1-contact-creation.md): `FLOW-1-contact-creation.md`
- Related schemas:
- *(none)*

## Contracts / schemas

- Prefer links to `docs/backend/endpoints/<service>/` and [`DECISIONS.md`](../../DECISIONS.md); avoid duplicating route tables here.

## Open questions

- TBD

## Cross-links

- [`PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md) — maintenance backlog
- Sibling sections: [`index.json`](../index.json)
