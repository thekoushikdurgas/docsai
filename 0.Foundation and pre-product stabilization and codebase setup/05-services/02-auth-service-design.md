---
id: 0.2.2.2
title: `services/auth-service` skeleton
phase: 0.Foundation and pre-product stabilization and codebase setup
owner: platform
last_reviewed: 2026-04-19
status: populated
flow_refs: ["flow1"]
schema_refs: ["User.json"]
---

# `services/auth-service` skeleton

## Summary

No separate `auth-service` binary: **JWT + org context** live in the gateway; Django admin has its own auth. RLS via `SET LOCAL app.current_org_id` in the API layer per [`DECISIONS.md`](../../DECISIONS.md).

Authoritative map: [`02-architecture/04-as-built-map.md`](../02-architecture/04-as-built-map.md) (`0.2.2.2`).


## Anchors (do not fork)

- Architecture decisions: [`DECISIONS.md`](../../DECISIONS.md)
- Phase navigation: [`PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md)
- Docs entry: [`README.md`](../../README.md)
- Phase hub: [Phase README](../README.md)
- Related flows:
- [flow1](../flows/FLOW-1-contact-creation.md): `FLOW-1-contact-creation.md`
- Related schemas:
- [`User.json`](../../docs/json_schemas/User.json)

## Contracts / schemas

- Prefer links to `docs/backend/endpoints/<service>/` and [`DECISIONS.md`](../../DECISIONS.md); avoid duplicating route tables here.

## Open questions

- TBD

## Cross-links

- [`PHASE-DOCS-INDEX.md`](../../PHASE-DOCS-INDEX.md) — maintenance backlog
- Sibling sections: [`index.json`](../index.json)
