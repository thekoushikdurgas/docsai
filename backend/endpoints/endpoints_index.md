---
title: "Endpoints master index (aggregated)"
source_json: endpoints_index.json
generator: json_to_markdown_endpoints.py
---

# Endpoints master index

- **version:** 2.1
- **last_updated:** 2026-03-28T12:00:00.000000+00:00
- **total:** 173

## EC2 Go HTTP inventory (non-GraphQL satellites)

- [EC2_GO_SATELLITE_ROUTES.md](EC2_GO_SATELLITE_ROUTES.md) — Gin services under `EC2/*.server/`; linked from relevant era matrices below.

## Supplemental indexes (era matrices)

- [s3storage_endpoint_era_matrix](s3storage_endpoint_era_matrix.md) — `s3storage_endpoint_era_matrix.json`
- [logsapi_endpoint_era_matrix](logsapi_endpoint_era_matrix.md) — `logsapi_endpoint_era_matrix.json`
- [emailapis_endpoint_era_matrix](emailapis_endpoint_era_matrix.md) — `emailapis_endpoint_era_matrix.json`
- [connectra_endpoint_era_matrix](connectra_endpoint_era_matrix.md) — `connectra_endpoint_era_matrix.json`
- [jobs_endpoint_era_matrix](jobs_endpoint_era_matrix.md) — `jobs_endpoint_era_matrix.json`
- [emailcampaign_endpoint_era_matrix](emailcampaign_endpoint_era_matrix.md) — `emailcampaign_endpoint_era_matrix.json`
- [appointment360_endpoint_era_matrix](appointment360_endpoint_era_matrix.md) — `appointment360_endpoint_era_matrix.json`
- [mailvetter_endpoint_era_matrix](mailvetter_endpoint_era_matrix.md) — `mailvetter_endpoint_era_matrix.json`
- [contact_ai_endpoint_era_matrix](contact_ai_endpoint_era_matrix.md) — `contact_ai_endpoint_era_matrix.json`
- [salesnavigator_endpoint_era_matrix](salesnavigator_endpoint_era_matrix.md) — `salesnavigator_endpoint_era_matrix.json`

## All endpoints (summary)

| endpoint_id | method | endpoint_path | api_version | endpoint_state | spec |
| --- | --- | --- | --- | --- | --- |
| count_contacts_graphql | QUERY | graphql/CountContacts | graphql | development | [detail](count_contacts_graphql.md) |
| get_activities_graphql | QUERY | graphql/GetActivities | graphql | development | [detail](get_activities_graphql.md) |
| get_billing_graphql | QUERY | graphql/GetBilling | graphql | development | [detail](get_billing_graphql.md) |
| get_company_contacts_graphql | QUERY | graphql/GetCompanyContacts | graphql | development | [detail](get_company_contacts_graphql.md) |
| get_company_filters_graphql | QUERY | graphql/GetCompanyFilters | graphql | development | [detail](get_company_filters_graphql.md) |
| get_company_graphql | QUERY | graphql/GetCompany | graphql | development | [detail](get_company_graphql.md) |
| get_contact_filters_graphql | QUERY | graphql/GetContactFilters | graphql | development | [detail](get_contact_filters_graphql.md) |
| get_contact_graphql | QUERY | graphql/GetContact | graphql | development | [detail](get_contact_graphql.md) |
| get_user_stats_graphql | QUERY | graphql/GetUserStats | graphql | development | [detail](get_user_stats_graphql.md) |
| list_exports_graphql | QUERY | graphql/ListExports | graphql | development | [detail](list_exports_graphql.md) |
| list_saved_searches_graphql | QUERY | graphql/ListSavedSearches | graphql | development | [detail](list_saved_searches_graphql.md) |
| list_users_graphql | QUERY | graphql/ListUsers | graphql | development | [detail](list_users_graphql.md) |
| mutation_abort_upload_graphql | MUTATION | graphql/AbortUpload | graphql | development | [detail](mutation_abort_upload_graphql.md) |
| mutation_analyze_email_risk_graphql | MUTATION | graphql/AnalyzeEmailRisk | graphql | development | [detail](mutation_analyze_email_risk_graphql.md) |
| mutation_cancel_export_graphql | MUTATION | graphql/CancelExport | graphql | development | [detail](mutation_cancel_export_graphql.md) |
| mutation_cancel_subscription_graphql | MUTATION | graphql/CancelSubscription | graphql | development | [detail](mutation_cancel_subscription_graphql.md) |
| mutation_complete_upload_graphql | MUTATION | graphql/CompleteUpload | graphql | development | [detail](mutation_complete_upload_graphql.md) |
| mutation_create_addon_graphql | MUTATION | graphql/CreateAddon | graphql | development | [detail](mutation_create_addon_graphql.md) |
| mutation_create_ai_chat_graphql | MUTATION | graphql/CreateAIChat | graphql | development | [detail](mutation_create_ai_chat_graphql.md) |
| mutation_create_api_key_graphql | MUTATION | graphql/CreateAPIKey | graphql | development | [detail](mutation_create_api_key_graphql.md) |
| mutation_create_company_export_graphql | MUTATION | graphql/CreateCompanyExport | graphql | development | [detail](mutation_create_company_export_graphql.md) |
| mutation_create_company_graphql | MUTATION | graphql/CreateCompany | graphql | development | [detail](mutation_create_company_graphql.md) |
| mutation_create_contact_export_graphql | MUTATION | graphql/CreateContactExport | graphql | development | [detail](mutation_create_contact_export_graphql.md) |
| mutation_create_contact_graphql | MUTATION | graphql/CreateContact | graphql | development | [detail](mutation_create_contact_graphql.md) |
| mutation_create_dashboard_page_graphql | MUTATION | graphql/CreateDashboardPage | graphql | development | [detail](mutation_create_dashboard_page_graphql.md) |
| mutation_create_documentation_page_graphql | MUTATION | graphql/CreateDocumentationPage | graphql | development | [detail](mutation_create_documentation_page_graphql.md) |
| mutation_create_export_job_graphql | MUTATION | graphql/CreateExportJob | graphql | development | [detail](mutation_create_export_job_graphql.md) |
| mutation_create_import_job_graphql | MUTATION | graphql/CreateImportJob | graphql | development | [detail](mutation_create_import_job_graphql.md) |
| mutation_create_job_graphql | MUTATION | graphql/CreateJob | graphql | development | [detail](mutation_create_job_graphql.md) |
| mutation_create_log_graphql | MUTATION | graphql/CreateLog | graphql | development | [detail](mutation_create_log_graphql.md) |
| mutation_create_logs_batch_graphql | MUTATION | graphql/CreateLogsBatch | graphql | development | [detail](mutation_create_logs_batch_graphql.md) |
| mutation_create_marketing_page_graphql | MUTATION | graphql/CreateMarketingPage | graphql | development | [detail](mutation_create_marketing_page_graphql.md) |
| mutation_create_plan_graphql | MUTATION | graphql/CreatePlan | graphql | development | [detail](mutation_create_plan_graphql.md) |
| mutation_create_plan_period_graphql | MUTATION | graphql/CreatePlanPeriod | graphql | development | [detail](mutation_create_plan_period_graphql.md) |
| mutation_create_saved_search_graphql | MUTATION | graphql/CreateSavedSearch | graphql | development | [detail](mutation_create_saved_search_graphql.md) |
| mutation_delete_addon_graphql | MUTATION | graphql/DeleteAddon | graphql | development | [detail](mutation_delete_addon_graphql.md) |
| mutation_delete_ai_chat_graphql | MUTATION | graphql/DeleteAIChat | graphql | development | [detail](mutation_delete_ai_chat_graphql.md) |
| mutation_delete_api_key_graphql | MUTATION | graphql/DeleteAPIKey | graphql | development | [detail](mutation_delete_api_key_graphql.md) |
| mutation_delete_company_graphql | MUTATION | graphql/DeleteCompany | graphql | development | [detail](mutation_delete_company_graphql.md) |
| mutation_delete_contact_graphql | MUTATION | graphql/DeleteContact | graphql | development | [detail](mutation_delete_contact_graphql.md) |
| mutation_delete_dashboard_page_graphql | MUTATION | graphql/DeleteDashboardPage | graphql | development | [detail](mutation_delete_dashboard_page_graphql.md) |
| mutation_delete_documentation_page_graphql | MUTATION | graphql/DeleteDocumentationPage | graphql | development | [detail](mutation_delete_documentation_page_graphql.md) |
| mutation_delete_log_graphql | MUTATION | graphql/DeleteLog | graphql | development | [detail](mutation_delete_log_graphql.md) |
| mutation_delete_logs_bulk_graphql | MUTATION | graphql/DeleteLogsBulk | graphql | development | [detail](mutation_delete_logs_bulk_graphql.md) |
| mutation_delete_marketing_page_graphql | MUTATION | graphql/DeleteMarketingPage | graphql | development | [detail](mutation_delete_marketing_page_graphql.md) |
| mutation_delete_notifications_graphql | MUTATION | graphql/DeleteNotifications | graphql | development | [detail](mutation_delete_notifications_graphql.md) |
| mutation_delete_plan_graphql | MUTATION | graphql/DeletePlan | graphql | development | [detail](mutation_delete_plan_graphql.md) |
| mutation_delete_plan_period_graphql | MUTATION | graphql/DeletePlanPeriod | graphql | development | [detail](mutation_delete_plan_period_graphql.md) |
| mutation_delete_saved_search_graphql | MUTATION | graphql/DeleteSavedSearch | graphql | development | [detail](mutation_delete_saved_search_graphql.md) |
| mutation_delete_user_graphql | MUTATION | graphql/DeleteUser | graphql | development | [detail](mutation_delete_user_graphql.md) |
| mutation_disable_2fa_graphql | MUTATION | graphql/Disable2FA | graphql | development | [detail](mutation_disable_2fa_graphql.md) |
| mutation_export_emails_graphql | MUTATION | graphql/ExportEmails | graphql | development | [detail](mutation_export_emails_graphql.md) |
| mutation_export_linkedin_results_graphql | MUTATION | graphql/ExportLinkedIn | graphql | development | [detail](mutation_export_linkedin_results_graphql.md) |
| mutation_find_single_email_graphql | MUTATION | graphql/FindSingleEmail | graphql | development | [detail](mutation_find_single_email_graphql.md) |
| mutation_generate_and_verify_graphql | MUTATION | graphql/GenerateAndVerify | graphql | development | [detail](mutation_generate_and_verify_graphql.md) |
| mutation_generate_company_summary_graphql | MUTATION | graphql/GenerateCompanySummary | graphql | development | [detail](mutation_generate_company_summary_graphql.md) |
| mutation_hard_delete_marketing_page_graphql | MUTATION | graphql/HardDeleteMarketingPage | graphql | development | [detail](mutation_hard_delete_marketing_page_graphql.md) |
| mutation_initiate_upload_graphql | MUTATION | graphql/InitiateUpload | graphql | development | [detail](mutation_initiate_upload_graphql.md) |
| mutation_login_graphql | MUTATION | graphql/Login | graphql | development | [detail](mutation_login_graphql.md) |
| mutation_logout_graphql | MUTATION | graphql/Logout | graphql | development | [detail](mutation_logout_graphql.md) |
| mutation_mark_notification_as_read_graphql | MUTATION | graphql/MarkNotificationAsRead | graphql | development | [detail](mutation_mark_notification_as_read_graphql.md) |
| mutation_parse_filters_graphql | MUTATION | graphql/ParseFilters | graphql | development | [detail](mutation_parse_filters_graphql.md) |
| mutation_promote_to_admin_graphql | MUTATION | graphql/PromoteToAdmin | graphql | development | [detail](mutation_promote_to_admin_graphql.md) |
| mutation_promote_to_super_admin_graphql | MUTATION | graphql/PromoteToSuperAdmin | graphql | development | [detail](mutation_promote_to_super_admin_graphql.md) |
| mutation_publish_marketing_page_graphql | MUTATION | graphql/PublishMarketingPage | graphql | development | [detail](mutation_publish_marketing_page_graphql.md) |
| mutation_purchase_addon_graphql | MUTATION | graphql/PurchaseAddon | graphql | development | [detail](mutation_purchase_addon_graphql.md) |
| mutation_refresh_token_graphql | MUTATION | graphql/RefreshToken | graphql | development | [detail](mutation_refresh_token_graphql.md) |
| mutation_regenerate_backup_codes_graphql | MUTATION | graphql/RegenerateBackupCodes | graphql | development | [detail](mutation_regenerate_backup_codes_graphql.md) |
| mutation_register_graphql | MUTATION | graphql/Register | graphql | development | [detail](mutation_register_graphql.md) |
| mutation_register_part_graphql | MUTATION | graphql/RegisterPart | graphql | development | [detail](mutation_register_part_graphql.md) |
| mutation_reset_usage_graphql | MUTATION | graphql/ResetUsage | graphql | development | [detail](mutation_reset_usage_graphql.md) |
| mutation_revoke_session_graphql | MUTATION | graphql/RevokeSession | graphql | development | [detail](mutation_revoke_session_graphql.md) |
| mutation_save_sales_navigator_profiles_graphql | MUTATION | graphql/SaveSalesNavigatorProfiles | graphql | development | [detail](mutation_save_sales_navigator_profiles_graphql.md) |
| mutation_search_linkedin_graphql | MUTATION | graphql/SearchLinkedIn | graphql | development | [detail](mutation_search_linkedin_graphql.md) |
| mutation_send_message_graphql | MUTATION | graphql/SendMessage | graphql | development | [detail](mutation_send_message_graphql.md) |
| mutation_setup_2fa_graphql | MUTATION | graphql/Setup2FA | graphql | development | [detail](mutation_setup_2fa_graphql.md) |
| mutation_submit_metric_graphql | MUTATION | graphql/SubmitMetric | graphql | development | [detail](mutation_submit_metric_graphql.md) |
| mutation_subscribe_graphql | MUTATION | graphql/Subscribe | graphql | development | [detail](mutation_subscribe_graphql.md) |
| mutation_track_usage_graphql | MUTATION | graphql/TrackUsage | graphql | development | [detail](mutation_track_usage_graphql.md) |
| mutation_update_addon_graphql | MUTATION | graphql/UpdateAddon | graphql | development | [detail](mutation_update_addon_graphql.md) |
| mutation_update_ai_chat_graphql | MUTATION | graphql/UpdateAIChat | graphql | development | [detail](mutation_update_ai_chat_graphql.md) |
| mutation_update_company_graphql | MUTATION | graphql/UpdateCompany | graphql | development | [detail](mutation_update_company_graphql.md) |
| mutation_update_contact_graphql | MUTATION | graphql/UpdateContact | graphql | development | [detail](mutation_update_contact_graphql.md) |
| mutation_update_dashboard_page_graphql | MUTATION | graphql/UpdateDashboardPage | graphql | development | [detail](mutation_update_dashboard_page_graphql.md) |
| mutation_update_documentation_page_graphql | MUTATION | graphql/UpdateDocumentationPage | graphql | development | [detail](mutation_update_documentation_page_graphql.md) |
| mutation_update_log_graphql | MUTATION | graphql/UpdateLog | graphql | development | [detail](mutation_update_log_graphql.md) |
| mutation_update_marketing_page_graphql | MUTATION | graphql/UpdateMarketingPage | graphql | development | [detail](mutation_update_marketing_page_graphql.md) |
| mutation_update_notification_preferences_graphql | MUTATION | graphql/UpdatePreferences | graphql | development | [detail](mutation_update_notification_preferences_graphql.md) |
| mutation_update_plan_graphql | MUTATION | graphql/UpdatePlan | graphql | development | [detail](mutation_update_plan_graphql.md) |
| mutation_update_profile_graphql | MUTATION | graphql/UpdateProfile | graphql | development | [detail](mutation_update_profile_graphql.md) |
| mutation_update_saved_search_graphql | MUTATION | graphql/UpdateSavedSearch | graphql | development | [detail](mutation_update_saved_search_graphql.md) |
| mutation_update_saved_search_usage_graphql | MUTATION | graphql/UpdateSavedSearchUsage | graphql | development | [detail](mutation_update_saved_search_usage_graphql.md) |
| mutation_update_user_credits_graphql | MUTATION | graphql/UpdateUserCredits | graphql | development | [detail](mutation_update_user_credits_graphql.md) |
| mutation_update_user_role_graphql | MUTATION | graphql/UpdateUserRole | graphql | development | [detail](mutation_update_user_role_graphql.md) |
| mutation_upload_avatar_graphql | MUTATION | graphql/UploadAvatar | graphql | development | [detail](mutation_upload_avatar_graphql.md) |
| mutation_upsert_by_linkedin_url_graphql | MUTATION | graphql/UpsertByLinkedInUrl | graphql | development | [detail](mutation_upsert_by_linkedin_url_graphql.md) |
| mutation_verify_2fa_graphql | MUTATION | graphql/Verify2FA | graphql | development | [detail](mutation_verify_2fa_graphql.md) |
| mutation_verify_and_find_graphql | MUTATION | graphql/VerifyAndFind | graphql | development | [detail](mutation_verify_and_find_graphql.md) |
| mutation_verify_bulk_emails_graphql | MUTATION | graphql/VerifyBulkEmails | graphql | development | [detail](mutation_verify_bulk_emails_graphql.md) |
| mutation_verify_single_email_graphql | MUTATION | graphql/VerifySingleEmail | graphql | development | [detail](mutation_verify_single_email_graphql.md) |
| query_admin_marketing_pages_graphql | QUERY | graphql/AdminMarketingPages | graphql | development | [detail](query_admin_marketing_pages_graphql.md) |
| query_aggregate_metrics_graphql | QUERY | graphql/AggregateMetrics | graphql | development | [detail](query_aggregate_metrics_graphql.md) |
| query_companies_graphql | QUERY | graphql/QueryCompanies | graphql | development | [detail](query_companies_graphql.md) |
| query_contacts_graphql | QUERY | graphql/QueryContacts | graphql | development | [detail](query_contacts_graphql.md) |
| query_find_emails_graphql | QUERY | graphql/FindEmails | graphql | development | [detail](query_find_emails_graphql.md) |
| query_get_2fa_status_graphql | QUERY | graphql/Get2FAStatus | graphql | development | [detail](query_get_2fa_status_graphql.md) |
| query_get_activity_stats_graphql | QUERY | graphql/GetActivityStats | graphql | development | [detail](query_get_activity_stats_graphql.md) |
| query_get_addons_graphql | QUERY | graphql/GetAddons | graphql | development | [detail](query_get_addons_graphql.md) |
| query_get_admin_addons_graphql | QUERY | graphql/GetAdminAddons | graphql | development | [detail](query_get_admin_addons_graphql.md) |
| query_get_admin_plans_graphql | QUERY | graphql/GetAdminPlans | graphql | development | [detail](query_get_admin_plans_graphql.md) |
| query_get_ai_chat_graphql | QUERY | graphql/GetAIChat | graphql | development | [detail](query_get_ai_chat_graphql.md) |
| query_get_api_metadata_graphql | QUERY | graphql/GetAPIMetadata | graphql | development | [detail](query_get_api_metadata_graphql.md) |
| query_get_dashboard_page_graphql | QUERY | graphql/GetDashboardPage | graphql | development | [detail](query_get_dashboard_page_graphql.md) |
| query_get_documentation_content_graphql | QUERY | graphql/GetDocumentationContent | graphql | development | [detail](query_get_documentation_content_graphql.md) |
| query_get_documentation_page_graphql | QUERY | graphql/GetDocumentationPage | graphql | development | [detail](query_get_documentation_page_graphql.md) |
| query_get_export_download_url_graphql | QUERY | graphql/GetExportDownloadUrl | graphql | development | [detail](query_get_export_download_url_graphql.md) |
| query_get_export_graphql | QUERY | graphql/GetExport | graphql | development | [detail](query_get_export_graphql.md) |
| query_get_health_graphql | QUERY | graphql/GetHealth | graphql | development | [detail](query_get_health_graphql.md) |
| query_get_import_job_graphql | QUERY | graphql/GetImportJob | graphql | development | [detail](query_get_import_job_graphql.md) |
| query_get_invoices_graphql | QUERY | graphql/GetInvoices | graphql | development | [detail](query_get_invoices_graphql.md) |
| query_get_job_graphql | QUERY | graphql/GetJob | graphql | development | [detail](query_get_job_graphql.md) |
| query_get_log_statistics_graphql | QUERY | graphql/GetLogStatistics | graphql | development | [detail](query_get_log_statistics_graphql.md) |
| query_get_marketing_page_graphql | QUERY | graphql/GetMarketingPage | graphql | development | [detail](query_get_marketing_page_graphql.md) |
| query_get_me_graphql | QUERY | graphql/GetMe | graphql | development | [detail](query_get_me_graphql.md) |
| query_get_notification_graphql | QUERY | graphql/GetNotification | graphql | development | [detail](query_get_notification_graphql.md) |
| query_get_performance_metrics_graphql | QUERY | graphql/GetPerformanceMetrics | graphql | development | [detail](query_get_performance_metrics_graphql.md) |
| query_get_plans_graphql | QUERY | graphql/GetPlans | graphql | development | [detail](query_get_plans_graphql.md) |
| query_get_presigned_url_graphql | QUERY | graphql/GetPresignedUrl | graphql | development | [detail](query_get_presigned_url_graphql.md) |
| query_get_s3_file_data_graphql | QUERY | graphql/GetS3FileData | graphql | development | [detail](query_get_s3_file_data_graphql.md) |
| query_get_s3_file_presigned_url_graphql | QUERY | graphql/GetS3FileDownloadUrl | graphql | development | [detail](query_get_s3_file_presigned_url_graphql.md) |
| query_get_saved_search_graphql | QUERY | graphql/GetSavedSearch | graphql | development | [detail](query_get_saved_search_graphql.md) |
| query_get_session_graphql | QUERY | graphql/GetSession | graphql | development | [detail](query_get_session_graphql.md) |
| query_get_unread_count_graphql | QUERY | graphql/GetUnreadCount | graphql | development | [detail](query_get_unread_count_graphql.md) |
| query_get_upload_status_graphql | QUERY | graphql/GetUploadStatus | graphql | development | [detail](query_get_upload_status_graphql.md) |
| query_get_upload_url_graphql | QUERY | graphql/GetUploadUrl | graphql | development | [detail](query_get_upload_url_graphql.md) |
| query_get_usage_graphql | QUERY | graphql/GetUsage | graphql | development | [detail](query_get_usage_graphql.md) |
| query_get_user_graphql | QUERY | graphql/GetUser | graphql | development | [detail](query_get_user_graphql.md) |
| query_get_user_history_graphql | QUERY | graphql/GetUserHistory | graphql | development | [detail](query_get_user_history_graphql.md) |
| query_get_vql_health_graphql | QUERY | graphql/GetVQLHealth | graphql | development | [detail](query_get_vql_health_graphql.md) |
| query_get_vql_stats_graphql | QUERY | graphql/GetVQLStats | graphql | development | [detail](query_get_vql_stats_graphql.md) |
| query_list_ai_chats_graphql | QUERY | graphql/ListAIChats | graphql | development | [detail](query_list_ai_chats_graphql.md) |
| query_list_api_keys_graphql | QUERY | graphql/ListAPIKeys | graphql | development | [detail](query_list_api_keys_graphql.md) |
| query_list_dashboard_pages_graphql | QUERY | graphql/ListDashboardPages | graphql | development | [detail](query_list_dashboard_pages_graphql.md) |
| query_list_documentation_pages_graphql | QUERY | graphql/ListDocumentationPages | graphql | development | [detail](query_list_documentation_pages_graphql.md) |
| query_list_import_jobs_graphql | QUERY | graphql/ListImportJobs | graphql | development | [detail](query_list_import_jobs_graphql.md) |
| query_list_jobs_graphql | QUERY | graphql/ListJobs | graphql | development | [detail](query_list_jobs_graphql.md) |
| query_list_marketing_pages_graphql | QUERY | graphql/ListMarketingPages | graphql | development | [detail](query_list_marketing_pages_graphql.md) |
| query_list_notifications_graphql | QUERY | graphql/ListNotifications | graphql | development | [detail](query_list_notifications_graphql.md) |
| query_list_s3_files_graphql | QUERY | graphql/ListS3Files | graphql | development | [detail](query_list_s3_files_graphql.md) |
| query_list_saved_searches_graphql | QUERY | graphql/ListSavedSearches | graphql | development | [detail](query_list_saved_searches_graphql.md) |
| query_list_scraping_records_graphql | QUERY | graphql/ListScrapingRecords | graphql | development | [detail](query_list_scraping_records_graphql.md) |
| query_list_sessions_graphql | QUERY | graphql/ListSessions | graphql | development | [detail](query_list_sessions_graphql.md) |
| query_list_team_members_graphql | QUERY | graphql/ListTeamMembers | graphql | development | [detail](query_list_team_members_graphql.md) |
| query_list_users_graphql | QUERY | graphql/ListUsers | graphql | development | [detail](query_list_users_graphql.md) |
| query_query_logs_graphql | QUERY | graphql/QueryLogs | graphql | development | [detail](query_query_logs_graphql.md) |
| query_search_logs_graphql | QUERY | graphql/SearchLogs | graphql | development | [detail](query_search_logs_graphql.md) |
| mutation_create_campaign | MUTATION | graphql/createCampaign | graphql | planned | [detail](mutation_create_campaign.md) |
| mutation_schedule_campaign | MUTATION | graphql/scheduleCampaign | graphql | planned | [detail](mutation_schedule_campaign.md) |
| mutation_pause_campaign | MUTATION | graphql/pauseCampaign | graphql | planned | [detail](mutation_pause_campaign.md) |
| query_list_campaigns | QUERY | graphql/listCampaigns | graphql | planned | [detail](query_list_campaigns.md) |
| query_get_campaign | QUERY | graphql/getCampaign | graphql | planned | [detail](query_get_campaign.md) |
| mutation_create_sequence | MUTATION | graphql/createSequence | graphql | planned | [detail](mutation_create_sequence.md) |
| mutation_enroll_contacts_sequence | MUTATION | graphql/enrollContacts | graphql | planned | [detail](mutation_enroll_contacts_sequence.md) |
| query_list_sequences | QUERY | graphql/listSequences | graphql | planned | [detail](query_list_sequences.md) |
| mutation_save_campaign_template | MUTATION | graphql/saveTemplate | graphql | planned | [detail](mutation_save_campaign_template.md) |
| query_list_campaign_templates | QUERY | graphql/listCampaignTemplates | graphql | planned | [detail](query_list_campaign_templates.md) |
| query_render_template_preview | QUERY | graphql/renderPreview | graphql | planned | [detail](query_render_template_preview.md) |
| mutation_create_webhook | MUTATION | graphql/subscribeWebhook | graphql | planned | [detail](mutation_create_webhook.md) |
| query_list_webhooks | QUERY | graphql/listWebhooks | graphql | planned | [detail](query_list_webhooks.md) |
| mutation_delete_webhook | MUTATION | graphql/deleteWebhook | graphql | planned | [detail](mutation_delete_webhook.md) |
| mutation_connect_integration | MUTATION | graphql/connectIntegration | graphql | planned | [detail](mutation_connect_integration.md) |
| query_list_integrations | QUERY | graphql/listIntegrations | graphql | planned | [detail](query_list_integrations.md) |
| mutation_sync_integration | MUTATION | graphql/syncContacts | graphql | planned | [detail](mutation_sync_integration.md) |

<!-- AUTO:db-graph:start -->

## Era alignment (Contact360 0.x–10.x)

- **Lifecycle `era` (metadata):** `—` — see [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md#era-tags-on-endpoints) for theme mapping.

## Database tables → SQL snapshots

- *No `db_tables_read` / `db_tables_write` in this spec — gateway-only or metadata TBD; see lineage.*

## Lineage & infrastructure docs

- [Appointment360 lineage](../database/appointment360_data_lineage.md) (default GraphQL owner)

## Downstream services (cross-endpoint)

- *No `lambda_services` list — typically Appointment360-only DB access or inline HTTP client; see [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md).*

## Related endpoint graph

- **Topology overview:** [SERVICE_TOPOLOGY.md](SERVICE_TOPOLOGY.md)
- **Conventions:** [ENDPOINT_DATABASE_LINKS.md](ENDPOINT_DATABASE_LINKS.md)

<!-- AUTO:db-graph:end -->
---

*Generated from `endpoints_index.json`. Re-run `python json_to_markdown_endpoints.py`.*
