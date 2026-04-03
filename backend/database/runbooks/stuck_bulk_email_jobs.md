# Runbook: stuck bulk email / export jobs (Era 2.4)

Operator steps when a **bulk finder**, **verifier**, or **pattern** job stops progressing or stays in `processing` / `in_queue` too long.

## Preconditions

- Identify **`job_id`** from the dashboard Jobs table or GraphQL `job(jobId)`.
- Confirm user still exists and owns the job (`scheduler_jobs.user_id` → `users.uuid`).

## Triage

1. **Gateway / DB:** `SELECT job_id, status, job_type, source_service, status_payload, updated_at FROM scheduler_jobs WHERE job_id = :job_id;`
2. **Worker truth:** If `source_service = email_server`, check `status_payload` from email.server for live errors (rate limit, Mailvetter, S3).
3. **S3 input:** Verify multipart upload completed; input key present and readable.
4. **Checkpoint:** If processor supports resume, confirm checkpoint cursor advanced; if not, treat as stuck worker.

## Mitigations

| Situation | Action |
| --- | --- |
| Transient provider error | Use GraphQL **`retryJob`** (if applicable to job family) after cooldown. |
| Bad CSV / schema | Fix source file; create a **new** job (document idempotency token if re-uploading same file). |
| Worker OOM / crash | Restart worker pod/process; rely on checkpoint resume — verify idempotency before manual DB edits. |
| Duplicate job rows | Do not delete rows without lineage review; mark superseded in ops notes. |

## Escalation

- Capture: `job_id`, user id, timestamps, last `status_payload`, S3 input/output keys.
- Open incident with **Data Pipeline** + **Platform** if S3 or multipart metadata worker is implicated (see **Hard gate** risks in era doc `docs/2. Contact360 email system/2.4 — Bulk Processing.md`).

## Links

- GraphQL: [`16_JOBS_MODULE.md`](../graphql.modules/16_JOBS_MODULE.md)
- DDL: [`../scheduler_jobs.sql`](../scheduler_jobs.sql)
