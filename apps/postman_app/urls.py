from django.urls import path
from . import views
app_name = "postman_app"
urlpatterns = [path("", views.dashboard_view, name="dashboard")]
