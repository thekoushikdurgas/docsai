# Campaign Commercial and Compliance (10.x)

## Send metering and billing linkage

- Meter strategy: default per send attempt, optional per delivered (contract-specific).
- Every send event must carry `org_id` + `campaign_id` for credit reconciliation.
- Reconciliation source: logsapi immutable events + campaign counters.

## PII retention policy

- `recipients` and related evidence follow tenant retention policy.
- Redact PII in operational logs and support bundles.
- Enforce scheduled purge jobs with audit trail.

## Opt-out and consent audit

- Immutable record for unsubscribe with source, actor, campaign, timestamp.
- Suppression entry written before further sends.
- GDPR/CAN-SPAM traceability must be queryable by campaign and recipient.

## Contract freeze and reproducibility

- Lock template hash + audience snapshot at send start.
- Preserve release contract references for endpoint/status vocab at run time.
- Any change after freeze requires new patch release or explicit compliance waiver.

## 10.x patch delivery mapping

- `10.A.7`: compliance/audit delivery.
- `10.A.9`: governance lock and release sign-off evidence.
