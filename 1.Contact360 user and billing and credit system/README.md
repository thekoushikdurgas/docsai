# Phase 1 — Identity, billing, credits (Slice B)

**Owner:** billing-platform · **Last reviewed:** 2026-04-19

## MVP architecture

| Concern | Implementation direction |
| ------- | ------------------------ |
| **Identity** | Org / user / role / invitation — **gateway Postgres** + JWT; resolver maps auth state to billing mode (**active / past_due / read-only**). |
| **RLS** | `SET LOCAL app.current_org_id` per [`DECISIONS.md`](../DECISIONS.md). |
| **Plans** | Catalog **FREE / STARTER / PRO / ENTERPRISE** as data; entitlements consumed by gateway middleware. |
| **Ledger** | Single **reserve → settle** pattern for enrichment (`EnrichmentJob.json`); **same shape** for email/SMS sends, AI tokens (meters). |
| **PSP** | Webhooks → idempotent handlers → internal billing state. Default PSP split: [`OPEN-DECISIONS-RESOLVED.md`](../OPEN-DECISIONS-RESOLVED.md). Cross-link Phase 9 billing narrative when present (`166-billing`). |
| **UI** | Billing MVP: overview, plan change, low-credit nudge, dunning surfaces. |

## GraphQL

Billing-related modules exist under `contact360.io/api/app/graphql/modules/billing/` — extend in lockstep with `DECISIONS.md` and this README.

## Done when (slice)

One org can sign up, run enrichment, see usage/credits; out-of-credit blocks gateway mutations cleanly.
