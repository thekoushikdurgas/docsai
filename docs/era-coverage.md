# Contact360 Admin — Era Coverage Register

Maps each roadmap era to its admin surface task.
Aligned with `docs/codebases/admin-codebase-analysis.md` gap register.

| Era | Focus | Admin Surface | Status |
|-----|-------|---------------|--------|
| 0.x | Foundation & stabilization | Shell, env validation, route inventory test. Skin to design tokens. All URLs mounted and functional. | ✅ Completed |
| 1.x | User & billing & credit system | Billing review (/admin/billing/payments/), credit timeline on user detail, QR payment proof flow, approve/decline with audit log. | ✅ Completed |
| 2.x | Email system | Email ops panel: provider/failure/retry visibility cards. `/admin/` → email section with provider tabs, failed delivery table, retry action. | 🔲 Planned |
| 3.x | Contact & company data | Connectra lineage panel: ingestion drift alerts, contact import status, company data freshness indicators. | 🔲 Planned |
| 4.x | Extension & Sales Navigator | Extension diagnostics: SN ingestion errors, replay UI, extension version tracking, debug console. | 🔲 Planned |
| 5.x | AI workflows | AI governance panel: model selection, quota usage gauge, prompt version management, token cost tracker. `/ai/` admin extension. | 🔲 Planned |
| 6.x | Reliability & Scaling | SLO dashboard: per-service error budget gauge, DLQ depth counter, p95 latency chart, alert rule manager. System Status enhanced. | 🔲 Planned |
| 7.x | Deployment | RBAC audit trail viewer; secret rotation checklist page; deployment event log; environment diff viewer. | 🔲 Planned |
| 8.x | Public & private APIs | API boundary view: public vs private endpoint table; versioning governance checklist; deprecation tracker. `/api/v1/` surface. | 🔲 Planned |
| 9.x | Ecosystem integrations | Integrations panel: connector health cards, partner quota usage, SLA evidence download, webhook log. | 🔲 Planned |
| 10.x | Email campaign | Campaign ops console: suppression list manager, compliance checklist, bounce rate tracker, sender reputation gauge. | 🔲 Planned |

## Implementation notes

- Each era adds a new admin section or extends an existing one.
- When implementing an era slice, update this file from `Planned` → `In Progress` → `Completed`.
- Also update `docs/codebases/admin-codebase-analysis.md` gap register.
- Add frontend page entries to `docs/frontend/pages/admin_surface.md`.
- Add new API endpoints to `docs/backend/endpoints/admin_endpoint_era_matrix.md`.
