# Hiring analytics suite

Routes:

- **Demands & Trends** (`/demands-and-trends`) — filtered hiring-signal sample (limit 500) with KPI strip and breakdown charts. Uses `src/lib/hiringAnalytics.ts` aggregations client-side.
- **Market Insights** (`/market-insights`) — six tabs over the same filtered sample.

Dashboard **hiring KPI strip** (Pro/admin) reads `hireSignal.dashboardKpis`, backed by **job.server** `GET /api/v1/jobs/kpis` (Mongo aggregates).

Skill soft/hard split uses **`src/lib/skillCategories.ts`** heuristics.

Company detail **Hiring signals** tab loads `hireSignal.companyJobs` (limit 200) via `useCompanyHiringSignals`.

Shared primitives live under `src/components/feature/hiring-analytics/`.
