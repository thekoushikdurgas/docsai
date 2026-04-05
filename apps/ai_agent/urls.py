from django.urls import path
from . import views
app_name = "ai_agent"
urlpatterns = [
    path("chat/", views.chat_view, name="chat"),
    path("sessions/", views.sessions_view, name="sessions"),
    path("sessions/<str:session_id>/", views.session_detail_view, name="session_detail"),
    path("api/chat/", views.api_chat_view, name="api_chat"),
]
