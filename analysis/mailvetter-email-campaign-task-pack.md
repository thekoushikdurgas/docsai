# Mailvetter Task Pack (10.x)

Codebase: `backend(dev)/mailvetter`

## Contract and API

- Primary preflight endpoint: `POST /v1/emails/validate-bulk`.
- Callback contract: webhook to campaign service with job completion summary.
- Legacy `/upload` route marked deprecated and frozen.

## Execution tasks

| Task | Scope | Patch |
| --- | --- | --- |
| Finalize bulk preflight contract | contract | `10.A.0` |
| Persist campaign result snapshot tables | data | `10.A.2` |
| Implement webhook callback path | service | `10.A.1` |
| Integrate risk badges in campaign UI | surface | `10.A.3` |
| Add throughput/SLA alerts | ops | `10.A.8` |

## Required outputs

- Verification summary by `valid/invalid/catchall`.
- Recipient-level result evidence linked to `campaign_id`.
- Immutable preflight artifact for compliance replay.
