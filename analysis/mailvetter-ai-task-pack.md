# Mailvetter — 5.x AI Workflows Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `5.x` — AI-assisted verification explainability

## Contract track

- [ ] Define explainability schema for AI consumption (`top_factors`, `risk_reason`, `confidence_band`).
- [ ] Define prompt-safe output contract (no sensitive raw SMTP payload).

## Service track

- [ ] Add AI-friendly summarized reason generator from `score_details`.
- [ ] Add optional “recommend action” output (`send`, `retry`, `suppress`).

## Surface track

- [ ] Email verifier UI: AI explanation drawer on result row click.
- [ ] Campaign preflight: AI summary card for risky domains.

## Data track

- [ ] Store normalized reason codes and factor vectors per result.
- [ ] Add retention policy for AI-derived summaries.

## Ops track

- [ ] Add PII redaction in AI logs and traces.
- [ ] Add quality evaluation set for explanation correctness.
