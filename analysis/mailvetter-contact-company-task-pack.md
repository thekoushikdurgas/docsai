# Mailvetter — 3.x contact & company data

**Service:** `backend(dev)/mailvetter`  
**Era:** `3.x` — Verification **lineage** linked to **contacts** and **companies** in Connectra (dashboard shows “last verified” grounded in Mailvetter results).

Cross-reference: [`docs/codebases/mailvetter-codebase-analysis.md`](../codebases/mailvetter-codebase-analysis.md).

---

## Contract track

- [ ] Define verification-to-contact linkage: required/optional **`contact_uuid`**, optional **`company_uuid`** on verify requests and stored results.  
- [ ] **Freshness contract:** how “last verified at” on contact/company rows is computed (latest successful verify vs any attempt); TTL for stale badge.  
- [ ] Status vocabulary alignment with dashboard badges (`pending` / `processing` / `completed` / `failed` — per analysis hardening).

## Service track

- [ ] Accept optional Contact360 identifiers in **single** and **bulk** verify payloads.  
- [ ] Enrichment handoff fields compatible with **Connectra** email / domain columns when gateway merges verifier output into contact records.  
- [ ] Resolver or callback path to **update** existing contact verification metadata without duplicate noise.

## Surface track

- [ ] Contacts table: **verifier status** badge and **last-verified** timestamp (see email/Mailvetter UI bindings in frontend docs).  
- [ ] Company detail: aggregate verifier health by **domain** (optional **`3.x`** scope).

## Data track

- [ ] Extend `results` (or equivalent) with nullable **`contact_uuid`**, **`company_uuid`**.  
- [ ] Indexes for lookup by **`contact_uuid`** / **`company_uuid`** for reconciliation jobs.

## Ops track

- [ ] **Reconciliation job:** orphaned Mailvetter rows with no resolvable contact — weekly report + optional auto-archive.  
- [ ] **Drift report:** compare Connectra **email** / **email_status** with latest Mailvetter verdict; threshold alerting.  
- [ ] **Runbook:** [`docs/governance.md`](../governance.md) / ops folder — incident: “verifier says valid but CRM shows bounce” (cache, async merge lag, wrong uuid link).  
- [ ] Release gate: idempotency on bulk create (per analysis execution queue) when touching contact linkage.

---

## Freshness contract (detail)

| Field | Rule |
| --- | --- |
| `verified_at` | UTC timestamp of **successful** completion event |
| Display on CRM row | Max(`verified_at`) for linked `contact_uuid` |
| Stale | If `now - verified_at > N days`, show muted badge + “re-verify” CTA (product-defined `N`) |

Document **`N`** and exceptions (free plan vs paid) in PRD or [`docs/roadmap.md`](../roadmap.md).

---

## Completion gate

- [ ] Sample bulk verify with **`contact_uuid`** → contact row shows badge + timestamp after gateway merge.  
- [ ] Orphan reconciliation report runs in staging with zero **unexpected** data loss.  
- [ ] Drift report query documented for support (`logs.api` or DB script).  
- [ ] Runbook linked from this pack or from [`docs/audit-compliance.md`](../audit-compliance.md) if verifier evidence is audit-relevant.

---

## References

- [`docs/codebases/mailvetter-codebase-analysis.md`](../codebases/mailvetter-codebase-analysis.md)  
- [`emailapis-contact-company-task-pack.md`](emailapis-contact-company-task-pack.md) — adjacent enrichment  
- [`enrichment-dedup.md`](enrichment-dedup.md) — identity keys
