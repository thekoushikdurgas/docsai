from django.urls import path

from . import views

app_name = "durgasman"

urlpatterns = [
    # Main dashboard (3-pane Postman UI)
    path("", views.dashboard, name="dashboard"),
    # Upload page + upload endpoints
    path("upload/", views.upload_view, name="upload"),
    path("upload/collection/", views.upload_collection_view, name="upload_collection"),
    path(
        "upload/environment/", views.upload_environment_view, name="upload_environment"
    ),
    # Collections API (JSON responses)
    path("collections/", views.collections_list_view, name="collections_list"),
    path(
        "collections/<int:col_id>/json/",
        views.collection_json_view,
        name="collection_json",
    ),
    path(
        "collections/<int:col_id>/delete/",
        views.collection_delete_view,
        name="collection_delete",
    ),
    # Environments API (JSON responses)
    path("environments/", views.environments_list_view, name="environments_list"),
    path(
        "environments/<int:env_id>/json/",
        views.environment_json_view,
        name="environment_json",
    ),
    path(
        "environments/<int:env_id>/delete/",
        views.environment_delete_view,
        name="environment_delete",
    ),
    # Request proxy
    path("send/", views.send_request_view, name="send"),
    # Legacy stubs kept for JS compatibility
    path("api/collections/", views.api_collections, name="api_collections"),
    path("api/environments/", views.api_environments, name="api_environments"),
    path("api/history/", views.api_history, name="api_history"),
    path("api/analyze/", views.api_analyze_response, name="api_analyze"),
]
