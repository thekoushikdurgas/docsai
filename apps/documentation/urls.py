"""URL configuration for documentation app."""
from django.urls import path, include, reverse
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from .views import dashboard as dashboard_views


def redirect_to_dashboard_health(request):
    """Redirect /docs/health/ to dashboard with ?tab=health (for sidebar and links)."""
    return HttpResponseRedirect(reverse('documentation:dashboard') + '?tab=health')


def redirect_pages_format_to_create(request):
    """Redirect /docs/pages/format/ to pages create with Format tab (format content merged into create form)."""
    from urllib.parse import urlencode
    target = reverse('documentation:page_create')
    params = {'tab': 'format'}
    if request.GET.get('return_url'):
        params['return_url'] = request.GET.get('return_url')
    return HttpResponseRedirect(target + '?' + urlencode(params))


def create_redirect_view(target_name):
    """Create a redirect view function for a given URL name."""
    def redirect_view(request):
        from django.urls import reverse
        try:
            target_url = reverse(f'documentation:{target_name}')
            # Preserve query parameters
            query_string = request.GET.urlencode()
            if query_string:
                target_url = f"{target_url}?{query_string}"
            return HttpResponsePermanentRedirect(target_url)
        except Exception:
            # Fallback to dashboard if route doesn't exist
            return redirect('documentation:dashboard')
    return redirect_view
# Removed: api_router, api_urls_versioned (API routes removed)
# Import legacy views directly from views.py file (not from views package)
# Use importlib to avoid package/directory conflict
import importlib.util
import os
views_file_path = os.path.join(os.path.dirname(__file__), 'views.py')
spec = importlib.util.spec_from_file_location("legacy_views", views_file_path)
legacy_views = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy_views)
from .views.pages_views import (
    page_detail_view,
    page_form_view,
    page_create_api,
    page_draft_api,
    page_update_api,
    page_delete_api,
)
from .views.endpoints_views import (
    endpoint_detail_view,
    endpoint_form_view,
    endpoint_create_api,
    endpoint_draft_api,
    endpoint_update_api,
    endpoint_delete_api,
    endpoint_delete_view,
)
from .views.relationships_views import (
    relationship_detail_view,
    relationship_form_view,
    relationship_create_api,
    relationship_update_api,
    relationship_delete_view,
    relationship_delete_api,
)
from .views.postman_views import (
    postman_detail_view,
    postman_form_view,
    postman_delete_view,
)
from .views import operations
from .views import documentation_dashboard_views as media_manager_dashboard
from .views import documentation_file_views
from .views import routes_overview
from .api import views as api_views
from .api import documentation_dashboard_api as media_manager_api

app_name = 'documentation'

urlpatterns = [
    # Dashboard (list/graph use initial_data + /api/v1/dashboard/*)
    path('', dashboard_views.documentation_dashboard, name='dashboard'),
    path('pages/', dashboard_views.documentation_dashboard, name='dashboard_pages'),
    path('endpoints/', dashboard_views.documentation_dashboard, name='dashboard_endpoints'),
    path('relationships/', dashboard_views.documentation_dashboard, name='dashboard_relationships'),
    
    # API endpoints - REMOVED (dashboard APIs removed; use /api/v1/dashboard/*)
    # Removed: /api/versions/, /api/v2/, /api/health/, /api/stats/, /api/schemas/
    # Services are now used directly in views and minimal dashboard/media APIs
    # Note: /api/v1/ is included at root level in docsai/urls.py for statistics endpoints
    
    # ============================================================================
    # Unified Dashboard Routes - Migrated from /docs/media-manager/
    # All 119 endpoints integrated into /docs/ dashboard
    # ============================================================================
    
    # Health tab entry (redirect to dashboard ?tab=health for sidebar/links)
    path('health/', redirect_to_dashboard_health, name='health'),
    path('service-info/', media_manager_dashboard.media_manager_service_info, name='service_info'),
    # Redirect old endpoint-stats to new /api/docs/ with graph
    path('docs/endpoint-stats/', lambda r: HttpResponsePermanentRedirect('/api/docs/'), name='docs_endpoint_stats'),
    
    # Routes & APIs overview (static route before parameterized)
    path('routes-overview/', routes_overview.routes_overview_view, name='routes_overview'),

    # Pages API Routes (static routes before parameterized) - statistics now live on main /docs/ dashboard
    path('pages/format/', redirect_pages_format_to_create, name='pages_format'),
    path('pages/types/', media_manager_dashboard.media_manager_pages_types, name='pages_types'),
    path('pages/by-type/docs/', media_manager_dashboard.media_manager_pages_by_type_docs, name='pages_by_type_docs'),
    path('pages/by-type/marketing/', media_manager_dashboard.media_manager_pages_by_type_marketing, name='pages_by_type_marketing'),
    path('pages/by-type/dashboard/', media_manager_dashboard.media_manager_pages_by_type_dashboard, name='pages_by_type_dashboard'),
    path('pages/by-type/product/', media_manager_dashboard.media_manager_pages_by_type_product, name='pages_by_type_product'),
    path('pages/by-type/title/', media_manager_dashboard.media_manager_pages_by_type_title, name='pages_by_type_title'),
    # Generic pages by type route (must be after specific routes)
    path('pages/by-type/<str:page_type>/', media_manager_dashboard.media_manager_pages_by_type, name='pages_by_type'),
    path('pages/by-type/<str:page_type>/published/', media_manager_dashboard.media_manager_pages_by_type_published, name='pages_by_type_published'),
    path('pages/by-type/<str:page_type>/draft/', media_manager_dashboard.media_manager_pages_by_type_draft, name='pages_by_type_draft'),
    path('pages/by-type/<str:page_type>/stats/', media_manager_dashboard.media_manager_pages_by_type_stats, name='pages_by_type_stats'),
    path('pages/by-type/<str:page_type>/count/', media_manager_dashboard.media_manager_pages_by_type_count, name='pages_by_type_count'),
    path('pages/by-state/<str:state>/count/', media_manager_dashboard.media_manager_pages_by_state_count, name='pages_by_state_count'),
    path('pages/by-state/<str:state>/', media_manager_dashboard.media_manager_pages_by_state, name='pages_by_state'),
    path('pages/by-user-type/<str:user_type>/', media_manager_dashboard.media_manager_pages_by_user_type, name='pages_by_user_type'),
    # Page sub-resource routes (must be before page detail route)
    path('pages/<str:page_id>/sections/', media_manager_dashboard.media_manager_page_sections, name='page_sections'),
    path('pages/<str:page_id>/components/', media_manager_dashboard.media_manager_page_components, name='page_components'),
    path('pages/<str:page_id>/endpoints/', media_manager_dashboard.media_manager_page_endpoints, name='page_endpoints'),
    path('pages/<str:page_id>/versions/', media_manager_dashboard.media_manager_page_versions, name='page_versions'),
    path('pages/<str:page_id>/access-control/', media_manager_dashboard.media_manager_page_access_control, name='page_access_control'),
    # Page detail route (after sub-resources)
    path('pages/<str:page_id>/detail/', media_manager_dashboard.media_manager_page_detail, name='page_detail_enhanced'),
    
    # Endpoints API Routes (static routes before parameterized) - 28 routes
    path('endpoints/statistics/', media_manager_dashboard.media_manager_endpoints_statistics, name='endpoints_statistics'),
    path('endpoints/format/', media_manager_dashboard.media_manager_endpoints_format, name='endpoints_format'),
    path('endpoints/api-versions/', media_manager_dashboard.media_manager_endpoints_api_versions, name='endpoints_api_versions'),
    path('endpoints/methods/', media_manager_dashboard.media_manager_endpoints_methods, name='endpoints_methods'),
    path('endpoints/by-api-version/v1/', media_manager_dashboard.media_manager_endpoints_by_api_version_v1, name='endpoints_by_api_version_v1'),
    path('endpoints/by-api-version/v4/', media_manager_dashboard.media_manager_endpoints_by_api_version_v4, name='endpoints_by_api_version_v4'),
    path('endpoints/by-api-version/graphql/', media_manager_dashboard.media_manager_endpoints_by_api_version_graphql, name='endpoints_by_api_version_graphql'),
    # Generic endpoints by API version route (must be after specific routes)
    path('endpoints/by-api-version/<str:api_version>/', media_manager_dashboard.media_manager_endpoints_by_api_version, name='endpoints_by_api_version'),
    path('endpoints/by-api-version/<str:api_version>/count/', media_manager_dashboard.media_manager_endpoints_by_api_version_count, name='endpoints_by_api_version_count'),
    path('endpoints/by-api-version/<str:api_version>/stats/', media_manager_dashboard.media_manager_endpoints_by_api_version_stats, name='endpoints_by_api_version_stats'),
    path('endpoints/by-api-version/<str:api_version>/by-method/<str:method>/', media_manager_dashboard.media_manager_endpoints_by_api_version_by_method, name='endpoints_by_api_version_by_method'),
    path('endpoints/by-method/GET/', media_manager_dashboard.media_manager_endpoints_by_method_get, name='endpoints_by_method_get'),
    path('endpoints/by-method/POST/', media_manager_dashboard.media_manager_endpoints_by_method_post, name='endpoints_by_method_post'),
    path('endpoints/by-method/QUERY/', media_manager_dashboard.media_manager_endpoints_by_method_query, name='endpoints_by_method_query'),
    path('endpoints/by-method/MUTATION/', media_manager_dashboard.media_manager_endpoints_by_method_mutation, name='endpoints_by_method_mutation'),
    # Generic endpoints by method route (must be after specific routes)
    path('endpoints/by-method/<str:method>/', media_manager_dashboard.media_manager_endpoints_by_method, name='endpoints_by_method'),
    path('endpoints/by-method/<str:method>/count/', media_manager_dashboard.media_manager_endpoints_by_method_count, name='endpoints_by_method_count'),
    path('endpoints/by-method/<str:method>/stats/', media_manager_dashboard.media_manager_endpoints_by_method_stats, name='endpoints_by_method_stats'),
    path('endpoints/by-state/<str:state>/count/', media_manager_dashboard.media_manager_endpoints_by_state_count, name='endpoints_by_state_count'),
    path('endpoints/by-state/<str:state>/', media_manager_dashboard.media_manager_endpoints_by_state, name='endpoints_by_state'),
    path('endpoints/by-lambda/<str:service_name>/count/', media_manager_dashboard.media_manager_endpoints_by_lambda_count, name='endpoints_by_lambda_count'),
    path('endpoints/by-lambda/<str:service_name>/', media_manager_dashboard.media_manager_endpoints_by_lambda, name='endpoints_by_lambda'),
    # Endpoint sub-resource routes (must be before endpoint detail route)
    path('endpoints/<str:endpoint_id>/pages/', media_manager_dashboard.media_manager_endpoint_pages, name='endpoint_pages'),
    path('endpoints/<str:endpoint_id>/access-control/', media_manager_dashboard.media_manager_endpoint_access_control, name='endpoint_access_control'),
    path('endpoints/<str:endpoint_id>/lambda-services/', media_manager_dashboard.media_manager_endpoint_lambda_services, name='endpoint_lambda_services'),
    path('endpoints/<str:endpoint_id>/files/', media_manager_dashboard.media_manager_endpoint_files, name='endpoint_files'),
    path('endpoints/<str:endpoint_id>/methods/', media_manager_dashboard.media_manager_endpoint_methods, name='endpoint_methods'),
    path('endpoints/<str:endpoint_id>/used-by-pages/', media_manager_dashboard.media_manager_endpoint_used_by_pages, name='endpoint_used_by_pages'),
    path('endpoints/<str:endpoint_id>/dependencies/', media_manager_dashboard.media_manager_endpoint_dependencies, name='endpoint_dependencies'),
    # Endpoint detail route (after sub-resources)
    path('endpoints/<str:endpoint_id>/detail/', media_manager_dashboard.media_manager_endpoint_detail, name='endpoint_detail_enhanced'),
    
    # Relationships API Routes (static routes before parameterized) - 38 routes
    path('relationships/statistics/', media_manager_dashboard.media_manager_relationships_statistics, name='relationships_statistics'),
    path('relationships/format/', media_manager_dashboard.media_manager_relationships_format, name='relationships_format'),
    path('relationships/graph/', media_manager_dashboard.media_manager_relationships_graph, name='relationships_graph'),
    path('relationships/usage-types/', media_manager_dashboard.media_manager_relationships_usage_types, name='relationships_usage_types'),
    path('relationships/usage-contexts/', media_manager_dashboard.media_manager_relationships_usage_contexts, name='relationships_usage_contexts'),
    path('relationships/by-page/<str:page_id>/primary/', media_manager_dashboard.media_manager_relationships_by_page_primary, name='relationships_by_page_primary'),
    path('relationships/by-page/<str:page_id>/secondary/', media_manager_dashboard.media_manager_relationships_by_page_secondary, name='relationships_by_page_secondary'),
    path('relationships/by-page/<str:page_id>/count/', media_manager_dashboard.media_manager_relationships_by_page_count, name='relationships_by_page_count'),
    path('relationships/by-page/<str:page_id>/by-usage-type/<str:usage_type>/', media_manager_dashboard.media_manager_relationships_by_page_by_usage_type, name='relationships_by_page_by_usage_type'),
    path('relationships/by-page/<str:page_id>/', media_manager_dashboard.media_manager_relationships_by_page, name='relationships_by_page'),
    path('relationships/by-endpoint/<str:endpoint_id>/pages/', media_manager_dashboard.media_manager_relationships_by_endpoint_pages, name='relationships_by_endpoint_pages'),
    path('relationships/by-endpoint/<str:endpoint_id>/count/', media_manager_dashboard.media_manager_relationships_by_endpoint_count, name='relationships_by_endpoint_count'),
    path('relationships/by-endpoint/<str:endpoint_id>/by-usage-context/<str:usage_context>/', media_manager_dashboard.media_manager_relationships_by_endpoint_by_usage_context, name='relationships_by_endpoint_by_usage_context'),
    path('relationships/by-endpoint/<str:endpoint_id>/', media_manager_dashboard.media_manager_relationships_by_endpoint, name='relationships_by_endpoint'),
    path('relationships/by-usage-type/primary/', media_manager_dashboard.media_manager_relationships_by_usage_type_primary, name='relationships_by_usage_type_primary'),
    path('relationships/by-usage-type/secondary/', media_manager_dashboard.media_manager_relationships_by_usage_type_secondary, name='relationships_by_usage_type_secondary'),
    path('relationships/by-usage-type/conditional/', media_manager_dashboard.media_manager_relationships_by_usage_type_conditional, name='relationships_by_usage_type_conditional'),
    # Generic relationships by usage type route (must be after specific routes)
    path('relationships/by-usage-type/<str:usage_type>/', media_manager_dashboard.media_manager_relationships_by_usage_type, name='relationships_by_usage_type'),
    path('relationships/by-usage-type/<str:usage_type>/count/', media_manager_dashboard.media_manager_relationships_by_usage_type_count, name='relationships_by_usage_type_count'),
    path('relationships/by-usage-type/<str:usage_type>/by-usage-context/<str:usage_context>/', media_manager_dashboard.media_manager_relationships_by_usage_type_by_usage_context, name='relationships_by_usage_type_by_usage_context'),
    path('relationships/by-usage-context/data_fetching/', media_manager_dashboard.media_manager_relationships_by_usage_context_data_fetching, name='relationships_by_usage_context_data_fetching'),
    path('relationships/by-usage-context/data_mutation/', media_manager_dashboard.media_manager_relationships_by_usage_context_data_mutation, name='relationships_by_usage_context_data_mutation'),
    path('relationships/by-usage-context/authentication/', media_manager_dashboard.media_manager_relationships_by_usage_context_authentication, name='relationships_by_usage_context_authentication'),
    path('relationships/by-usage-context/analytics/', media_manager_dashboard.media_manager_relationships_by_usage_context_analytics, name='relationships_by_usage_context_analytics'),
    # Generic relationships by usage context route (must be after specific routes)
    path('relationships/by-usage-context/<str:usage_context>/', media_manager_dashboard.media_manager_relationships_by_usage_context, name='relationships_by_usage_context'),
    path('relationships/by-usage-context/<str:usage_context>/count/', media_manager_dashboard.media_manager_relationships_by_usage_context_count, name='relationships_by_usage_context_count'),
    path('relationships/by-state/<str:state>/count/', media_manager_dashboard.media_manager_relationships_by_state_count, name='relationships_by_state_count'),
    path('relationships/by-state/<str:state>/', media_manager_dashboard.media_manager_relationships_by_state, name='relationships_by_state'),
    path('relationships/by-lambda/<str:service_name>/', media_manager_dashboard.media_manager_relationships_by_lambda, name='relationships_by_lambda'),
    path('relationships/by-invocation-pattern/<str:pattern>/', media_manager_dashboard.media_manager_relationships_by_invocation_pattern, name='relationships_by_invocation_pattern'),
    path('relationships/by-postman-config/<str:config_id>/', media_manager_dashboard.media_manager_relationships_by_postman_config, name='relationships_by_postman_config'),
    path('relationships/performance/slow/', media_manager_dashboard.media_manager_relationships_performance_slow, name='relationships_performance_slow'),
    path('relationships/performance/errors/', media_manager_dashboard.media_manager_relationships_performance_errors, name='relationships_performance_errors'),
    # Relationship sub-resource routes (must be before relationship detail route)
    path('relationships/<str:relationship_id>/access-control/', media_manager_dashboard.media_manager_relationship_access_control, name='relationship_access_control'),
    path('relationships/<str:relationship_id>/data-flow/', media_manager_dashboard.media_manager_relationship_data_flow, name='relationship_data_flow'),
    path('relationships/<str:relationship_id>/performance/', media_manager_dashboard.media_manager_relationship_performance, name='relationship_performance'),
    path('relationships/<str:relationship_id>/dependencies/', media_manager_dashboard.media_manager_relationship_dependencies, name='relationship_dependencies'),
    path('relationships/<str:relationship_id>/postman/', media_manager_dashboard.media_manager_relationship_postman, name='relationship_postman'),
    # Relationship detail route (after sub-resources)
    path('relationships/<str:relationship_id>/detail/', media_manager_dashboard.media_manager_relationship_detail, name='relationship_detail_enhanced'),
    
    # Postman API Routes (static routes before parameterized) - 14 routes
    path('postman/statistics/', media_manager_dashboard.media_manager_postman_statistics, name='postman_statistics'),
    path('postman/format/', media_manager_dashboard.media_manager_postman_format, name='postman_format'),
    path('postman/by-state/<str:state>/count/', media_manager_dashboard.media_manager_postman_by_state_count, name='postman_by_state_count'),
    path('postman/by-state/<str:state>/', media_manager_dashboard.media_manager_postman_by_state, name='postman_by_state'),
    # Postman sub-resource routes (must be before postman detail route)
    path('postman/<str:config_id>/collection/', media_manager_dashboard.media_manager_postman_collection, name='postman_collection'),
    path('postman/<str:config_id>/environments/<str:env_name>/', media_manager_dashboard.media_manager_postman_environment, name='postman_environment'),
    path('postman/<str:config_id>/environments/', media_manager_dashboard.media_manager_postman_environments, name='postman_environments'),
    path('postman/<str:config_id>/mappings/<str:mapping_id>/', media_manager_dashboard.media_manager_postman_mapping, name='postman_mapping'),
    path('postman/<str:config_id>/mappings/', media_manager_dashboard.media_manager_postman_mappings, name='postman_mappings'),
    path('postman/<str:config_id>/test-suites/<str:suite_id>/', media_manager_dashboard.media_manager_postman_test_suite, name='postman_test_suite'),
    path('postman/<str:config_id>/test-suites/', media_manager_dashboard.media_manager_postman_test_suites, name='postman_test_suites'),
    path('postman/<str:config_id>/access-control/', media_manager_dashboard.media_manager_postman_access_control, name='postman_access_control'),
    # Postman detail route (after sub-resources)
    path('postman/<str:config_id>/detail/', media_manager_dashboard.media_manager_postman_detail, name='postman_detail_enhanced'),
    
    # Index API Routes (8 routes)
    path('index/pages/validate/', media_manager_dashboard.media_manager_index_pages_validate, name='index_pages_validate'),
    path('index/endpoints/validate/', media_manager_dashboard.media_manager_index_endpoints_validate, name='index_endpoints_validate'),
    path('index/relationships/validate/', media_manager_dashboard.media_manager_index_relationships_validate, name='index_relationships_validate'),
    path('index/postman/validate/', media_manager_dashboard.media_manager_index_postman_validate, name='index_postman_validate'),
    path('index/pages/', media_manager_dashboard.media_manager_index_pages, name='index_pages'),
    path('index/endpoints/', media_manager_dashboard.media_manager_index_endpoints, name='index_endpoints'),
    path('index/relationships/', media_manager_dashboard.media_manager_index_relationships, name='index_relationships'),
    path('index/postman/', media_manager_dashboard.media_manager_index_postman, name='index_postman'),
    
    # Dashboard API Routes (4 routes)
    path('dashboard/pages/', media_manager_dashboard.media_manager_dashboard_pages, name='dashboard_pages_enhanced'),
    path('dashboard/endpoints/', media_manager_dashboard.media_manager_dashboard_endpoints, name='dashboard_endpoints_enhanced'),
    path('dashboard/relationships/', media_manager_dashboard.media_manager_dashboard_relationships, name='dashboard_relationships_enhanced'),
    path('dashboard/postman/', media_manager_dashboard.media_manager_dashboard_postman, name='dashboard_postman_enhanced'),
    
    # ============================================================================
    # End of Unified Dashboard Routes
    # ============================================================================
    
    # Pages CRUD (form views use services directly - API endpoints)
    # Static 'create' must come before '<str:page_id>' or /docs/pages/create/ is matched as detail
    path('pages/create/', page_form_view, name='page_create'),
    path('pages/<str:page_id>/', page_detail_view, name='page_detail'),
    path('pages/<str:page_id>/edit/', page_form_view, name='page_edit'),
    path('pages/<str:page_id>/update/', legacy_views.update_page_view, name='page_update'),
    path('pages/<str:page_id>/delete/', legacy_views.delete_page_view, name='page_delete'),
    
    # Endpoints CRUD (form views use services directly - no API endpoints)
    # Static 'create' must come before '<str:endpoint_id>' or /docs/endpoints/create/ is matched as detail
    path('endpoints/create/', endpoint_form_view, name='endpoint_create'),
    path('endpoints/<str:endpoint_id>/', endpoint_detail_view, name='endpoint_detail'),
    path('endpoints/<str:endpoint_id>/edit/', endpoint_form_view, name='endpoint_edit'),
    path('endpoints/<str:endpoint_id>/delete/', endpoint_delete_view, name='endpoint_delete'),
    
    # API endpoints (for form auto-save and AJAX operations)
    path('api/endpoints/draft/', endpoint_draft_api, name='api_endpoint_draft'),
    path('api/pages/draft/', page_draft_api, name='api_page_draft'),
    
    # Relationships CRUD and API (form + create/update/delete API for AJAX)
    # Static 'create' must come before '<str:relationship_id>' or /docs/relationships/create/ is matched as detail
    path('relationships/create/', relationship_form_view, name='relationship_create'),
    path('relationships/<str:relationship_id>/delete/', relationship_delete_view, name='relationship_delete'),
    path('relationships/<str:relationship_id>/', relationship_detail_view, name='relationship_detail'),
    path('relationships/<str:relationship_id>/edit/', relationship_form_view, name='relationship_edit'),
    path('api/relationships/create/', relationship_create_api, name='api_relationship_create'),
    path('api/relationships/<str:relationship_id>/update/', relationship_update_api, name='api_relationship_update'),
    path('api/relationships/<str:relationship_id>/delete/', relationship_delete_api, name='api_relationship_delete'),
    
    # Postman CRUD (create before detail so /postman/create/ is not captured as postman_id)
    path('postman/create/', postman_form_view, name='postman_create'),
    path('postman/<str:postman_id>/delete/', postman_delete_view, name='postman_delete'),
    path('postman/<str:postman_id>/edit/', postman_form_view, name='postman_edit'),
    path('postman/<str:postman_id>/', postman_detail_view, name='postman_detail'),
    
    # Documentation dashboard AJAX API endpoints
    path('api/dashboard/pages/', media_manager_api.get_pages_list_api, name='api_docs_dashboard_pages'),
    path('api/dashboard/endpoints/', media_manager_api.get_endpoints_list_api, name='api_docs_dashboard_endpoints'),
    path('api/dashboard/relationships/', media_manager_api.get_relationships_list_api, name='api_docs_dashboard_relationships'),
    path('api/dashboard/postman/', media_manager_api.get_postman_list_api, name='api_docs_dashboard_postman'),
    path('api/dashboard/statistics/', media_manager_api.get_statistics_api, name='api_docs_dashboard_statistics'),
    path('api/dashboard/health/', media_manager_api.get_health_api, name='api_docs_dashboard_health'),

    # Pages bulk import (Excel upload -> JSON -> pages create/update)
    path('api/pages/bulk-import/check/', media_manager_api.pages_bulk_import_check_api, name='api_pages_bulk_import_check'),
    path('api/pages/bulk-import/preview/', media_manager_api.pages_bulk_import_preview_api, name='api_pages_bulk_import_preview'),
    path('api/pages/bulk-import/', media_manager_api.pages_bulk_import_api, name='api_pages_bulk_import'),

    # Documentation files API (legacy media API name preserved for compatibility)
    path('api/media/files/', documentation_file_views.list_files_api, name='api_media_files'),
    path('api/media/sync-status/', documentation_file_views.sync_status_api, name='api_media_sync_status'),
    path('api/media/bulk-sync/', documentation_file_views.bulk_sync_api, name='api_media_bulk_sync'),

    # Operations
    path('operations/', operations.operations_dashboard, name='operations_dashboard'),
    path('operations/history/', operations.operations_history, name='operations_history'),
    path('api/operations/history/', operations.operations_history_api, name='api_operations_history'),
    path('api/operations/upload-file-list/<str:resource_type>/', operations.upload_file_list_api, name='api_operations_upload_file_list'),
    path('api/operations/upload-to-s3/<str:resource_type>/', operations.upload_to_s3_api, name='api_operations_upload_to_s3'),
    path('api/operations/upload/start/', operations.upload_start_api, name='api_operations_upload_start'),
    path('api/operations/upload-progress/<str:job_id>/', operations.upload_progress_api, name='api_operations_upload_progress'),
    path('api/operations/analyze/start/', operations.analyze_start_api, name='api_operations_analyze_start'),
    path('api/operations/analyze-progress/<str:job_id>/', operations.analyze_progress_api, name='api_operations_analyze_progress'),
    path('api/operations/generate-json/start/', operations.generate_json_start_api, name='api_operations_generate_json_start'),
    path('api/operations/generate-json-progress/<str:job_id>/', operations.generate_json_progress_api, name='api_operations_generate_json_progress'),
    path('operations/run-pipeline/', operations.run_pipeline_view, name='operations_run_pipeline'),
    path('operations/analyze/', operations.analyze_docs_view, name='operations_analyze'),
    path('operations/validate/', operations.validate_docs_view, name='operations_validate'),
    path('operations/generate-json/', operations.generate_json_view, name='operations_generate_json'),
    path('operations/generate-postman/', operations.generate_postman_view, name='operations_generate_postman'),
    path('operations/upload/', operations.upload_docs_view, name='operations_upload'),
    path('operations/seed/', operations.seed_documentation_view, name='operations_seed'),
    path('operations/workflow/', operations.workflow_view, name='operations_workflow'),
    path('operations/status/', operations.docs_status_view, name='operations_status'),
    path('operations/tasks/', operations.task_list_view, name='operations_tasks'),
    path('operations/tasks/<str:task_id>/', operations.task_detail_view, name='operations_task_detail'),
    
    # Legacy detail/update/delete are still available via new dashboard URLs and enhanced forms
]
