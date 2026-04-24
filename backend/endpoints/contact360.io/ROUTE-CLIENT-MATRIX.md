# GraphQL → HTTP client matrix (summary)

| GraphQL area | Client module | Env prefix |
|--------------|---------------|------------|
| contacts / companies / jobs (Connectra) | `connectra_client` | `CONNECTRA_` |
| email | `email_server_client` | `EMAIL_SERVER_` |
| phone | `phone_server_client` | `PHONE_SERVER_` |
| aiChats | `ai_client` | `AI_SERVER_` |
| s3 / upload | `s3storage_client` | `S3STORAGE_` |
| admin logs | `logs_client` | `LOGS_SERVER_` |
| salesNavigator | `sales_navigator_client` | `SALES_NAVIGATOR_` |
| campaignSatellite / mutations.campaigns | `campaign_service_client` | `CAMPAIGN_` |
| pages (DocsAI) | `docsai_client` | `DOCSAI_` |
| resume | `resume_ai_client` | `RESUME_AI_` |
| **hireSignal** (job.server) | `job_server_client` | `JOB_SERVER_` |

See `app/clients/` for method-level mapping.
