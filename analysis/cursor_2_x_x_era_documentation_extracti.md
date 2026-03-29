# 2.x.x era documentation extraction
_Exported on 3/25/2026 at 01:52:33 GMT+5:30 from Cursor (2.6.21)_

---

**User**

Read the following files and return content relevant to the 2.x.x era (email system, finder, verifier, mailbox):
1. d:\code\ayan\contact\docs\roadmap.md - search for "2.x" era sections (finder, verifier, mailvetter, email system, bulk)
2. d:\code\ayan\contact\docs\versions.md - search for "2.0", "2.1", "2.2", "2.3", "2.4" entries

Return just the relevant sections: stage names, status, KPIs, summaries, code pointers, dependencies.

---

**Cursor**


Reading both files and extracting 2.x-era content.




Here is a condensed extract focused on the **2.x email era** (finder, verifier, results, bulk, Mailvetter, mailbox-related notes) from the two files.

---

## `d:\code\ayan\contact\docs\roadmap.md`

### Current focus (2.x mention)
- Near-term work includes **bulk validation hardening (Stage 2.4)** alongside billing; **finder → verifier → results** is called the product backbone.

### **VERSION 2.x — Email System**

| Stage | Name | Status | Depends on | Risk | Definition of done | KPI | Ships in |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **2.1** | Email Finder Engine | Completed | 1.1, 1.2 | Provider inconsistency | Finder returns candidates with normalized metadata and logging | Finder success rate, median response latency | `2.0.0` |
| **2.2** | Email Verification Engine | Completed | 2.1 | External signal variability (DNS/SMTP/provider) | Normalized statuses in single and bulk flows | Verification completion rate, invalid classification precision | `2.0.0` |
| **2.3** | Results Engine | Completed | 2.1, 2.2 | UI inconsistency in status/confidence | Best result + auditable activity history | Result view completion rate, user action-to-result latency | `2.0.0` |
| **2.4** | Bulk Processing — Validation | In progress | 2.1, 2.2, 2.3 | Partial failures in stream processors / resume | Upload, async processing, checkpoint resume, output retrieval reliable | Bulk job success rate, resume success rate, processing throughput | `2.1.0` |

**Summaries / bullets (stages):**
- **2.1:** 10 pattern formats, historical logs, Go worker (`emailapigo`), provider fallback/normalization.
- **2.2:** Mailvetter (and/or configured provider); Valid / Delivered-Catchall / Undelivered-Catchall / Invalid / Not Found + confidence; DNS/SMTP/SPF/DMARC scoring.
- **2.3:** Best email + status + confidence; validation activity logs.
- **2.4:** CSV upload; streaming + checkpointing + multipart upload; concurrency: finder stream **3**, verifier stream **5**.

**Code pointers (from roadmap):**
- **2.1:** `contact360.io/app/src/services/graphql/emailService.ts`, `contact360.io/app/src/hooks/useEmailFinderSingle.ts`, `lambda/emailapis/`, `lambda/emailapigo/`
- **2.2:** `contact360.io/app/src/hooks/useEmailVerifierSingle.ts`, `backend(dev)/mailvetter/`, `contact360.io/api/sql/apis/15_EMAIL_MODULE.md`
- **2.3:** `contact360.io/app/src/components/email/EmailFinderSingle.tsx`, `contact360.io/app/src/components/email/EmailVerifierBulkResults.tsx`
- **2.4:** `contact360.io/app/src/hooks/useNewExport.ts`, `contact360.io/jobs/app/processors/email_finder_export_stream.py`, `contact360.io/jobs/app/processors/email_verify_export_stream.py`, `lambda/s3storage/docs/multipart_upload_guide.md`

### Feature-to-service matrix (2.x rows)
| Stage | Feature | Services | UI | Data | Ships |
| --- | --- | --- | --- | --- | --- |
| 2.1 | Email finder | `emailapis`, `emailapigo`, `appointment360` | `dashboard` | PostgreSQL, S3 | `2.0.0` |
| 2.2 | Email verifier | `mailvetter`, `emailapis`, `appointment360` | `dashboard` | PostgreSQL | `2.0.0` |
| 2.3 | Results engine | `appointment360` | `dashboard` | PostgreSQL | `2.0.0` |
| 2.4 | Bulk processing | `tkdjob`, `s3storage`, `emailapis`, `mailvetter` | `dashboard` | S3, PostgreSQL | `2.1.0` |

### Deep execution `1.x` → `2.x` (email-related bullets)
- **2.1 Finder:** 10-pattern generation + Go path for heavy load; credit deduction per finder call.
- **2.2 Verifier:** Reliable Mailvetter; SPF/DMARC; status normalization + confidence.
- **2.3 Results:** Best result + confidence; audit logs for verification events.
- **2.4 Bulk:** Streaming checkpoint/resume; multipart S3 + output retrieval E2E.

### Cross-era streams touching **2.x** (email / bulk / verifier)
- **`s3storage` 2.x:** Multipart protocol + retry semantics; durable multipart session; bulk-path failure recovery.
- **`logs.api` 2.x:** Email workflow and bulk processing telemetry at scale.
- **`jobs` 2.x:** Email finder/verify/pattern stream processors.
- **`contact.ai` 2.x:** `analyzeEmailRisk` contract lock; HF JSON email scoring; PII review.
- **`salesnavigator` 2.x:** Email/phone validation; enrichment handoff stub; `email_status` preservation.
- **`mailvetter` 2.x:** Primary delivery era — single/bulk verification contracts, async jobs/results, scoring model freeze. Task pack: `docs/2. Contact360 email system/mailvetter-email-system-task-pack.md`

### **Mailbox** (`contact360.io/email` era table)
- **2.x:** *core mailbox operations live (folder/detail/imap connect)*

---

## `d:\code\ayan\contact\docs\versions.md`

### Release index (2.x line)
- **`2.0.0`:** planned, TBD — *Email system era — finder, verifier, results, bulk*

### Unreleased (next cut) — 2.x tie-in
- Planned stage mapping includes **`2.4`** (bulk) alongside **`1.3`** (billing).

### **`1.0.0`** (context: work already mapped to 2.x stages)
- Roadmap mapping: **`2.1`, `2.2`, `2.3`** (plus `1.1`, `1.2`).

### **`1.1.0`** (bulk + billing)
- Roadmap mapping: **`1.3`, `2.4`**.

### Release entries **2.0.0 – 2.4.0**

| Version | Status | Target | Summary | Scope (short) | Roadmap mapping | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| **2.0.0** | planned | TBD | Email system era — dedicated email feature completeness | Finder (patterns, Go path, fallback), verifier (Mailvetter, DNS/SMTP/SPF/DMARC), results, bulk CSV | `2.1`–`2.4` | Email Engineering |
| **2.1.0** | planned | TBD | Finder production maturity | Multi-pattern generation, Go worker, credit deduction | `2.1` | Email Engineering |
| **2.2.0** | planned | TBD | Verifier production maturity | Mailvetter, SMTP/DNS/SPF/DMARC scoring, confidence normalization | `2.2` | Email Engineering + Mailvetter |
| **2.3.0** | planned | TBD | Results + audit history | Best result, confidence, activity log quality | `2.3` | Email Engineering + Dashboard |
| **2.4.0** | planned | TBD | Bulk validation hardening | CSV upload, streaming checkpoint, multipart S3, job processors | `2.4` | Data Pipeline + Storage |

### **`2.x` task-pack pattern** (`versions.md`)
- **Contract:** finder/verifier API + GraphQL schema.
- **Service:** pattern generation, Go worker, Mailvetter, bulk job processors.
- **Surface:** email UI, bulk export UX, results.
- **Data/Ops:** credit deduction accuracy, bulk checkpoint reliability, provider fallback telemetry.

### Other **`versions.md`** 2.x pointers (supporting spine)
- **`s3storage`:** `2.x` — durable multipart protocol, metadata freshness.
- **`logs.api`:** `2.x` — email workflow telemetry scale and batch behavior.
- **`connectra` 2.x:** bulk CSV import/export / streaming contract — *dependency: email finder/verifier bulk flows*.
- **`emailapis` 2.x:** email core maturity (bulk correctness + provider harmonization).
- **`jobs` 2.x:** email stream processors and bulk reliability.
- **`contact.ai` 2.x:** `analyzeEmailRisk` contract, HF JSON, PII review.
- **Appointment360 (`contact360.io/api`) 2.x:** email module (finder/verifier), jobs module (create/list/status), remove inline debug file writes.
- **Mailvetter 2.x (spine table):** **PRIMARY** — single/bulk verification contract, async job lifecycle, scoring model freeze. Docs refs: `docs/codebases/mailvetter-codebase-analysis.md`, `MAILVETTER_ERA_TASK_PACKS.md`, endpoint matrix, data lineage, Postman.
- **Email app (`contact360.io/email`):** **2.x** — core mailbox operations live (folder/detail/imap connect).

---

**Note:** Roadmap **stage IDs** (`2.1`–`2.4`) do not line up 1:1 with **release minors** `2.1.0`–`2.4.0` in `versions.md` (e.g. roadmap ships 2.1–2.3 in **`2.0.0`**, bulk stage 2.4 in **`2.1.0`**). Both files are consistent on that split if you read “stage” vs “version” separately.

