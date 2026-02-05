# Endpoints vs Backend Audit

Generated from `endpoints_index.json` and `lambda/appointment360` GraphQL modules.

- **Documented endpoint files:** 156 (see `media/endpoints/index.json`)
- **Documented endpoint paths:** 154
- **Backend ops in this audit:** 128
- **Documented (matched):** 128
- **Missing docs (in audit, no matching path):** 0

## Documented path names (sample)

```
AbortUpload
AdminMarketingPages
AggregateMetrics
AnalyzeEmailRisk
CancelExport
CancelSubscription
CompleteUpload
CountContacts
CreateAIChat
CreateAPIKey
CreateAddon
CreateCompany
CreateCompanyExport
CreateContact
CreateContactExport
CreateDashboardPage
CreateDocumentationPage
CreateExportJob
CreateImportJob
CreateJob
CreateLog
CreateLogsBatch
CreateMarketingPage
CreatePlan
CreatePlanPeriod
CreateSavedSearch
DeleteAIChat
DeleteAPIKey
DeleteAddon
DeleteCompany
DeleteContact
DeleteDashboardPage
DeleteDocumentationPage
DeleteLog
DeleteLogsBulk
DeleteMarketingPage
DeleteNotifications
DeletePlan
DeletePlanPeriod
DeleteSavedSearch
DeleteUser
Disable2FA
ExportEmails
ExportLinkedIn
FindEmails
FindSingleEmail
GenerateAndVerify
GenerateCompanySummary
Get2FAStatus
GetAIChat
...
```

## Backend ops with no matching documented path

None (all audited ops have a documented path).

## service_file alignment

- Endpoints with **no service_file** (null/empty): 0


- Endpoints where **service_file** does not reference `appointment360`: 0

  None (all have appointment360 in service_file or use router_file only).

## Recent changes

- **service_file fill:** All 66 endpoints that had null `service_file` were filled via `scripts/fill_endpoint_service_files.py` (mapping path+method → appointment360 module/resolver). `scripts/normalize_endpoints_to_spec.py` was run to validate `used_by_pages` and regenerate `index.json` and `endpoints_index.json`.

## Notes

- Backend has additional operations (e.g. pages.*, email.*) not all mapped here.
- Some backend methods may map to the same doc (e.g. admin.users and users.users → ListUsers).
- Run this script after updating endpoints to refresh the report.
