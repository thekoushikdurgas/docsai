# jobs UI bindings

## Purpose
Map GraphQL **`jobs`** (gateway + `scheduler_jobs`) to dashboard surfaces including pages, tabs, components, inputs/controls, hooks, contexts, and end-to-end execution flow. Work runs on **email.server** and **sync.server**, not a separate `contact360.io/jobs` service.

## Binding matrix
| Era | Pages/tabs | Components | Inputs/controls | Hooks/services/contexts |
| --- | --- | --- | --- | --- |
| `0.x` | baseline dashboard shell | `JobsCard`, `JobsPipelineStats` (stub) | basic action buttons | auth/app contexts + base API service |
| `1.x` | billing + usage pages with job activity touchpoints | `JobsTable`, `JobsRetryModal` | retry button, confirmation checkbox | billing/usage hooks + jobs query hooks |
| `2.x` | email finder/verifier bulk tabs | `ScheduleJobModal`, `FilesUploadModal`, `JobsCardExpandPanel` | file selectors, mapping checkboxes, retry radio inputs, progress bars | email hooks + jobs service bridge |
| `3.x` | contacts/companies import-export tabs | `ExecutionFlow`, `JobDetailsModal`, `DataInspector` | VQL input, filter inputs, run/retry controls | contacts/companies hooks + GraphQL jobs module |
| `4.x` | extension/SN ingestion views | sync status cards, ingestion timeline widgets | sync toggles, retry controls | extension services + jobs status polling |
| `5.x` | AI workflows tab | AI batch cards + execution detail panels | model selector, confidence threshold inputs | AI workflow hooks + jobs orchestration service |
| `6.x` | reliability tab | queue health cards, failure heatmaps | SLO filters, retry/dead-letter controls | observability hooks + metrics services |
| `7.x` | admin governance tab | audit timeline panel, retention cards | date filters, role filters, compliance checkboxes | admin contexts + jobs timeline API |
| `8.x` | API/integrations tab | webhook setup cards, API contract panels | key selectors, callback URL inputs | partner API services + jobs callbacks |
| `9.x` | ecosystem/productization tab | tenant quota cards, entitlement panels | tenant selector, quota controls | tenant contexts + quota services |
| `10.x` | campaign workflow tabs | campaign execution panel, compliance evidence modal | audience selectors, approval checkbox, progress trackers | campaign services + jobs timeline/status hooks |

## Surface components tracked

- `JobsTable`
- `JobsCard`
- `JobsCardExpandPanel`
- `JobDetailsModal`
- `ExecutionFlow`
- `ScheduleJobModal`
- `JobsRetryModal`
- `JobsPipelineStats`
- `DataInspector`
- `FilesUploadModal`

## End-to-end binding graph

`UI component -> Hook -> GraphQL jobs module -> EmailServerJobsClient / ConnectraClient -> email.server or sync.server HTTP APIs -> worker queues -> Postgres/S3/OpenSearch`
