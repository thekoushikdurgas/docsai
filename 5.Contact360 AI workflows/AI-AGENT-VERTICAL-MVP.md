# AI agent vertical — MVP (Slice G)

**Owner:** ai-platform · **Last reviewed:** 2026-04-19

## Runtime split (resolved)

- **Planner / LangGraph-style runtime:** **`ai.server`** (Go + Asynq workers).
- **Gateway:** JWT, org isolation, **tool registry**, **approval-gated writes**, SSE proxy, rate limits — see [`OPEN-DECISIONS-RESOLVED.md`](../OPEN-DECISIONS-RESOLVED.md).

## Tool registry v1

| Class | Tools |
| ----- | ----- |
| **Read** | Connectra VQL list/count (scoped), `email.find` / `phone.find`, campaign metrics read |
| **Write (one)** | Example: **draft campaign** or sequence step — requires **explicit user approval** in UI before execute |

## Metering

- Token + cost telemetry → **Slice B ledger** (AI tokens as a meter alongside enrichment credits).

## Safety

- Org isolation enforced at **resolver / tool** boundary — not inside model prompts (`87-safety/04` pattern).

## Transport

- Chat token stream: **SSE** with backpressure; reuse gateway mutation abuse guards.
