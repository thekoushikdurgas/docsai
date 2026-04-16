# Ownership split

| Data | Owner |
|------|--------|
| CRM phone fields, lead scores | Contact360 DB + sync.server as configured |
| Bulk verify / S3 jobs / job rows | **phone.server** (`phoneapi_jobs` + Redis) |

Use satellite output as enrichment input to the CRM; do not treat `phoneapi_jobs` as the CRM system of record.
