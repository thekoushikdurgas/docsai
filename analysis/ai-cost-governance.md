# AI cost governance (Era 5 — roadmap Stages **5.3–5.4**)

Operational checklist for **per-user quotas**, **provider cost caps**, **rate limiting**, and **prompt versioning**. Wire limits to **Appointment360** (`contact360.io/api`), **Contact AI** (`backend(dev)/contact.ai`), and observability (**`logs.api`**) as implementations land.

See also [`ai-workflows.md`](ai-workflows.md) and [`docs/codebases/contact-ai-codebase-analysis.md`](../codebases/contact-ai-codebase-analysis.md).

---

## Control matrix

| Control | Intent | Wiring (enforcement location) | Env / config knobs (document as implemented) |
| ------- | ------ | ----------------------------- | --------------------------------------------- |
| Per-user / per-plan quota | Cap AI messages or utility calls per day; degrade gracefully | Primary: **`contact360.io/api`** (usage ledger + GraphQL guard before `LambdaAIClient`); optional duplicate in Contact AI | **Planned / product:** `AI_DAILY_QUOTA_MESSAGES`, `AI_DAILY_QUOTA_UTILITIES` (API service); expose plan defaults in billing config |
| Provider cost caps | Alert or hard-stop when HF/inference spend exceeds budget | **Contact AI** `HFService`: max tokens, timeout, fallback chain; future monthly/daily USD cap | **Today (Contact AI):** `HF_MAX_TOKENS`, `HF_TIMEOUT_SECONDS`, `HF_CHAT_MODEL`, `HF_FALLBACK_MODELS` in `app/core/config.py`. **Planned:** `PROVIDER_COST_CAP_USD_DAILY` or provider-specific caps |
| Request rate limit (edge) | Protect Lambda from abuse / stampedes | **Contact AI** token-bucket middleware | **`AI_RATE_LIMIT_REQUESTS`**, **`AI_RATE_LIMIT_WINDOW`** (see `app/core/config.py`) |
| Prompt versioning | Reproducible audits and rollbacks of system behavior | **Contact AI** centralizes `HF_SYSTEM_INSTRUCTION` (and utility prompts); stamp **`PROMPT_VERSION`** on chat or audit metadata (**[`5.4 — Prompt Constitution.md`](5.4 — Prompt Constitution.md)**) | **Planned:** `PROMPT_VERSION` (string/semver) in env or SSM; align with DocsAI constants per [`docs/docsai-sync.md`](../docsai-sync.md) |
| Credits / billing | Align AI usage with commercial plans | **Appointment360** deducts credits on successful inference per product rules | Configure in billing/credits module; document idempotency on retry |
| Observability | Cost and quota signals for on-call | **`logs.api`** structured events; metrics from Contact AI | Emit `ai_quota_denied`, provider errors with **no PII** ([`5.8 — Audit Telescope.md`](5.8 — Audit Telescope.md)) |

---

## Operational runbook (condensed)

1. **Quota exhaustion:** Confirm API returns user-visible error; verify no silent skip of billing; temporarily raise plan limit only via config + audit ticket.
2. **Provider overspend:** Lower `HF_MAX_TOKENS`, tighten `HF_FALLBACK_MODELS`, or disable optional models; enable kill-switch feature flag if present.
3. **Prompt incident:** Roll back `PROMPT_VERSION` / `HF_SYSTEM_INSTRUCTION` deployment; replay golden tests for `parse-filters` and chat ([`5.4 — Prompt Constitution.md`](5.4 — Prompt Constitution.md)).
4. **Rate limit storm:** Tune `AI_RATE_LIMIT_REQUESTS` / `AI_RATE_LIMIT_WINDOW`; scale Lambda concurrency; check abusive `user_id` in API logs.

---

## Compliance pointers

- PII minimization in logs: [`docs/audit-compliance.md`](../audit-compliance.md) (Era `5.x` AI controls).  
- Storage of prompts/outputs: [`5.7 — Artifact Vault.md`](5.7 — Artifact Vault.md) — Artifact Vault.
