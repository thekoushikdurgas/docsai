#!/usr/bin/env python3
"""
Fill missing service_file and service_methods in media/endpoints/*.json
using appointment360 backend module/resolver mapping.
Run from repo root or docsai: python scripts/fill_endpoint_service_files.py [--write]
"""
import json
import re
import sys
from pathlib import Path

# Path from script to media/endpoints
SCRIPT_DIR = Path(__file__).resolve().parent
DOCSAI_ROOT = SCRIPT_DIR.parent
ENDPOINTS_DIR = DOCSAI_ROOT / "media" / "endpoints"

# (path without "graphql/", method) -> (module, file_type, resolver)
# file_type is "queries" or "mutations"
BACKEND_MAP = {
    # Auth
    ("Login", "MUTATION"): ("auth", "mutations", "login"),
    ("Register", "MUTATION"): ("auth", "mutations", "register"),
    ("Logout", "MUTATION"): ("auth", "mutations", "logout"),
    ("RefreshToken", "MUTATION"): ("auth", "mutations", "refresh_token"),
    ("GetMe", "QUERY"): ("auth", "queries", "me"),
    ("GetSession", "QUERY"): ("auth", "queries", "session"),
    # Users
    ("GetUser", "QUERY"): ("users", "queries", "user"),
    ("ListUsers", "QUERY"): ("users", "queries", "users"),
    ("UserStats", "QUERY"): ("users", "queries", "user_stats"),
    ("UpdateProfile", "MUTATION"): ("users", "mutations", "update_profile"),
    ("UploadAvatar", "MUTATION"): ("users", "mutations", "upload_avatar"),
    ("UpdateUser", "MUTATION"): ("users", "mutations", "update_user"),
    ("PromoteToAdmin", "MUTATION"): ("users", "mutations", "promote_to_admin"),
    ("PromoteToSuperAdmin", "MUTATION"): ("users", "mutations", "promote_to_super_admin"),
    # Admin
    ("GetUserStats", "QUERY"): ("admin", "queries", "userStats"),
    ("GetUserHistory", "QUERY"): ("admin", "queries", "userHistory"),
    ("QueryLogs", "QUERY"): ("admin", "queries", "logs"),
    ("SearchLogs", "QUERY"): ("admin", "queries", "searchLogs"),
    ("GetLogStatistics", "QUERY"): ("admin", "queries", "logStatistics"),
    ("UpdateUserRole", "MUTATION"): ("admin", "mutations", "updateUserRole"),
    ("UpdateUserCredits", "MUTATION"): ("admin", "mutations", "updateUserCredits"),
    ("DeleteUser", "MUTATION"): ("admin", "mutations", "deleteUser"),
    ("PromoteToAdmin", "MUTATION"): ("admin", "mutations", "promoteToAdmin"),
    ("PromoteToSuperAdmin", "MUTATION"): ("admin", "mutations", "promoteToSuperAdmin"),
    ("CreateLog", "MUTATION"): ("admin", "mutations", "createLog"),
    ("CreateLogsBatch", "MUTATION"): ("admin", "mutations", "createLogsBatch"),
    ("UpdateLog", "MUTATION"): ("admin", "mutations", "updateLog"),
    ("DeleteLog", "MUTATION"): ("admin", "mutations", "deleteLog"),
    ("DeleteLogsBulk", "MUTATION"): ("admin", "mutations", "deleteLogsBulk"),
    # Contacts
    ("GetContact", "QUERY"): ("contacts", "queries", "contact"),
    ("Contacts", "QUERY"): ("contacts", "queries", "contacts"),
    ("CountContacts", "QUERY"): ("contacts", "queries", "contactCount"),
    ("ContactQuery", "QUERY"): ("contacts", "queries", "contactQuery"),
    ("GetContactFilters", "QUERY"): ("contacts", "queries", "filters"),
    ("GetContactFilterData", "QUERY"): ("contacts", "queries", "filterData"),
    ("CreateContact", "MUTATION"): ("contacts", "mutations", "createContact"),
    ("UpdateContact", "MUTATION"): ("contacts", "mutations", "updateContact"),
    ("DeleteContact", "MUTATION"): ("contacts", "mutations", "deleteContact"),
    ("BatchCreateContacts", "MUTATION"): ("contacts", "mutations", "batchCreateContacts"),
    # Companies
    ("GetCompany", "QUERY"): ("companies", "queries", "company"),
    ("Companies", "QUERY"): ("companies", "queries", "companies"),
    ("CompanyQuery", "QUERY"): ("companies", "queries", "companyQuery"),
    ("CompanyCount", "QUERY"): ("companies", "queries", "companyCount"),
    ("GetCompanyContacts", "QUERY"): ("companies", "queries", "companyContacts"),
    ("GetCompanyFilters", "QUERY"): ("companies", "queries", "filters"),
    ("GetCompanyFilterData", "QUERY"): ("companies", "queries", "filterData"),
    ("CreateCompany", "MUTATION"): ("companies", "mutations", "createCompany"),
    ("UpdateCompany", "MUTATION"): ("companies", "mutations", "updateCompany"),
    ("DeleteCompany", "MUTATION"): ("companies", "mutations", "deleteCompany"),
    # Jobs
    ("ListJobs", "QUERY"): ("jobs", "queries", "jobs"),
    ("GetUploadUrl", "QUERY"): ("jobs", "queries", "uploadUrl"),
    ("GetJob", "QUERY"): ("jobs", "queries", "job"),
    ("GetExportDownloadUrl", "QUERY"): ("jobs", "queries", "exportDownloadUrl"),
    ("CreateJob", "MUTATION"): ("jobs", "mutations", "createJob"),
    ("CreateExportJob", "MUTATION"): ("jobs", "mutations", "createExportJob"),
    # Imports
    ("ListImportJobs", "QUERY"): ("imports", "queries", "importJobs"),
    ("GetImportJob", "QUERY"): ("imports", "queries", "importJob"),
    ("CreateImportJob", "MUTATION"): ("imports", "mutations", "createImportJob"),
    # Activities
    ("GetActivities", "QUERY"): ("activities", "queries", "activities"),
    ("GetActivityStats", "QUERY"): ("activities", "queries", "activityStats"),
    # Analytics
    ("GetPerformanceMetrics", "QUERY"): ("analytics", "queries", "performanceMetrics"),
    ("AggregateMetrics", "QUERY"): ("analytics", "queries", "aggregateMetrics"),
    ("SubmitPerformanceMetric", "MUTATION"): ("analytics", "mutations", "submitPerformanceMetric"),
    # Billing
    ("GetBilling", "QUERY"): ("billing", "queries", "billing"),
    ("GetPlans", "QUERY"): ("billing", "queries", "plans"),
    ("GetAddons", "QUERY"): ("billing", "queries", "addons"),
    ("GetInvoices", "QUERY"): ("billing", "queries", "invoices"),
    ("Subscribe", "MUTATION"): ("billing", "mutations", "subscribe"),
    ("PurchaseAddon", "MUTATION"): ("billing", "mutations", "purchaseAddon"),
    ("CancelSubscription", "MUTATION"): ("billing", "mutations", "cancelSubscription"),
    ("CreatePlan", "MUTATION"): ("billing", "mutations", "createPlan"),
    ("UpdatePlan", "MUTATION"): ("billing", "mutations", "updatePlan"),
    ("DeletePlan", "MUTATION"): ("billing", "mutations", "deletePlan"),
    ("CreatePlanPeriod", "MUTATION"): ("billing", "mutations", "createPlanPeriod"),
    ("UpdatePlanPeriod", "MUTATION"): ("billing", "mutations", "updatePlanPeriod"),
    ("DeletePlanPeriod", "MUTATION"): ("billing", "mutations", "deletePlanPeriod"),
    ("CreateAddon", "MUTATION"): ("billing", "mutations", "createAddon"),
    ("UpdateAddon", "MUTATION"): ("billing", "mutations", "updateAddon"),
    ("DeleteAddon", "MUTATION"): ("billing", "mutations", "deleteAddon"),
    # Email
    ("FindEmails", "QUERY"): ("email", "queries", "findEmails"),
    ("FindSingleEmail", "MUTATION"): ("email", "queries", "findEmails"),  # may be query in docs
    ("VerifySingleEmail", "MUTATION"): ("email", "queries", "verifySingleEmail"),
    ("VerifyBulkEmails", "MUTATION"): ("email", "queries", "verifyEmailsBulk"),
    ("VerifyAndFind", "MUTATION"): ("email", "queries", "verifyexportEmail"),
    ("ExportEmails", "MUTATION"): ("email", "queries", "exportEmails"),
    ("VerifyEmailsBulk", "QUERY"): ("email", "queries", "verifyEmailsBulk"),
    ("VerifySingleEmail", "QUERY"): ("email", "queries", "verifySingleEmail"),
    # Exports
    ("GetExport", "QUERY"): ("exports", "queries", "export"),
    ("ListExports", "QUERY"): ("exports", "queries", "exports"),
    ("GetExportStatus", "QUERY"): ("exports", "queries", "exportStatus"),
    ("GetExportByJobUuid", "QUERY"): ("exports", "queries", "exportByJobUuid"),
    ("CreateContactExport", "MUTATION"): ("exports", "mutations", "createContactExport"),
    ("CreateCompanyExport", "MUTATION"): ("exports", "mutations", "createCompanyExport"),
    # Usage
    ("GetUsage", "QUERY"): ("usage", "queries", "usage"),
    ("TrackUsage", "MUTATION"): ("usage", "mutations", "trackUsage"),
    ("ResetUsage", "MUTATION"): ("usage", "mutations", "resetUsage"),
    # Upload
    ("GetUploadStatus", "QUERY"): ("upload", "queries", "uploadStatus"),
    ("GetPresignedUrl", "QUERY"): ("upload", "queries", "presignedUrl"),
    ("InitiateUpload", "MUTATION"): ("upload", "mutations", "initiateUpload"),
    ("RegisterPart", "MUTATION"): ("upload", "mutations", "registerPart"),
    ("CompleteUpload", "MUTATION"): ("upload", "mutations", "completeUpload"),
    ("AbortUpload", "MUTATION"): ("upload", "mutations", "abortUpload"),
    # S3
    ("ListS3Files", "QUERY"): ("s3", "queries", "s3Files"),
    ("GetS3FileData", "QUERY"): ("s3", "queries", "s3FileData"),
    ("GetS3FileInfo", "QUERY"): ("s3", "queries", "s3FileInfo"),
    ("GetS3FilePresignedUrl", "QUERY"): ("s3", "queries", "s3FileDownloadUrl"),
    ("GetS3FileDownloadUrl", "QUERY"): ("s3", "queries", "s3FileDownloadUrl"),
    # AI Chats
    ("ListAIChats", "QUERY"): ("ai_chats", "queries", "aiChats"),
    ("GetAIChat", "QUERY"): ("ai_chats", "queries", "aiChat"),
    ("CreateAIChat", "MUTATION"): ("ai_chats", "mutations", "createAIChat"),
    ("UpdateAIChat", "MUTATION"): ("ai_chats", "mutations", "updateAIChat"),
    ("DeleteAIChat", "MUTATION"): ("ai_chats", "mutations", "deleteAIChat"),
    ("SendMessage", "MUTATION"): ("ai_chats", "mutations", "sendMessage"),
    ("AnalyzeEmailRisk", "MUTATION"): ("ai_chats", "mutations", "analyzeEmailRisk"),
    ("GenerateCompanySummary", "MUTATION"): ("ai_chats", "mutations", "generateCompanySummary"),
    ("ParseContactFilters", "MUTATION"): ("ai_chats", "mutations", "parseContactFilters"),
    ("ParseFilters", "MUTATION"): ("ai_chats", "mutations", "parseContactFilters"),
    # Notifications
    ("ListNotifications", "QUERY"): ("notifications", "queries", "notifications"),
    ("GetNotification", "QUERY"): ("notifications", "queries", "notification"),
    ("GetUnreadCount", "QUERY"): ("notifications", "queries", "unreadCount"),
    ("GetNotificationPreferences", "QUERY"): ("notifications", "queries", "notificationPreferences"),
    ("MarkNotificationAsRead", "MUTATION"): ("notifications", "mutations", "markNotificationAsRead"),
    ("MarkNotificationsAsRead", "MUTATION"): ("notifications", "mutations", "markNotificationsAsRead"),
    ("DeleteNotifications", "MUTATION"): ("notifications", "mutations", "deleteNotifications"),
    ("UpdateNotificationPreferences", "MUTATION"): ("notifications", "mutations", "updateNotificationPreferences"),
    ("UpdatePreferences", "MUTATION"): ("notifications", "mutations", "updateNotificationPreferences"),
    # Sales Navigator
    ("SalesNavigatorRecords", "QUERY"): ("sales_navigator", "queries", "salesNavigatorRecords"),
    ("SaveSalesNavigatorProfiles", "MUTATION"): ("sales_navigator", "mutations", "saveSalesNavigatorProfiles"),
    # Saved Searches
    ("ListSavedSearches", "QUERY"): ("saved_searches", "queries", "listSavedSearches"),
    ("GetSavedSearch", "QUERY"): ("saved_searches", "queries", "getSavedSearch"),
    ("CreateSavedSearch", "MUTATION"): ("saved_searches", "mutations", "createSavedSearch"),
    ("UpdateSavedSearch", "MUTATION"): ("saved_searches", "mutations", "updateSavedSearch"),
    ("DeleteSavedSearch", "MUTATION"): ("saved_searches", "mutations", "deleteSavedSearch"),
    ("UpdateSavedSearchUsage", "MUTATION"): ("saved_searches", "mutations", "updateSavedSearchUsage"),
    # Two-Factor
    ("Get2FAStatus", "QUERY"): ("two_factor", "queries", "get2FAStatus"),
    ("Setup2FA", "MUTATION"): ("two_factor", "mutations", "setup2FA"),
    ("Verify2FA", "MUTATION"): ("two_factor", "mutations", "verify2FA"),
    ("Disable2FA", "MUTATION"): ("two_factor", "mutations", "disable2FA"),
    ("RegenerateBackupCodes", "MUTATION"): ("two_factor", "mutations", "regenerateBackupCodes"),
    # Profile
    ("ListAPIKeys", "QUERY"): ("profile", "queries", "listAPIKeys"),
    ("ListSessions", "QUERY"): ("profile", "queries", "listSessions"),
    ("ListTeamMembers", "QUERY"): ("profile", "queries", "listTeamMembers"),
    ("CreateAPIKey", "MUTATION"): ("profile", "mutations", "createAPIKey"),
    ("DeleteAPIKey", "MUTATION"): ("profile", "mutations", "deleteAPIKey"),
    ("RevokeSession", "MUTATION"): ("profile", "mutations", "revokeSession"),
    ("RevokeAllOtherSessions", "MUTATION"): ("profile", "mutations", "revokeAllOtherSessions"),
    ("InviteTeamMember", "MUTATION"): ("profile", "mutations", "inviteTeamMember"),
    ("UpdateTeamMemberRole", "MUTATION"): ("profile", "mutations", "updateTeamMemberRole"),
    ("RemoveTeamMember", "MUTATION"): ("profile", "mutations", "removeTeamMember"),
    # Health
    ("GetApiMetadata", "QUERY"): ("health", "queries", "apiMetadata"),
    ("GetHealth", "QUERY"): ("health", "queries", "apiHealth"),
    ("GetVqlHealth", "QUERY"): ("health", "queries", "vqlHealth"),
    ("GetVqlStats", "QUERY"): ("health", "queries", "vqlStats"),
    ("GetPerformanceStats", "QUERY"): ("health", "queries", "performanceStats"),
    ("ApiMetadata", "QUERY"): ("health", "queries", "apiMetadata"),
    ("ApiHealth", "QUERY"): ("health", "queries", "apiHealth"),
    ("VqlHealth", "QUERY"): ("health", "queries", "vqlHealth"),
    ("VqlStats", "QUERY"): ("health", "queries", "vqlStats"),
    ("PerformanceStats", "QUERY"): ("health", "queries", "performanceStats"),
    ("GetVQLHealth", "QUERY"): ("health", "queries", "vqlHealth"),
    ("GetVQLStats", "QUERY"): ("health", "queries", "vqlStats"),
    # LinkedIn
    ("SearchByLinkedInUrl", "MUTATION"): ("linkedin", "mutations", "search"),
    ("ExportLinkedIn", "MUTATION"): ("linkedin", "mutations", "exportLinkedInResults"),
    ("UpsertByLinkedInUrl", "MUTATION"): ("linkedin", "mutations", "upsertByLinkedInUrl"),
    # Pages (DocsAI)
    ("GetDashboardPage", "QUERY"): ("pages", "queries", "page"),
    ("ListDashboardPages", "QUERY"): ("pages", "queries", "dashboardPages"),
    ("CreateDashboardPage", "MUTATION"): ("pages", "queries", "page"),
    ("UpdateDashboardPage", "MUTATION"): ("pages", "queries", "page"),
    ("DeleteDashboardPage", "MUTATION"): ("pages", "queries", "page"),
    ("GetDocumentationPage", "QUERY"): ("pages", "queries", "page"),
    ("ListDocumentationPages", "QUERY"): ("pages", "queries", "pages"),
    ("GetDocumentationContent", "QUERY"): ("pages", "queries", "pageContent"),
    ("CreateDocumentationPage", "MUTATION"): ("pages", "queries", "page"),
    ("UpdateDocumentationPage", "MUTATION"): ("pages", "queries", "page"),
    ("DeleteDocumentationPage", "MUTATION"): ("pages", "queries", "page"),
    ("GetMarketingPage", "QUERY"): ("pages", "queries", "page"),
    ("ListMarketingPages", "QUERY"): ("pages", "queries", "marketingPages"),
    ("CreateMarketingPage", "MUTATION"): ("pages", "queries", "page"),
    ("UpdateMarketingPage", "MUTATION"): ("pages", "queries", "page"),
    ("DeleteMarketingPage", "MUTATION"): ("pages", "queries", "page"),
    ("PublishMarketingPage", "MUTATION"): ("pages", "queries", "page"),
    ("AdminMarketingPages", "QUERY"): ("pages", "queries", "dashboardPages"),
    ("CancelExport", "MUTATION"): ("exports", "mutations", "createContactExport"),  # may be different
}

# Aliases: endpoint_path in docs may differ slightly
ALIASES = {
    "GetAdminPlans": "GetPlans",
    "GetAdminAddons": "GetAddons",
    "ListScrapingRecords": "ListJobs",
}


def op_from_path(endpoint_path: str) -> str:
    """Extract operation name from endpoint_path (e.g. graphql/GetUserStats -> GetUserStats)."""
    if not endpoint_path:
        return ""
    return endpoint_path.replace("graphql/", "").strip()


def lookup_backend(endpoint_path: str, method: str) -> tuple[str, str, str] | None:
    """Return (module, file_type, resolver) or None."""
    op = op_from_path(endpoint_path)
    op = ALIASES.get(op, op)
    key = (op, method)
    if key in BACKEND_MAP:
        return BACKEND_MAP[key]
    return None


def main() -> None:
    write = "--write" in sys.argv
    if not ENDPOINTS_DIR.is_dir():
        print(f"Endpoints dir not found: {ENDPOINTS_DIR}")
        sys.exit(1)

    updated = 0
    skipped = 0
    no_map = []

    for path in sorted(ENDPOINTS_DIR.glob("*.json")):
        if path.name in ("index.json", "endpoints_index.json"):
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Skip {path.name}: {e}")
            continue

        endpoint_id = data.get("endpoint_id", "")
        endpoint_path = data.get("endpoint_path", "")
        method = data.get("method", "QUERY")

        if data.get("service_file"):
            skipped += 1
            continue

        backend = lookup_backend(endpoint_path, method)
        if not backend:
            no_map.append((path.name, endpoint_path, method))
            continue

        module, file_type, resolver = backend
        service_file = f"appointment360/app/graphql/modules/{module}/{file_type}.py"
        data["service_file"] = service_file
        existing_methods = data.get("service_methods") or []
        if resolver not in existing_methods:
            data["service_methods"] = existing_methods + [resolver] if existing_methods else [resolver]

        if write:
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(f"Updated {path.name} -> {service_file} [{resolver}]")
        else:
            print(f"[DRY-RUN] Would set {path.name} -> {service_file} [{resolver}]")
        updated += 1

    print(f"\nUpdated: {updated}, Skipped (had service_file): {skipped}, No mapping: {len(no_map)}")
    if no_map:
        print("No mapping for:")
        for fn, ep, m in no_map[:30]:
            print(f"  {fn}  {ep}  {m}")
        if len(no_map) > 30:
            print(f"  ... and {len(no_map) - 30} more")
    if not write and updated:
        print("\nRun with --write to apply changes.")


if __name__ == "__main__":
    main()
