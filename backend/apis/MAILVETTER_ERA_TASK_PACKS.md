# Mailvetter Era Task Pack Index

## Era task-pack files

| Era | File |
| --- | --- |
| `0.x` | `docs/0. Foundation and pre-product stabilization and codebase setup/mailvetter-foundation-task-pack.md` |
| `1.x` | `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `mailvetter-user-billing-task-pack.md` merged) |
| `2.x` | `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `mailvetter-email-system-task-pack.md` merged) |
| `3.x` | `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `mailvetter-contact-company-task-pack.md` merged) |
| `4.x` | `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `mailvetter-extension-sn-task-pack.md` merged) |
| `5.x` | `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `mailvetter-ai-task-pack.md` merged) |
| `6.x` | `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `mailvetter-reliability-scaling-task-pack.md` merged) |
| `7.x` | `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `mailvetter-deployment-task-pack.md` merged) |
| `8.x` | `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-public-private-apis-task-pack.md` merged) |
| `9.x` | `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-ecosystem-productization-task-pack.md` merged) |
| `10.x` | `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `mailvetter-email-campaign-task-pack.md` merged) |

## Canonical runtime route map

- `GET /v1/health`
- `POST /v1/emails/validate`
- `POST /v1/emails/validate-bulk`
- `GET /v1/jobs/:job_id`
- `GET /v1/jobs/:job_id/results`

Legacy compatibility routes (deprecated): `/verify`, `/upload`, `/status`, `/results`.
