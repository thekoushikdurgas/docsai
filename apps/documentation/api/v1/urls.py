"""
REST API v1 — health, dashboard, docs meta, pages, endpoints, relationships, postman.
"""

from django.urls import path, include

from . import views

app_name = "api_v1"

urlpatterns = [
    path("", views.service_info, name="service_info"),
    path("health/", views.health_view, name="health"),
    path("health/database/", views.health_database, name="health_database"),
    path("health/cache/", views.health_cache, name="health_cache"),
    path("health/storage/", views.health_storage, name="health_storage"),
    path("docs/endpoint-stats/", views.endpoint_stats, name="endpoint_stats"),
    path(
        "docs/endpoint-stats-by-user-type/",
        views.endpoint_stats_by_user_type,
        name="endpoint_stats_by_user_type",
    ),
    path("pages/", include("apps.documentation.api.v1.pages_urls")),
    path("endpoints/", include("apps.documentation.api.v1.endpoints_urls")),
    path("relationships/", include("apps.documentation.api.v1.relationships_urls")),
    path("postman/", include("apps.documentation.api.v1.postman_urls")),
    path("dashboard/pages/", views.dashboard_pages, name="dashboard_pages"),
    path("dashboard/endpoints/", views.dashboard_endpoints, name="dashboard_endpoints"),
    path(
        "dashboard/relationships/",
        views.dashboard_relationships,
        name="dashboard_relationships",
    ),
    path("dashboard/postman/", views.dashboard_postman, name="dashboard_postman"),
]
