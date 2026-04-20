# Public REST v1 subset (Slice I)

**Owner:** platform-api · **Last reviewed:** 2026-04-19

## Policy

- **Public:** REST + OpenAPI only — [`DECISIONS.md`](../DECISIONS.md).
- **Product:** GraphQL for dashboard + extension on the gateway — credentials never expose satellite URLs/keys.

## Suggested v1 resources (MVP)

| Area | Operations |
| ---- | ---------- |
| Contacts | CRUD + list with stable pagination |
| Companies | CRUD |
| Enrichment jobs | Submit async job + poll status |
| Campaigns | Create draft + trigger send (idempotent) |

## Shape

- **Gateway-shaped CRM DTOs** — not raw Connectra payloads ([`OPEN-DECISIONS-RESOLVED.md`](../OPEN-DECISIONS-RESOLVED.md)).

## Auth

- API keys issued per org; gateway validates and applies same RLS / org scoping as GraphQL.

## Automation

- Keep [`../backend/endpoints/contact360.io/public-private.md`](../backend/endpoints/contact360.io/public-private.md) and [`GRAPHQL-SCHEMA-GENERATION.md`](../backend/endpoints/contact360.io/GRAPHQL-SCHEMA-GENERATION.md) updated with each release.
