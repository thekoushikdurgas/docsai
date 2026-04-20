# Campaign send + engagement (Slice H)

**Owner:** campaigns · **Last reviewed:** 2026-04-19

## Anchor

- **Satellite:** `campaign.server` — `/campaigns`, `/sequences`, `/campaign-templates`, `/cql/*`; Asynq tasks `campaign:send|email|phone|linkedin|sequence_step` — [`DECISIONS.md`](../DECISIONS.md).
- **Gateway:** GraphQL `campaignSatellite`, `campaigns` mutations; **SSE** for web progress.

## Entity lifecycle

- Align JSON models with **`Campaign.json`** and campaign.server internal models (document field parity in service repo).

## CQL round-trip

1. Builder UI → gateway parse/validate → **campaign.server** `/cql/*` — **single program** for sequences ([`OPEN-DECISIONS-RESOLVED.md`](../OPEN-DECISIONS-RESOLVED.md) — separate workflow DSL is future-only).

## Audience & gates

- Audience from **VQL** saved segments (Slice C).
- **Pre-send:** Slice E validations + **TRAI DND** cache (Redis ~24h) for SMS/WhatsApp India routes.

## Engagement → Kafka

- Topics: **`email.opened`**, **`email.clicked`**, **`email.bounced`**; future **`email.replied`** — key `org_id`; consumers feed analytics + **lead scoring** (Slice I).

## Frequency

- **Caps + suppression** at gateway/queue boundary before provider dispatch.
