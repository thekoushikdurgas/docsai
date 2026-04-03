# Master plan — minors `4.0`–`4.6` (five-track matrix)

**Codebase risks (explicit):** [`salesnavigator-codebase-analysis.md`](../codebases/salesnavigator-codebase-analysis.md) — scoped tenant API key model, **distributed rate limit**, **chunk-level idempotency token** — must close or waive before `4.x` scale-up.

| Minor | Contract | Service | Surface | Data | Ops |
| --- | --- | --- | --- | --- | --- |
| **4.0 Harbor** | Extension bootstrap + env matrix | `extension.server` health + config | Install / update story | Feature flags storage | Canary deploy |
| **4.1 Auth & Session** | Cookie/session contract vs gateway | Secure token exchange; CSRF | Login / reconnect UX | Session audit columns | Key rotation runbook |
| **4.2 Harvest** | Scrape + chunk upload API | Bounded workers; Mailvetter hooks | Progress + cancel | Raw chunk dedup keys | Abuse detection |
| **4.3 Sync Integrity** | Idempotent chunk apply to Connectra | Ordering + retry policy | Conflict UI | Twin-store writes traced | Reconciliation job alerts |
| **4.4 Telemetry** | Event schema + PII policy | Batching + sampling | Opt-in UX | Retention windows | Dashboards + SLOs |
| **4.5 Popup UX** | Action surface contracts | Latency budget | Chrome MV3 constraints | Local cache policy | Crash reporting |
| **4.6 Dashboard Integration** | GraphQL alignment with `3.x` | Feature gating | Shared components with app | User_scraping / metadata | Cross-service tracing |

**Cross-links:** [`21_LINKEDIN_MODULE.md`](../backend/graphql.modules/21_LINKEDIN_MODULE.md), [`23_SALES_NAVIGATOR_MODULE.md`](../backend/graphql.modules/23_SALES_NAVIGATOR_MODULE.md), [`micro.services.apis/salesnavigator.api.md`](../backend/micro.services.apis/salesnavigator.api.md).
