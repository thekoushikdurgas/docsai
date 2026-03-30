# Appointment360 Era Task Pack Index

Quick-reference index linking each Contact360 era to its Appointment360 (`contact360.io/api`) task pack.

**Gateway task board:** Granular `✅/🟡/📌/⬜` tasks by era (verified against `app/graphql/schema.py` and clients) live in [APPOINTMENT360_GATEWAY_TASK_BOARD.md](APPOINTMENT360_GATEWAY_TASK_BOARD.md).

## Era task pack files

| Era | Theme | Task pack file |
| --- | --- | --- |
| `0.x` | Foundation | `docs/0. Foundation and pre-product stabilization and codebase setup/appointment360-foundation-task-pack.md` |
| `1.x` | User, Billing, Credit | `docs/1. Contact360 user and billing and credit system/` — patches `1.N.P — *.md` (**Service task slices**; former `appointment360-user-billing-task-pack.md` merged) |
| `2.x` | Email System | `docs/2. Contact360 email system/` — patches `2.N.P — *.md` (**Service task slices**; former `appointment360-email-system-task-pack.md` merged) |
| `3.x` | Contact & Company Data | `docs/3. Contact360 contact and company data system/` — patches `3.N.P — *.md` (**Service task slices**; former `appointment360-contact-company-task-pack.md` merged) |
| `4.x` | Extension & Sales Navigator | `docs/4. Contact360 Extension and Sales Navigator maturity/` — patches `4.N.P — *.md` (**Service task slices**; former `appointment360-extension-sn-task-pack.md` merged) |
| `5.x` | AI Workflows | `docs/5. Contact360 AI workflows/` — patches `5.N.P — *.md` (**Service task slices**; former `appointment360-ai-task-pack.md` merged) |
| `6.x` | Reliability & Scaling | `docs/6. Contact360 Reliability and Scaling/` — patches `6.N.P — *.md` (**Service task slices**; former `appointment360-reliability-scaling-task-pack.md` merged) |
| `7.x` | Deployment | `docs/7. Contact360 deployment/` — patches `7.N.P — *.md` (**Service task slices**; former `appointment360-deployment-task-pack.md` merged) |
| `8.x` | Public & Private APIs | `docs/8. Contact360 public and private apis and endpoints/` — patches `8.N.P — *.md` (**Micro-gate** + **Service task slices**; former `appointment360-api-endpoint-task-pack.md` merged) |
| `9.x` | Ecosystem & Productization | `docs/9. Contact360 Ecosystem integrations and Platform productization/` — patches `9.N.P — *.md` (**Micro-gate** + **Service task slices**; former `appointment360-ecosystem-productization-task-pack.md` merged) |
| `10.x` | Email Campaign | `docs/10. Contact360 email campaign/` — patches `10.N.P — *.md` (**Micro-gate** + **Service task slices**; former `appointment360-email-campaign-task-pack.md` merged) |

## GraphQL module-to-era activation map

`Mounted` means the namespace exists on root `Query` or `Mutation` in `contact360.io/api/app/graphql/schema.py`. Doc-only rows describe intended contracts before schema wiring.

| Module | Era activated | Mounted in schema | Module doc |
| --- | --- | --- | --- |
| `auth` | `0.x` | yes | `01_AUTH_MODULE.md` |
| `health` | `0.x` | yes | `08_HEALTH_MODULE.md` |
| `users` | `1.x` | yes | `02_USERS_MODULE.md` |
| `billing` | `1.x` | yes | `14_BILLING_MODULE.md` |
| `usage` | `1.x` | yes | `09_USAGE_MODULE.md` |
| `activities` | `1.x` | yes | `11_ACTIVITIES_MODULE.md` |
| `email` | `2.x` | yes | `15_EMAIL_MODULE.md` |
| `jobs` | `2.x` | yes | `16_JOBS_MODULE.md` |
| `upload` | `2.x` | yes | `10_UPLOAD_MODULE.md` |
| `contacts` | `3.x` | yes | `03_CONTACTS_MODULE.md` |
| `companies` | `3.x` | yes | `04_COMPANIES_MODULE.md` |
| `s3` | `3.x` | yes | `07_S3_MODULE.md` |
| `savedSearches` | `3.x` | yes | `26_SAVED_SEARCHES_MODULE.md` |
| `linkedin` | `4.x` | yes | `21_LINKEDIN_MODULE.md` |
| `salesNavigator` | `4.x` | yes | `23_SALES_NAVIGATOR_MODULE.md` |
| `aiChats` | `5.x` | yes | `17_AI_CHATS_MODULE.md` |
| `resume` | `5.x` | yes | `29_RESUME_AI_REST_SERVICE.md` |
| `analytics` | `6.x` | yes | `18_ANALYTICS_MODULE.md` |
| `admin` | `7.x` | yes | `13_ADMIN_MODULE.md` |
| `pages` | `8.x` | yes | `19_PAGES_MODULE.md` |
| `profile` | `8.x` | yes | `28_PROFILE_MODULE.md` |
| `twoFactor` | `8.x` | yes | `27_TWO_FACTOR_MODULE.md` |
| `notifications` | `9.x` | yes | `05_NOTIFICATIONS_MODULE.md` |
| `featureOverview` | `9.x` | yes | `09_USAGE_MODULE.md` (see `app/graphql/modules/usage/feature_overview.py`) |
| `webhooks` | `9.x` | **no** | `06_WEBHOOKS_MODULE.md` |
| `integrations` | `9.x` | **no** | `20_INTEGRATIONS_MODULE.md` |
| `campaigns` | `10.x` | **no** | `22_CAMPAIGNS_MODULE.md` |
| `sequences` | `10.x` | **no** | `24_SEQUENCES_MODULE.md` |
| `campaignTemplates` | `10.x` | **no** | `25_CAMPAIGN_TEMPLATES_MODULE.md` |

## Downstream client activation map

| Client | Era activated | Config key prefix |
| --- | --- | --- |
| `LambdaEmailClient` | `2.x` | `LAMBDA_EMAIL_API_*` |
| `TkdjobClient` | `2.x` | `TKDJOB_API_*` |
| `ConnectraClient` | `3.x` | `CONNECTRA_*` |
| `LambdaSalesNavigatorClient` | `4.x` | `LAMBDA_SN_API_*` |
| `LambdaAIClient` | `5.x` | `LAMBDA_AI_API_*` (proxies Contact AI REST; see `17_AI_CHATS_MODULE.md`) |
| `ResumeAIClient` | `5.x` | `RESUME_AI_*` |
| `LambdaS3StorageClient` | `3.x` | `LAMBDA_S3STORAGE_API_*` |
| `LambdaLogsClient` | `6.x` | `LAMBDA_LOGS_API_*` |
| `DocsAIClient` | `8.x` | `DOCSAI_*` |
| Email campaign HTTP client | `10.x` | **⬜ not implemented** — add settings + `app/clients/*` when mounting `campaigns` / `sequences` / `campaignTemplates` on the schema ([APPOINTMENT360_GATEWAY_TASK_BOARD.md](APPOINTMENT360_GATEWAY_TASK_BOARD.md)) |
