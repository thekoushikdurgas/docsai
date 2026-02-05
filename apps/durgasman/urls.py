"""URL configuration for Durgasman app."""

from django.urls import path
from . import views
from .api import execute

app_name = 'durgasman'

urlpatterns = [
    # Main views
    path('', views.dashboard, name='dashboard'),
    path('collection/<str:collection_id>/', views.collection_detail, name='collection_detail'),
    path('import/', views.import_view, name='import_view'),

    # API endpoints
    path('api/collections/', views.api_collections, name='api_collections'),
    path('api/collections/<str:collection_id>/requests/', views.api_collection_requests, name='api_collection_requests'),
    path('api/requests/<str:request_id>/', views.api_request_detail, name='api_request_detail'),
    path('api/environments/', views.api_environments, name='api_environments'),
    path('api/history/', views.api_history, name='api_history'),
    path('api/mocks/', views.api_mocks, name='api_mocks'),
    path('api/analyze/', views.api_analyze_response, name='api_analyze'),
    path('api/execute/', execute.execute_request, name='api_execute'),
]