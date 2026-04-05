from django.urls import path
from . import views
app_name = "json_store"
urlpatterns = [path("", views.index_view, name="index")]
