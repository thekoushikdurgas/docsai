# Phase 2 — Email & phone enrichment (Slice E)

**Owner:** data-enrichment · **Last reviewed:** 2026-04-19

## Source of truth (no fork)

- **Routes & env:** [`docs/backend/endpoints/email.server/`](../backend/endpoints/email.server/) · [`docs/backend/endpoints/phone.server/`](../backend/endpoints/phone.server/)
- **Waterfall policy:** [`docs/DECISIONS.md`](../DECISIONS.md) § Enrichment waterfall order
- **Jobs:** Gateway polls **`GET /jobs/:id/status`**; satellites use **Asynq** workers
- **Connectra:** Finder paths call **`POST /contacts/`** on sync.server with configured keys

## TRAI DND

- **Redis ~24h TTL** per destination key before SMS/WhatsApp sends (India routes) — shared with campaign pre-send gates.

## AI tools (Phase 5 catalog)

Document as thin wrappers over gateway endpoints:

- `email.find`, `phone.find`, `email.validate`, `phone.validate` → gateway → email.server / phone.server

## Done when (slice)

Single-contact enrichment + 1k bulk job complete with visible reserve/settle; TRAI DND-blocked phone rejected before send.
