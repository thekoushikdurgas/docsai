# Mailvetter — 4.x Extension & Sales Navigator Task Pack

**Service:** `backend(dev)/mailvetter`  
**Era:** `4.x` — Extension and SN maturity integration

## Contract track

- [ ] Define provenance contract: `source=extension|sales_navigator|dashboard`.
- [ ] Define idempotency contract for repeated extension verification submits.

## Service track

- [ ] Add source-tag support in verification payloads and persisted results.
- [ ] Add anti-abuse safeguards for extension burst traffic.
- [ ] Add priority queueing policy for interactive extension calls.

## Surface track

- [ ] Extension: show verification progress and final state badges.
- [ ] SN import flow: pre-verify selected leads before save/export.

## Data track

- [ ] Add `source` and `source_session_id` in `results` metadata.
- [ ] Add dedupe key for repeated verification within short windows.

## Ops track

- [ ] Add extension-specific rate and error dashboards.
- [ ] Add source-based abuse detection and alerting.


## References

- [docs/codebases/mailvetter-codebase-analysis.md](../codebases/mailvetter-codebase-analysis.md)
