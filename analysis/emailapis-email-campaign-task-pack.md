# EmailAPIs Task Pack (10.x)

Codebases: `lambda/emailapis`, `lambda/emailapigo`

## Campaign pre-send verification contract

- Endpoint must support bulk verification for campaign recipients.
- Required status vocabulary: `valid | invalid | catchall`.
- Response must include traceable evidence per recipient for compliance replay.

## Execution tasks

| Task | Scope | Patch |
| --- | --- | --- |
| Freeze campaign verification request/response schema | contract | `10.A.0` |
| Implement immutable verification evidence storage | data | `10.A.2` |
| Align UI badge/status values with verifier outcomes | surface | `10.A.3` |
| Add reliability budget and retry policy for provider fallbacks | ops | `10.A.6` |

## Evidence model

- Required fields: `campaign_id`, `recipient_email`, `provider`, `status`, `score`, `trace_id`, `verified_at`.
- Evidence cannot be overwritten; corrections append new version row.
