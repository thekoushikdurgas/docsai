# Email APIs — era `3.x` contact and company data

**Services:** `lambda/emailapis`, `lambda/emailapigo` (where deployed)  
**Era:** `3.x` — Contact360 **contact and company data system**  
**Summary:** Align finder/verifier/enrichment outputs with **Connectra identity keys** and **contact/company record shape** so dashboard email surfaces show **consistent** email status, domain, and lineage with the authoritative CRM index.

This pack decomposes work into **Contract**, **Service**, **Surface**, **Data**, and **Ops** tracks. Cross-reference: [`docs/codebases/emailapis-codebase-analysis.md`](../codebases/emailapis-codebase-analysis.md), [`emailapis-ui-bindings.md`](../frontend/emailapis-ui-bindings.md), [`enrichment-dedup.md`](enrichment-dedup.md).

---

## Contract track

- [ ] Freeze **Connectra linkage** contract: optional `contact_uuid`, `company_uuid` (or equivalent) on enrichment requests/responses where the gateway orchestrates email + contact views.  
- [ ] Align **enrichment payload** shape with Connectra contact fields used for **email** / **normalized_domain** display — no conflicting names between Lambda JSON and GraphQL types.  
- [ ] Document **domain-first lookup** and **deterministic candidate merge** rules (tie-breakers, “best email” policy) for the same natural person key.  
- [ ] Update [`docs/backend/endpoints/emailapis_endpoint_era_matrix.json`](../backend/endpoints/emailapis_endpoint_era_matrix.json) (or successor) for **3.x**-scoped route/payload notes.  
- [ ] Status vocabulary for finder/verifier steps matches dashboard expectations (`emailapis-ui-bindings.md`).

## Service track

- [ ] Implement/validate **3.x** finder/verifier/pattern paths with **non-blocking** logging on credit-aware gateway hops (per analysis).  
- [ ] Harden **bulk** fan-out where contact list context is present — avoid race that shows stale email on contact row.  
- [ ] **Go/Python** parity: shared field names for Connectra bridge responses where both runtimes are active.  
- [ ] Auth, provider routing, error envelope, and health diagnostics verified for internal consumers.

## Surface track

- [ ] **Contact / company rows:** email column and verifier badges stay consistent after enrichment reload (Finder/Verifier tabs per [`docs/frontend/emailapis-ui-bindings.md`](../frontend/emailapis-ui-bindings.md)).  
- [ ] Document hooks: `useEmailFinderSingle`, `useEmailVerifierSingle`, `useEmailVerifierBulk`, and any **contact page** integration points in [`docs/frontend/hooks-services-contexts.md`](../frontend/hooks-services-contexts.md).  
- [ ] Loading / error / partial-success states documented for bulk verifier flows tied to **CSV** or **segment** context (`jobs-ui-bindings.md` where job+dashboard intersect).

## Data track

- [ ] `email_finder_cache` / **pattern** tables: lineage notes for **3.x** when cache entries tie to `contact_uuid` or domain keys.  
- [ ] Provider, status, and **traceability** (request id) expectations recorded for reconciliation with Connectra upserts.  
- [ ] Drift checks: **enrichment outcome** vs **email_status** on contact record — automated or sampling script spec ([`logsapi-contact-company-data-task-pack.md`](logsapi-contact-company-data-task-pack.md) for failure logs).

## Ops track

- [ ] Observability: alert on verifier/finder **failure spikes** after Connectra schema or mapper changes.  
- [ ] Rollback and incident runbook: “email shows wrong on contact” triage (cache purge, re-fetch, Connectra resync).  
- [ ] Release validation evidence attached to RC (sample profiles + expected hydrated rows).

---

## Execution queue (from codebase analysis)

1. **Identity**: map Lambda responses to Connectra **UUID5** keys used in [`enrichment-dedup.md`](enrichment-dedup.md).  
2. **Merge**: deterministic domain-first candidate selection for duplicate finder hits.  
3. **UI contract**: one round-trip doc — GraphQL → emailapis → contact row fields.  
4. **Drift test**: scheduled compare job or manual quarterly checklist.

## Completion gate

- [ ] Golden profile: finder/verifier → contact row shows same email + status as Connectra **after** refresh.  
- [ ] Endpoint matrix updated for **3.x**.  
- [ ] No undocumented breaking field rename on enrichment responses.

## References

- [`docs/codebases/emailapis-codebase-analysis.md`](../codebases/emailapis-codebase-analysis.md)  
- [`docs/frontend/emailapis-ui-bindings.md`](../frontend/emailapis-ui-bindings.md)  
- [`appointment360-contact-company-task-pack.md`](appointment360-contact-company-task-pack.md) — GraphQL bridge
