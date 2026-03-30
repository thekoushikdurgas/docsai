# Contact360 email integration exploration
_Exported on 3/24/2026 at 01:38:38 GMT+5:30 from Cursor (2.6.20)_

---

**User**

Explore D:\code\ayan\contact\contact360.io\sync with medium thoroughness. Focus on email-related behavior and integrations. Return: (1) architecture map, (2) key modules/files that handle or propagate email data, (3) end-to-end flow for email fields through sync jobs, (4) risks/gaps and missing tests, (5) small prioritized task breakdown.

---

**Cursor**

I’ll scan `contact360.io/sync` with a focus on email-related logic, then map the architecture, trace email field flow through sync jobs, and call out risks/tests/tasks. I’ll start by retrieving any existing project knowledge, then inspect the relevant code paths.

I found the sync project structure and candidate email-related files; next I’ll read architecture/job/model files and then map the exact email data path. I also need to pull prior Byterover knowledge before deeper analysis.

I’ve confirmed job orchestration and now I’m drilling into contact/company models, batch upsert, and CSV job handlers to trace how `email` and related fields are parsed, transformed, stored, indexed, and exported.

## Architecture Map (Email-Focused)

- **Entry points**
  - API job creation/listing: `D:\code\ayan\contact\contact360.io\sync\modules\common\controller\jobController.go`
  - Job worker runtime: `D:\code\ayan\contact\contact360.io\sync\jobs\jobs.go`
- **Job processing + integrations**
  - S3 stream read/write + CSV parse/emit: `D:\code\ayan\contact\contact360.io\sync\jobs\s3_files.go`
  - Batch orchestration (company + contact dual writes): `D:\code\ayan\contact\contact360.io\sync\modules\common\service\batchInsertService.go`
- **Email-bearing domain models**
  - Contact source-of-truth model (`email`, `email_status`): `D:\code\ayan\contact\contact360.io\sync\models\contact.pgsql.go`
  - Contact search model (`email`, `email_status` in ES): `D:\code\ayan\contact\contact360.io\sync\models\contact.elastic.go`
  - Company model also derives `normalized_domain` from email and carries `company_name_for_emails`: `D:\code\ayan\contact\contact360.io\sync\models\company.pgsql.go`
- **Persistence + query layers**
  - PostgreSQL upsert/query contacts: `D:\code\ayan\contact\contact360.io\sync\models\contact.pgsql.repo.go`
  - Elasticsearch upsert/search contacts: `D:\code\ayan\contact\contact360.io\sync\models\contact.elastic.repo.go`
  - Filter value propagation (`filters_data`): `D:\code\ayan\contact\contact360.io\sync\models\filters_data.repo.go`
- **Query semantics**
  - VQL compiler for keyword/range/text (used by export/search jobs): `D:\code\ayan\contact\contact360.io\sync\utilities\query.go`

## Key Modules/Files Handling or Propagating Email Data

- `D:\code\ayan\contact\contact360.io\sync\jobs\s3_files.go`
  - Imports CSV rows containing `email` into batch upsert path.
  - Exports contact data using `select_columns` (including email fields if requested).
- `D:\code\ayan\contact\contact360.io\sync\modules\common\service\batchInsertService.go`
  - Cleans each row, converts to company/contact objects, deduplicates, then writes to PG+ES.
- `D:\code\ayan\contact\contact360.io\sync\models\contact.pgsql.go`
  - Canonical transformation: lowercases `email` and `email_status`.
- `D:\code\ayan\contact\contact360.io\sync\models\contact.elastic.go`
  - Mirrors contact `email`/`email_status` into search index documents.
- `D:\code\ayan\contact\contact360.io\sync\modules\contacts\service\contactService.go`
  - Builds filter_data entries from contact fields (includes `email_status` when configured in filters table).
- `D:\code\ayan\contact\contact360.io\sync\models\company.pgsql.go`
  - Uses `email` to derive `normalized_domain`; stores `company_name_for_emails`.

```22:53:D:\code\ayan\contact\contact360.io\sync\models\contact.pgsql.go
Email       string   `bun:"email" json:"email,omitempty"`
...
EmailStatus string `bun:"email_status" json:"email_status,omitempty"`
...
Email:       strings.ToLower(row["email"]),
...
EmailStatus: strings.ToLower(row["email_status"]),
```

## End-to-End Flow for Email Fields Through Sync Jobs

1. **Job creation**
   - Client posts `job_type` + `job_data` to `/common/jobs/create`.
   - Stored in `jobs` table (`data` JSONB).  
   - Files: `...modules\common\controller\jobController.go`, `...modules\common\service\jobService.go`, `...models\jobs.go`.

2. **Worker picks job**
   - `FirstTimeJob`/`RetryJobs` poll DB, set status (`open` -> `in_queue` -> `processing`), then dispatch to `ProcessInsertCsvFile` or `ProcessExportCsvFile`.  
   - File: `...jobs\jobs.go`.

3. **Import path (`insert_csv_file`)**
   - Read S3 object stream, parse CSV rows.
   - Row map is cleaned (`GetCleanedString`) in batch service.
   - `PgContactFromRowData` lowercases `email`, `email_status`; `PgCompanyFromRawData` derives company `normalized_domain` from row email domain.
   - Parallel writes:
     - PG contacts (`contacts.email`, `contacts.email_status`)
     - ES contacts (`email`, `email_status`)
     - filters_data (for configured non-direct filters, e.g., `email_status`)  
   - Files: `...jobs\s3_files.go`, `...modules\common\service\batchInsertService.go`, `...models\contact.pgsql.go`, `...models\company.pgsql.go`, `...modules\contacts\service\contactService.go`.

4. **Export path (`export_csv_file`)**
   - Job carries service + VQL + select columns.
   - For contacts: search IDs in ES, fetch projected columns from PG, stream CSV rows to S3.
   - Email fields are included only if requested in `select_columns`.  
   - Files: `...jobs\s3_files.go`, `...modules\contacts\service\contactService.go`, `...utilities\query.go`.

```66:104:D:\code\ayan\contact\contact360.io\sync\modules\common\service\batchInsertService.go
for _, row := range cleanedBatch {
    company := models.PgCompanyFromRawData(row)
    contact := models.PgContactFromRowData(row, company)
    elasticCompany := models.ElasticCompanyFromRawData(company)
    elasticContact := models.ElasticContactFromRawData(contact, company)
    ...
}
return companyUuids, contactUuids, s.UpsertBatch(pgCompanies, pgContacts, esCompanies, esContacts)
```

## Risks/Gaps and Missing Tests

- **High: retry logic likely broken for default jobs**
  - Retry filter requires `retry_count > 0`, but failures do not increment retry_count anywhere.
  - Default created jobs may never enter retry flow.
  - Files: `...models\jobs.repo.go`, `...jobs\jobs.go`.
- **High: retry scheduling ignores `run_after`**
  - `RetryJobs` query sets `Retrying: true` but no `run_after <= now` condition in repository.
  - May violate intended backoff timing.
- **High: possible panic on malformed CSV**
  - `CsvRowToMap` assumes `len(row) == len(headers)`; short rows can panic by index.
  - File: `...utilities\common.go`.
- **Medium: `run_after` based on stale timestamp**
  - `serverTime := time.Now()` is outside consumer loop, so multiple failed jobs may share incorrect retry base time.
  - File: `...jobs\jobs.go`.
- **Medium: data quality / identity collision risk**
  - Contact UUID derived from `first_name + last_name + linkedin`; missing/duplicate LinkedIn values can collapse distinct emails into one UUID.
  - File: `...models\contact.pgsql.go`.
- **Medium: missing input validation for email format in sync import**
  - CSV ingest path lowercases but does not validate email syntax or status vocabulary.
- **Bug: ignored upsert error in controller**
  - `contactService.BulkUpsert(...)` error is discarded in `contacts` batch endpoint.
  - File: `...modules\contacts\controller\contactController.go`.
- **Tests**
  - No Go tests found under `D:\code\ayan\contact\contact360.io\sync` (`*_test.go` absent).

## Small Prioritized Task Breakdown

1. **Fix retry eligibility + timing (P0)**
   - Add `run_after <= now` condition and explicit retry attempt handling (`retry_count` increment or separate attempt field).
2. **Harden CSV parsing (P0)**
   - Guard row/header length mismatch; return structured row-level errors instead of panic.
3. **Add sync-job focused tests (P0/P1)**
   - Import: email normalization, email_status propagation, malformed CSV handling.
   - Retry: failed job requeue behavior with `run_after`.
4. **Stop silent failures (P1)**
   - Handle and return BulkUpsert errors in contact batch controller.
5. **Strengthen identity and dedupe rules (P1)**
   - Revisit contact UUID strategy to avoid collisions when LinkedIn missing.
6. **Add validation/observability (P2)**
   - Optional email format checks during import + metrics on invalid/skipped email rows.

If you want, I can next produce a concrete test matrix (table-driven cases) for import/export email behavior and retry handling.

