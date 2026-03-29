# Contact360 Runbook Index

This index tracks minimum rollback and incident runbooks required by the `0.10` foundation exit gate.

## Core services

- `contact360.io/api` (Appointment360 gateway)
- `contact360.io/sync` (Connectra)
- `contact360.io/jobs` (TKD Job)
- `lambda/s3storage`
- `lambda/logs.api`
- `lambda/emailapis`
- `lambda/emailapigo`
- `backend(dev)/salesnavigator`
- `backend(dev)/contact.ai`
- `backend(dev)/resumeai`
- `backend(dev)/email campaign`

## Required runbook sections

Each service runbook should include:

1. Health endpoints and expected healthy payload.
2. Required environment variables and secret sources.
3. Deploy command(s) and rollback command(s).
4. Smoke checks to validate post-deploy behavior.
5. Escalation path and ownership.

## Foundation exit note

Until all service-specific runbooks are complete, this index is the canonical checklist anchor for `0.10.9 — Handoff`.
