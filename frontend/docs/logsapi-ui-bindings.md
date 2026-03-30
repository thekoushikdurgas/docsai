# logs.api UI bindings

## Purpose
Map `lambda/logs.api` to dashboard/ops surfaces including pages, tabs, buttons, inputs, components, hooks, contexts, and graph/flow elements.

## Binding matrix
| Era | Pages/tabs | Components | Inputs/controls | Hooks/services/contexts |
| --- | --- | --- | --- | --- |
| `0.x` | root/app/admin foundational shells | status cards and baseline alerts | basic search/filter inputs | auth/session contexts and health service patterns |
| `1.x` | profile/billing activity areas | alerts, timeline rows | search input, filter select | auth context, usage hooks |
| `2.x` | jobs/results tabs | `JobsCard`, `ExecutionFlow` | progress indicators, retry buttons | jobs polling hooks |
| `6.x` | reliability views | charts, metric cards | checkbox/radio filters | observability services |
| `7.x` | admin audit tabs | log table, export panel | date range inputs, level checkboxes | role context + admin hooks |
| `8.x` | API analytics tabs | endpoint list and detail panel | key selector, endpoint filters | integration/API services |
| `10.x` | campaign compliance tabs | audit trail timeline | compliance checkbox list | campaign contexts/services |

## Surface-specific bindings

- **`contact360.io/root`**: reliability/trust messaging and status-linked narrative surfaces for logging-backed platform claims.
- **`contact360.io/app`**: operational views (jobs/reliability/admin analytics) using filters, checkboxes/radios, and progress/status components.
- **`contact360.io/admin`**: core audit/log governance with tabular log views, query filters, export controls, and role-gated operations.

## 2026 addendum

- Canonical backend contract is S3 CSV query/aggregate storage model.
- UI bindings should include `query`, `search`, `statistics`, and bulk-delete/admin moderation actions.
