# EMAILAPP ERA TASK PACKS (Frontend Consumer)

## Scope
Frontend consumer surface: `contact360.io/email`.
This document maps Contact360 eras to the email app UI tasks and backend API contract usage.

## Era task packs

| Era | Focus | Key tasks |
| --- | --- | --- |
| 0.x | Foundation | Stabilize app shell, route split, theme/layout baseline |
| 1.x | User/Billing | Harden auth/login/signup/account profile flows |
| 2.x | Email system | Folder list/detail correctness, IMAP connect/switch UX |
| 3.x | Contact/company | Add mailbox-to-contact extraction/bridge points |
| 4.x | Extension | Ingestion parity hooks for extension-originated messages |
| 5.x | AI | Implement Ask AI and summarize/reply assist flows |
| 6.x | Reliability | Retry/backoff, error boundaries, telemetry |
| 7.x | Deployment | Build/deploy runbook and environment hardening |
| 8.x | APIs | Lock typed endpoint contracts and validation |
| 9.x | Ecosystem | Integrations/export hooks |
| 10.x | Campaign | Audience/campaign handoff from mailbox context |

## Security hardening tasks (`2.x` release gate)

- Replace direct mailbox credential headers (`X-Email`/`X-Password`) with tokenized mailbox session exchange.
- Remove plaintext IMAP credential persistence from browser storage (`localStorage`).
- Introduce short-lived backend-issued mailbox session tokens bound to user identity and tenant context.
- Add server-side credential vault/encryption boundary so raw mailbox secrets are never exposed to frontend runtime.
- Block `2.x` completion status until all above controls are implemented and verified in route-level tests.
