# emailapis task pack — era `5.x`

This pack decomposes `lambda/emailapis` and `lambda/emailapigo` work into Contract, Service, Surface, Data, and Ops tracks for **Contact360 AI workflows**.

**References:** [`docs/codebases/emailapis-codebase-analysis.md`](../codebases/emailapis-codebase-analysis.md), [`docs/backend/endpoints/emailapis_endpoint_era_matrix.json`](../backend/endpoints/emailapis_endpoint_era_matrix.json) (update when REST surface changes).

---

## Contract tasks

- [ ] Define **AI-assisted finder/verifier payload boundaries**: max list sizes, required identity keys (`first_name`, `last_name`, `domain`), and canonical status enum values shared with dashboard and Contact AI orchestration (`5.x` era freeze).
- [ ] Document **safe orchestration surface**: which operations AI may trigger (e.g. single verify vs bulk) vs require human confirmation; avoid exposing raw provider blobs to prompts.
- [ ] Update endpoint/reference matrix in `docs/backend/endpoints/emailapis_endpoint_era_matrix.json` when adding or changing AI-facing paths.
- [ ] Align **Python vs Go parity** on verifier provider priority (`mailvetter` vs `truelist` / `icypeas`) so AI-facing summaries do not drift by runtime.

## Service tasks

- [ ] Expose **stable, minimal JSON** responses for paths consumed by Appointment360 / future AI tools; consistent error envelope for quota and provider failures.
- [ ] Verify auth, provider routing, error translation, and health diagnostics under AI-driven traffic (higher fan-out risk).
- [ ] Add contract tests: finder cache hit/miss, verifier status mapping, bulk partial failure semantics.

## Surface tasks

- [ ] Document impacted pages/tabs/buttons/inputs for era `5.x` — especially assistant panels and email flows in [`docs/frontend/emailapis-ui-bindings.md`](../frontend/emailapis-ui-bindings.md).
- [ ] Document hooks/services/contexts and UX states (loading / error / progress / checkbox / radio) when AI suggests next actions on email results.
- [ ] Bind assistant panel results to **canonical email statuses** (no duplicate unofficial strings).

## Data tasks

- [ ] Document `email_finder_cache` and `email_patterns` lineage impact for era `5.x` when AI triggers lookups (cache poisoning, attribution).
- [ ] Track **AI-assisted decision lineage**: link job or request id to finder/verifier outcome **with confidence mapping** where Mailvetter/Contact AI participates (`5.x` analysis).
- [ ] Record provider, status, and traceability expectations per response for downstream logs.api events.

## Ops tasks

- [ ] Add observability checks and release validation evidence for era `5.x` (dashboards for AI-assisted failure clusters).
- [ ] Capture rollback and incident-runbook notes for email-impacting releases touching AI paths.
- [ ] Monitor **AI-assisted quality regressions** (spike in `unknown` / mismatch between runtimes).

---

## Cross-links

- Era version anchor: [`version_5.9.md`](version_5.9.md) Explainability Export (mailvetter + emailapis alignment).
- GraphQL gateway remains primary dashboard contract; lambdas stay execution plane.
