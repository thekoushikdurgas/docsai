# Runbook: unexpected “out of credits” / mutations blocked

**Symptom:** Users report mutations blocked; billing UI shows zero credits; ledger anomalies.

## Check

1. **Org plan state** — active vs past_due vs read-only in gateway DB.
2. **Ledger** — failed **settle** leaving reserved credits stuck; PSP webhook delays.
3. **Recent deploy** — billing resolver or middleware change.

## Mitigate

- Manual credit adjustment via approved admin path (audit log required).
- Replay idempotent PSP webhook if payment succeeded but state not updated.

## Prevent

- Alert on reserve/settle mismatch rate; reconcile job daily.
