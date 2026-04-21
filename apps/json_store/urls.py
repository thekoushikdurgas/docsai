"""URLs for ``apps.json_store``."""

from django.urls import path
from . import views

app_name = "json_store"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("upload/", views.upload_view, name="upload"),
    path("<int:doc_id>/view/", views.view_json_view, name="view"),
    path("<int:doc_id>/delete/", views.delete_view, name="delete"),
    path("<int:doc_id>/download/", views.download_view, name="download"),
]
