from django.urls import path
from . import views

app_name = "admin_ops"

urlpatterns = [
    path(
        "",
        lambda r: __import__("django.shortcuts", fromlist=["redirect"]).redirect(
            "admin_ops:users"
        ),
        name="index",
    ),
    path("users/", views.users_view, name="users"),
    path("users/<str:user_id>/history/", views.user_history_view, name="user_history"),
    path("users/<str:user_id>/", views.user_detail_view, name="user_detail"),
    path("jobs/", views.jobs_view, name="jobs"),
    path("jobs/<str:job_id>/retry/", views.job_retry_view, name="job_retry"),
    path("jobs/<str:job_id>/", views.job_detail_view, name="job_detail"),
    path("logs/", views.logs_view, name="logs"),
    path("logs/bulk-delete/", views.logs_bulk_delete_view, name="logs_bulk_delete"),
    path("logs/<str:log_id>/update/", views.log_update_view, name="log_update"),
    path("logs/<str:log_id>/delete/", views.delete_log_view, name="delete_log"),
    path("billing/payments/", views.billing_view, name="billing"),
    path(
        "billing/payments/<str:payment_id>/approve/",
        views.approve_payment_view,
        name="approve_payment",
    ),
    path(
        "billing/payments/<str:payment_id>/decline/",
        views.decline_payment_view,
        name="decline_payment",
    ),
    path(
        "billing/plans/new/", views.billing_plan_create_view, name="billing_plan_create"
    ),
    path(
        "billing/plans/<str:tier>/period/<str:period>/delete/",
        views.billing_plan_period_delete_view,
        name="billing_plan_period_delete",
    ),
    path(
        "billing/plans/<str:tier>/period/<str:period>/edit/",
        views.billing_plan_period_edit_view,
        name="billing_plan_period_edit",
    ),
    path(
        "billing/plans/<str:tier>/period/add/",
        views.billing_plan_period_add_view,
        name="billing_plan_period_add",
    ),
    path(
        "billing/plans/<str:tier>/delete/",
        views.billing_plan_delete_view,
        name="billing_plan_delete",
    ),
    path(
        "billing/plans/<str:tier>/edit/",
        views.billing_plan_edit_view,
        name="billing_plan_edit",
    ),
    path("billing/plans/", views.billing_plans_view, name="billing_plans"),
    path(
        "billing/addons/new/",
        views.billing_addon_create_view,
        name="billing_addon_create",
    ),
    path(
        "billing/addons/<str:package_id>/delete/",
        views.billing_addon_delete_view,
        name="billing_addon_delete",
    ),
    path(
        "billing/addons/<str:package_id>/edit/",
        views.billing_addon_edit_view,
        name="billing_addon_edit",
    ),
    path("billing/addons/", views.billing_addons_view, name="billing_addons"),
    path("billing/settings/", views.billing_settings_view, name="billing_settings"),
    path("storage/", views.storage_view, name="storage"),
    path(
        "storage/download-url/",
        views.storage_download_url_view,
        name="storage_download_url",
    ),
    path("storage/delete/", views.delete_artifact_view, name="delete_artifact"),
    path("system-status/", views.system_status_view, name="system_status"),
    path("settings/", views.settings_view, name="settings"),
    path("statistics/", views.statistics_view, name="statistics"),
]
