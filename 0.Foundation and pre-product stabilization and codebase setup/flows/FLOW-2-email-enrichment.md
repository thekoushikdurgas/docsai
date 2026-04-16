# Flow 2 — Email enrichment pipeline (canonical)

**Diagram (PNG):** [`flow2_email_enrichment.png`](../../prd/flow2_email_enrichment.png)  
**Related phases:** `2` (email/phone), `3` (data), `1` (credits), `7` (AWS)  
**Schemas:** `EnrichmentJob.json`, `enrichment.job.completed.v1.json`, `BillingLedgerEntry.json`

## Summary

Bulk and transactional enrichment path from research: **User uploads CSV** → **Storage service** issues **presigned PUT** → object lands in **S3** → **Lambda** validates schema → jobs land in **Redis / BullMQ** → **Pattern Engine** (internal rules, e.g. **12 patterns**) → external **waterfall** (Hunter / Apollo → **SMTP verify** mailbox ping → **ZeroBounce** catch-all handling) → rows **saved + scored** in **PostgreSQL**, output CSV via **presigned GET**, user notified (**email + in-app**).

Single-contact enrichment reuses the same waterfall stages with smaller queue units.

## Actors

- **User** — upload, download results
- **Storage / file-service** — presigned URLs
- **AWS S3** — durable object for CSV
- **Lambda** (or worker) — schema validation, enqueue
- **BullMQ workers** — chunked processing
- **Pattern Engine** — deterministic internal enrichment
- **External APIs** — Hunter.io, Apollo (examples from diagram)
- **SMTP verify** — mailbox-level verification
- **ZeroBounce** — catch-all / risky domain classification
- **PostgreSQL** — contacts + job state + scores
- **Notification** — completion to user

## Step-by-step

1. Client requests presigned upload; **PUT** CSV to S3.
2. S3 event → **schema validate** (reject malformed early).
3. Enqueue **BullMQ** jobs per chunk with idempotency keys per org.
4. Run **Pattern Engine**; on miss, **fallback** to external tier-1.
5. Chain **SMTP verify** then **ZeroBounce** as in diagram waterfall.
6. Persist enriched fields; write **billing ledger** lines for metered providers.
7. Write **output CSV** to S3; return **presigned GET** link.
8. Emit **`enrichment.job.completed`** (and optional in-app/email notify).

## Data contracts

| Type | Name / pattern |
| ---- | ---------------- |
| S3 | `imports/{org_id}/{job_id}/input.csv`, `.../output.csv` |
| Redis / BullMQ | Queue `enrichment:org:{org_id}`; job locks `lock:enrich:{job_id}` |
| Rate limit | **Redis token bucket per org** (diagram footnote) |
| Kafka | `enrichment.job.completed` (and optional `contact.updated`) |
| Postgres | `enrichment_jobs`, `contacts`, `billing_ledger_entries` |

## Waterfall (documented reference)

Order aligned with research diagram (see also `docs/DECISIONS.md`):

**Pattern Engine → Hunter.io → Apollo → SMTP verify → ZeroBounce**

(Provider names are interchangeable with equivalents under the same contract/credit rules.)

## Error paths

- **Invalid CSV** — fail fast at Lambda; no credits consumed.
- **Provider timeout** — retry with backoff; partial rows flagged.
- **Insufficient credits** — pause queue for org; surface in UI.
- **SMTP greylisting** — deferred retry bucket.

## Cross-links

- `docs/prd/contact360_detailed_flow.md`, `docs/prd/database-schema.md`.
- Phase 2 PRD: `docs/prd/Read all the above and previous prompts and then t (3).md`.
- Flow 1 (contact creation), Flow 4 (campaign uses verified emails).
