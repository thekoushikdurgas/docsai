#!/usr/bin/env python3
"""
Audit documented GraphQL endpoints (media/endpoints) against backend operations
(lambda/appointment360/app/graphql/modules). Loads endpoints_index.json and
reports documented path names vs a static list of backend (root, method) -> expected path.
"""
from pathlib import Path

ENDPOINTS_INDEX = Path(__file__).resolve().parent.parent / "media" / "endpoints" / "endpoints_index.json"
AUDIT_REPORT = Path(__file__).resolve().parent.parent / "media" / "ENDPOINTS_AUDIT.md"

# Backend (root, method) -> expected endpoint_path suffix (graphql/XXX)
# Built from lambda/appointment360 app/graphql/modules *queries.py and *mutations.py
BACKEND_OPS = [
    # Queries - activities
    ("activities", "activities", "GetActivities"),
    ("activities", "activityStats", "GetActivityStats"),
    # Queries - admin
    ("admin", "users", "ListUsers"),
    ("admin", "userStats", "GetUserStats"),
    ("admin", "userHistory", "GetUserHistory"),
    ("admin", "logStatistics", "GetLogStatistics"),
    ("admin", "logs", "QueryLogs"),
    ("admin", "searchLogs", "SearchLogs"),
    # Queries - auth
    ("auth", "me", "GetMe"),
    ("auth", "session", "GetSession"),
    # Queries - billing
    ("billing", "billing", "GetBilling"),
    ("billing", "plans", "GetPlans"),
    ("billing", "addons", "GetAddons"),
    ("billing", "invoices", "GetInvoices"),
    # Queries - contacts
    ("contacts", "contact", "GetContact"),
    ("contacts", "contacts", "QueryContacts"),
    ("contacts", "contactCount", "CountContacts"),
    ("contacts", "filters", "GetContactFilters"),
    # Queries - companies
    ("companies", "company", "GetCompany"),
    ("companies", "companies", "QueryCompanies"),
    ("companies", "companyContacts", "GetCompanyContacts"),
    ("companies", "filters", "GetCompanyFilters"),
    # Queries - exports
    ("exports", "export", "GetExport"),
    ("exports", "exports", "ListExports"),
    # Queries - health
    ("health", "apiMetadata", "GetAPIMetadata"),
    ("health", "apiHealth", "GetHealth"),
    ("health", "vqlHealth", "GetVQLHealth"),
    ("health", "vqlStats", "GetVQLStats"),
    ("health", "performanceStats", "GetPerformanceMetrics"),
    # Queries - usage, upload, jobs
    ("usage", "usage", "GetUsage"),
    ("upload", "uploadStatus", "GetUploadStatus"),
    ("upload", "presignedUrl", "GetPresignedUrl"),
    ("jobs", "jobs", "ListJobs"),
    ("jobs", "job", "GetJob"),
    ("jobs", "uploadUrl", "GetUploadUrl"),
    ("jobs", "exportDownloadUrl", "GetExportDownloadUrl"),
    # Queries - users
    ("users", "user", "GetUser"),
    ("users", "users", "ListUsers"),
    # Queries - saved_searches, profile, notifications, two_factor
    ("saved_searches", "listSavedSearches", "ListSavedSearches"),
    ("saved_searches", "getSavedSearch", "GetSavedSearch"),
    ("profile", "listAPIKeys", "ListAPIKeys"),
    ("profile", "listSessions", "ListSessions"),
    ("profile", "listTeamMembers", "ListTeamMembers"),
    ("notifications", "notifications", "ListNotifications"),
    ("notifications", "notification", "GetNotification"),
    ("notifications", "unreadCount", "GetUnreadCount"),
    ("two_factor", "get2FAStatus", "Get2FAStatus"),
    # Queries - ai_chats, s3, analytics, sales_navigator, imports
    ("ai_chats", "aiChats", "ListAIChats"),
    ("ai_chats", "aiChat", "GetAIChat"),
    ("s3", "s3Files", "ListS3Files"),
    ("s3", "s3FileData", "GetS3FileData"),
    ("s3", "s3FileDownloadUrl", "GetS3FileDownloadUrl"),
    ("analytics", "performanceMetrics", "GetPerformanceMetrics"),
    ("analytics", "aggregateMetrics", "AggregateMetrics"),
    ("sales_navigator", "salesNavigatorRecords", "ListScrapingRecords"),
    ("imports", "importJobs", "ListImportJobs"),
    ("imports", "importJob", "GetImportJob"),
    # Queries - email (subset)
    ("email", "findEmails", "FindEmails"),
    ("email", "verifySingleEmail", "VerifySingleEmail"),
    ("email", "verifyEmailsBulk", "VerifyBulkEmails"),
    ("email", "exportEmails", "ExportEmails"),
    # Queries - pages (subset that we document)
    ("pages", "dashboardPages", "ListDashboardPages"),
    ("pages", "marketingPages", "ListMarketingPages"),
    ("pages", "page", "GetDashboardPage"),  # or GetDocumentationPage / GetMarketingPage by type
    ("pages", "pageContent", "GetDocumentationContent"),
    # Mutations - auth, profile, admin, etc. (subset)
    ("auth", "login", "Login"),
    ("auth", "register", "Register"),
    ("auth", "logout", "Logout"),
    ("auth", "refresh_token", "RefreshToken"),
    ("admin", "updateUserRole", "UpdateUserRole"),
    ("admin", "updateUserCredits", "UpdateUserCredits"),
    ("admin", "deleteUser", "DeleteUser"),
    ("admin", "promoteToAdmin", "PromoteToAdmin"),
    ("admin", "promoteToSuperAdmin", "PromoteToSuperAdmin"),
    ("admin", "createLog", "CreateLog"),
    ("admin", "createLogsBatch", "CreateLogsBatch"),
    ("admin", "updateLog", "UpdateLog"),
    ("admin", "deleteLog", "DeleteLog"),
    ("admin", "deleteLogsBulk", "DeleteLogsBulk"),
    ("profile", "createAPIKey", "CreateAPIKey"),
    ("profile", "deleteAPIKey", "DeleteAPIKey"),
    ("profile", "revokeSession", "RevokeSession"),
    ("saved_searches", "createSavedSearch", "CreateSavedSearch"),
    ("saved_searches", "updateSavedSearch", "UpdateSavedSearch"),
    ("saved_searches", "deleteSavedSearch", "DeleteSavedSearch"),
    ("two_factor", "setup2FA", "Setup2FA"),
    ("two_factor", "verify2FA", "Verify2FA"),
    ("two_factor", "disable2FA", "Disable2FA"),
    ("two_factor", "regenerateBackupCodes", "RegenerateBackupCodes"),
    ("companies", "createCompany", "CreateCompany"),
    ("companies", "updateCompany", "UpdateCompany"),
    ("companies", "deleteCompany", "DeleteCompany"),
    ("contacts", "createContact", "CreateContact"),
    ("contacts", "updateContact", "UpdateContact"),
    ("contacts", "deleteContact", "DeleteContact"),
    ("exports", "createContactExport", "CreateContactExport"),
    ("exports", "createCompanyExport", "CreateCompanyExport"),
    ("imports", "createImportJob", "CreateImportJob"),
    ("billing", "subscribe", "Subscribe"),
    ("billing", "purchaseAddon", "PurchaseAddon"),
    ("billing", "cancelSubscription", "CancelSubscription"),
    ("upload", "initiateUpload", "InitiateUpload"),
    ("upload", "registerPart", "RegisterPart"),
    ("upload", "completeUpload", "CompleteUpload"),
    ("upload", "abortUpload", "AbortUpload"),
    ("usage", "trackUsage", "TrackUsage"),
    ("usage", "resetUsage", "ResetUsage"),
    ("analytics", "submitPerformanceMetric", "SubmitMetric"),
    ("ai_chats", "createAIChat", "CreateAIChat"),
    ("ai_chats", "updateAIChat", "UpdateAIChat"),
    ("ai_chats", "deleteAIChat", "DeleteAIChat"),
    ("ai_chats", "sendMessage", "SendMessage"),
    ("ai_chats", "analyzeEmailRisk", "AnalyzeEmailRisk"),
    ("ai_chats", "generateCompanySummary", "GenerateCompanySummary"),
    ("ai_chats", "parseContactFilters", "ParseFilters"),
    ("users", "update_profile", "UpdateProfile"),
    ("users", "upload_avatar", "UploadAvatar"),
    ("users", "promote_to_admin", "PromoteToAdmin"),
    ("users", "promote_to_super_admin", "PromoteToSuperAdmin"),
    ("jobs", "createJob", "CreateJob"),
    ("jobs", "createExportJob", "CreateExportJob"),
    ("notifications", "markNotificationAsRead", "MarkNotificationAsRead"),
    ("notifications", "deleteNotifications", "DeleteNotifications"),
    ("notifications", "updateNotificationPreferences", "UpdatePreferences"),
    ("linkedin", "search", "SearchLinkedIn"),
    ("linkedin", "exportLinkedInResults", "ExportLinkedIn"),
    ("linkedin", "upsertByLinkedInUrl", "UpsertByLinkedInUrl"),
    ("sales_navigator", "saveSalesNavigatorProfiles", "SaveSalesNavigatorProfiles"),
]


def load_documented_paths():
    """Return set of endpoint_path suffixes (e.g. 'GetActivities') from endpoints_index.json."""
    if not ENDPOINTS_INDEX.exists():
        return set()
    import json
    data = json.loads(ENDPOINTS_INDEX.read_text(encoding="utf-8"))
    paths = set()
    for ep in data.get("endpoints", []):
        p = ep.get("endpoint_path") or ""
        if p.startswith("graphql/"):
            paths.add(p.replace("graphql/", "", 1))
    return paths


def load_endpoints_index():
    """Load full endpoints list from endpoints_index.json."""
    if not ENDPOINTS_INDEX.exists():
        return []
    import json
    data = json.loads(ENDPOINTS_INDEX.read_text(encoding="utf-8"))
    return data.get("endpoints", [])


def run_service_file_check():
    """List endpoints where service_file is null or doesn't reference appointment360."""
    endpoints = load_endpoints_index()
    no_service = []
    no_appointment360 = []
    for ep in endpoints:
        sf = ep.get("service_file")
        eid = ep.get("endpoint_id", "")
        path_val = ep.get("endpoint_path", "")
        if not sf or (isinstance(sf, str) and not sf.strip()):
            no_service.append((eid, path_val))
        elif "appointment360" not in (sf or ""):
            no_appointment360.append((eid, path_val, sf))
    return no_service, no_appointment360


def run_audit():
    doc_paths = load_documented_paths()
    missing = []
    documented = []
    for root, method, expected in BACKEND_OPS:
        if expected in doc_paths:
            documented.append((root, method, expected))
        else:
            missing.append((root, method, expected))

    no_service, no_appointment360 = run_service_file_check()

    lines = [
        "# Endpoints vs Backend Audit",
        "",
        f"Generated from `endpoints_index.json` and `lambda/appointment360` GraphQL modules.",
        "",
        f"- **Documented endpoint paths:** {len(doc_paths)}",
        f"- **Backend ops in this audit:** {len(BACKEND_OPS)}",
        f"- **Documented (matched):** {len(documented)}",
        f"- **Missing docs (in audit, no matching path):** {len(missing)}",
        "",
        "## Documented path names (sample)",
        "",
        "```",
        "\n".join(sorted(doc_paths)[:50]) + ("\n..." if len(doc_paths) > 50 else ""),
        "```",
        "",
        "## Backend ops with no matching documented path",
        "",
    ]
    if missing:
        for root, method, expected in sorted(missing, key=lambda x: (x[0], x[1])):
            lines.append(f"- `{root}.{method}` → expected path: `graphql/{expected}`")
    else:
        lines.append("None (all audited ops have a documented path).")

    lines.extend([
        "",
        "## service_file alignment",
        "",
        f"- Endpoints with **no service_file** (null/empty): {len(no_service)}",
        "",
    ])
    if no_service:
        for eid, p in no_service[:20]:
            lines.append(f"  - `{eid}` ({p})")
        if len(no_service) > 20:
            lines.append(f"  - ... and {len(no_service) - 20} more")
    lines.extend([
        "",
        f"- Endpoints where **service_file** does not reference `appointment360`: {len(no_appointment360)}",
        "",
    ])
    if no_appointment360:
        for eid, p, sf in no_appointment360[:10]:
            lines.append(f"  - `{eid}` → `{sf}`")
        if len(no_appointment360) > 10:
            lines.append(f"  - ... and {len(no_appointment360) - 10} more")
    else:
        lines.append("  None (all have appointment360 in service_file or use router_file only).")

    lines.extend([
        "",
        "## Notes",
        "",
        "- Backend has additional operations (e.g. pages.*, email.*) not all mapped here.",
        "- Some backend methods may map to the same doc (e.g. admin.users and users.users → ListUsers).",
        "- Run this script after updating endpoints to refresh the report.",
        "",
    ])
    AUDIT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {AUDIT_REPORT} (missing: {len(missing)}, no_service_file: {len(no_service)}, no_appointment360: {len(no_appointment360)})")
    return missing


if __name__ == "__main__":
    run_audit()
