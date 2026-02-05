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
]
