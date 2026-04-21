"""URLs for ``apps.architecture`` (blueprint)."""

from django.urls import path
from . import views

app_name = "architecture"
urlpatterns = [path("", views.blueprint_view, name="blueprint")]
