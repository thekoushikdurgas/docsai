# Lead scoring v1 (Slice I)

**Owner:** growth-data · **Last reviewed:** 2026-04-19

## Inputs

- **Demo / firmo** fields from Connectra.
- **Behavioral** events from Kafka: enrichment outcomes (Slice E), **`email.*`** engagement (Slice H).

## Store

- Single **canonical** score row per contact per org with **versioned ruleset** id.

## Explainability

- API returns **top-3 reasons** (rule ids + human labels).

## Handoff

- **Top-N leads** + **“add to sequence”** mutation reuses **Slice H** campaign/sequence APIs — no second sequencer.
