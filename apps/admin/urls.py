"""URL configuration for admin app."""
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'admin'

urlpatterns = [
    path('', RedirectView.as_view(url='/admin/users/', permanent=False), name='index'),
    path('users/', views.users_view, name='users'),
    path('user-history/', views.user_history_view, name='user_history'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('logs/', views.logs_view, name='logs'),
    path('logs/bulk-delete/', views.logs_bulk_delete_view, name='logs_bulk_delete'),
    path('logs/<str:log_id>/update/', views.log_update_view, name='log_update'),
    path('logs/<str:log_id>/delete/', views.log_delete_view, name='log_delete'),
    path('system-status/', views.system_status_view, name='system_status'),
    path('settings/', views.settings_view, name='settings'),
    # Job Scheduler (lambda/tkdjob)
    path('jobs/', views.jobs_view, name='jobs'),
    path('jobs/<str:job_uuid>/detail/', views.job_detail_view, name='job_detail'),
    path('jobs/<str:job_uuid>/retry/', views.job_retry_view, name='job_retry'),
    # Storage Files (lambda/s3storage)
    path('storage/', views.storage_files_view, name='storage_files'),
    path('storage/download-url/', views.storage_download_url_view, name='storage_download_url'),
    path('storage/delete/', views.storage_delete_view, name='storage_delete'),
    # Managed billing (manual UPI proofs)
    path('billing/payments/', views.billing_payments_view, name='billing_payments'),
    path('billing/qr-upload/', views.billing_qr_upload_view, name='billing_qr_upload'),
    path('billing/payments/<str:submission_id>/approve/', views.billing_payment_approve_view, name='billing_payment_approve'),
    path('billing/payments/<str:submission_id>/decline/', views.billing_payment_decline_view, name='billing_payment_decline'),
    path('billing/settings/', views.billing_settings_view, name='billing_settings'),
]
